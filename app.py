from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta, date
import os
from dotenv import load_dotenv
from datetime import date
from vaccination_backend import db
from sqlalchemy import extract, func
from werkzeug.security import generate_password_hash, check_password_hash
from vaccination_backend.utils.statut import mettre_a_jour_statut_vaccination

# Import des modèles du backend
from vaccination_backend.models.utilisateur import Utilisateur
from vaccination_backend.models.enfant import Enfant
from vaccination_backend.models.vaccin import Vaccin
from vaccination_backend.models.vaccination import Vaccination
from vaccination_backend.models.alerte import Alerte
from vaccination_backend import init_app as init_backend
from vaccination_backend.utils.alerts import verifier_et_creer_alertes


# Chargement des variables d'environnement
load_dotenv()

# Initialisation de l'application
app = Flask(__name__, 
    template_folder='vaccination_frontend/templates',
    static_folder='vaccination_frontend/static'
)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'votre_cle_secrete_par_defaut')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'votre_cle_jwt_par_defaut')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialisation des extensions
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

jwt = JWTManager(app)

# Initialisation du backend
init_backend(app)

# Configuration du login manager
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Utilisateur, int(user_id))

# Routes principales
@app.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('accueil.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Utilisateur.query.filter_by(email=email).first()

        if user and check_password_hash(user.mot_de_passe, password):
            login_user(user)
            return redirect(url_for('dashboard'))  # ✅ Ne renvoie pas de JSON
        else:
            flash("Email ou mot de passe incorrect.", "error")
            return redirect(url_for('login'))  # ✅ Redirige avec flash message

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 1. Fonction de vérification (à coller AVANT la route dashboard)
def verifier_et_creer_alertes():
    today = date.today()
    vaccinations = Vaccination.query.all()

    for v in vaccinations:
        vaccin = db.session.get(Vaccin, v.vaccin_id)
        if not vaccin:
            continue

        prochaine_dose = v.dose + 1

        if prochaine_dose <= vaccin.nombre_doses:
            max_date = v.date_vaccination + timedelta(days=30 * prochaine_dose)

            # ✅ Mise à jour du statut de vaccination
            if today > max_date:
                v.statut_vaccination = 'en retard'
            else:
                v.statut_vaccination = 'à jour'

            # ✅ Création d’alerte si nécessaire
            existe = Alerte.query.filter_by(
                enfant_id=v.id_enfant,
                titre=f"Rappel en retard ({vaccin.nom_vaccin})",
                statut='active'
            ).first()

            if today > max_date and not existe:
                alerte = Alerte(
                    type="rappel",
                    titre=f"Rappel en retard ({vaccin.nom_vaccin})",
                    description=f"La dose {prochaine_dose} du vaccin {vaccin.nom_vaccin} est en retard.",
                    date_alerte=today,
                    date_echeance=max_date,
                    enfant_id=v.id_enfant,
                    utilisateur_id=1  # À adapter si plusieurs utilisateurs
                )
                alerte.save()

    db.session.commit()  


@app.route('/dashboard')
@login_required
def dashboard():
    verifier_et_creer_alertes()
    today = date.today()
    in_7_days = today + timedelta(days=7)

    # Initialisation pour éviter UnboundLocalError
    vaccinations_recents = []
    rappels_imminents = []
    dernières_vaccinations = []

    if current_user.role == 'parent':
        enfants = Enfant.query.filter_by(parent_id=current_user.id_utilisateur).all()
        enfants_ids = [e.id_enfant for e in enfants]
        vaccinations = Vaccination.query.filter(Vaccination.id_enfant.in_(enfants_ids)).all()
        alertes = Alerte.query.filter(Alerte.enfant_id.in_(enfants_ids)).order_by(Alerte.date_alerte.desc()).limit(3).all()
        alertes_urgentes = sum(1 for a in alertes if a.priorite == 'haute')

        vaccinations = Vaccination.query.all()

        enfants_a_jour = 0
        enfants_en_retard = 0
        
        for enfant in enfants:
            vaccins = Vaccination.query.filter_by(id_enfant=enfant.id_enfant).all()
            
            if not vaccins:
                enfants_en_retard += 1
            elif all(v.statut_vaccination == 'à jour' for v in vaccins):
                enfants_a_jour += 1
            else:
                enfants_en_retard += 1



    else:
        enfants = Enfant.query.all()
        vaccinations = Vaccination.query.all()
        enfants_a_jour = 0
        enfants_en_retard = 0

        for enfant in enfants:
            vaccins_enfant = [v for v in vaccinations if v.id_enfant == enfant.id_enfant]
            if all(v.statut_vaccination == 'à jour' for v in vaccins_enfant):
                enfants_a_jour += 1
            elif any(v.statut_vaccination == 'en retard' for v in vaccins_enfant):
                enfants_en_retard += 1

        alertes = Alerte.query.order_by(Alerte.date_alerte.desc()).limit(3).all()
        alertes_urgentes = Alerte.query.filter_by(priorite='haute').count()

        # Dernières vaccinations enrichies (affichage avec nom)
        dernières_vaccinations = db.session.query(
            Vaccination, Enfant, Vaccin
        ).join(
            Enfant, Vaccination.id_enfant == Enfant.id_enfant
        ).join(
            Vaccin, Vaccination.vaccin_id == Vaccin.vaccin_id
        ).order_by(Vaccination.date_vaccination.desc()).limit(5).all()

        # Rappels imminents dans les 7 jours
        rappels_imminents = Alerte.query.filter(
            Alerte.date_echeance.between(today, in_7_days),
            Alerte.statut == 'active'
        ).order_by(Alerte.date_echeance.asc()).limit(5).all()

        # Vaccinations récentes (à afficher dans bloc "dernières actions")
        vaccinations_recents = dernières_vaccinations

    stats = {
        "enfants_a_jour": enfants_a_jour,
        "enfants_en_retard": enfants_en_retard,
        "alertes_urgentes": alertes_urgentes
    }

    return render_template(
        'dashboard.html',
        stats=stats,
        alertes=alertes,
        vaccinations_recents=vaccinations_recents,
        rappels_imminents=rappels_imminents,
        dernières_vaccinations=dernières_vaccinations,
        current_user_role=current_user.role
    )

def calculate_age(date_naissance):
    today = date.today()
    return today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))

@app.route('/enfants')
@login_required
def enfants():
    verifier_et_creer_alertes()

    if current_user.role == 'parent':
        enfants = Enfant.query.filter_by(parent_id=current_user.id_utilisateur).all()
        parents = [current_user]
    else:
        enfants = Enfant.query.all()
        parents = Utilisateur.query.filter_by(role='parent').all()

    for e in enfants:
        e.age = calculate_age(e.date_naissance)

        # ✅ Corrigé : on récupère manuellement les vaccinations
        vaccinations = Vaccination.query.filter_by(id_enfant=e.id_enfant).all()

        if not vaccinations:
            e.statut_vaccinal = "en retard"
        elif all(v.statut_vaccination == "à jour" for v in vaccinations):
            e.statut_vaccinal = "à jour"
        else:
            e.statut_vaccinal = "en retard"

    return render_template('enfants.html', enfants=enfants, parents=parents)

@app.route('/vaccins')
@login_required
def vaccins():
    vaccins = Vaccin.query.all()
    return render_template('vaccins.html', vaccins=vaccins)

@app.route('/vaccinations')
@login_required
def vaccinations():
    results = db.session.query(Vaccination, Enfant, Vaccin).join(Enfant).join(Vaccin).all()

    vaccinations = []
    for vaccination, enfant, vaccin in results:
        vaccinations.append({
            "id": vaccination.id_vaccination,
            "prenom": enfant.prenom,
            "nom": enfant.nom,
            "vaccin": vaccin.nom_vaccin,
            "date": vaccination.date_vaccination.strftime('%d/%m/%Y'),
            "dose": f"{vaccination.dose}/{vaccin.nombre_doses}",
            "statut": vaccination.statut_vaccination
        })

    enfants = Enfant.query.all()
    vaccins = Vaccin.query.all()

    return render_template('vaccinations.html', vaccinations=vaccinations, enfants=enfants, vaccins=vaccins)

@app.route('/alertes')
@login_required
def alertes():
    if current_user.role == 'parent':
        enfants = Enfant.query.filter_by(parent_id=current_user.id_utilisateur).all()
        enfants_ids = [e.id_enfant for e in Enfant.query.filter_by(parent_id=current_user.id_utilisateur).all()]
        alertes = Alerte.query.filter(Alerte.enfant_id.in_(enfants_ids)).order_by(Alerte.date_alerte.desc()).all()
    else:
        alertes = Alerte.query.order_by(Alerte.date_alerte.desc()).all()
    
    return render_template('alertes.html', alertes=alertes)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/analyses')
@login_required
def analyses():
    from vaccination_backend.models.vaccination import Vaccination
    from vaccination_backend.models.enfant import Enfant
    from vaccination_backend.models.vaccin import Vaccin
    from vaccination_backend.models.alerte import Alerte

    # Total vaccinations
    total_vaccinations = Vaccination.query.count()
    total_enfants = Enfant.query.count()
    total_retard = Vaccination.query.filter_by(statut_vaccination='en retard').count()

    # Taux de couverture
    taux_couverture = round(((total_vaccinations - total_retard) / total_vaccinations) * 100, 2) if total_vaccinations else 0

    # Tendance vaccinations
    now = datetime.now()
    mois_courant = now.month
    mois_precedent = (now - timedelta(days=30)).month

    count_mois_courant = db.session.query(func.count()).filter(extract('month', Vaccination.date_vaccination) == mois_courant).scalar()
    count_mois_precedent = db.session.query(func.count()).filter(extract('month', Vaccination.date_vaccination) == mois_precedent).scalar()
    tendance_vaccinations = round(((count_mois_courant - count_mois_precedent) / count_mois_precedent) * 100, 2) if count_mois_precedent else 0

    # Tendance couverture (même valeur ici pour simplification)
    tendance_couverture = tendance_vaccinations

    # Tendance des retards
    count_retard_precedent = db.session.query(func.count()).filter(
        extract('month', Vaccination.date_vaccination) == mois_precedent,
        Vaccination.statut_vaccination == 'en retard'
    ).scalar()
    tendance_retard = round(((total_retard - count_retard_precedent) / count_retard_precedent) * 100, 2) if count_retard_precedent else 0

    # Vaccins populaires
    popular_vaccins = db.session.query(
        Vaccin.nom_vaccin,
        func.count(Vaccination.vaccin_id).label("nb")
    ).join(Vaccination, Vaccin.vaccin_id == Vaccination.vaccin_id).group_by(Vaccin.nom_vaccin).order_by(func.count(Vaccination.vaccin_id).desc()).limit(5).all()

    vaccins_populaires = []
    for nom, nb in popular_vaccins:
        pourcentage = round((nb / total_vaccinations) * 100, 1) if total_vaccinations else 0
        vaccins_populaires.append({
            "nom": nom,
            "nombre": nb,
            "pourcentage": pourcentage
        })

    # Alertes récentes (voir message précédent)
    alertes_courantes = db.session.query(
        Alerte.type,
        func.count(Alerte.id)
    ).filter(
        extract('month', Alerte.date_alerte) == mois_courant
    ).group_by(Alerte.type).all()

    alertes_precedentes = db.session.query(
        Alerte.type,
        func.count(Alerte.id)
    ).filter(
        extract('month', Alerte.date_alerte) == mois_precedent
    ).group_by(Alerte.type).all()

    current_dict = {t: c for t, c in alertes_courantes}
    prev_dict = {t: c for t, c in alertes_precedentes}

    alertes_recentes = []
    for t in set(current_dict.keys()).union(prev_dict.keys()):
        now_count = current_dict.get(t, 0)
        prev_count = prev_dict.get(t, 1)
        tendance = round(((now_count - prev_count) / prev_count) * 100) if prev_count else now_count * 100
        alertes_recentes.append({
            "type": t,
            "nombre": now_count,
            "tendance": tendance
        })

    # Résumé final
    stats = {
        "total_vaccinations": total_vaccinations,
        "taux_couverture": taux_couverture,
        "tendance_vaccinations": tendance_vaccinations,
        "tendance_couverture": tendance_couverture,
        "vaccins_retard": total_retard,
        "tendance_retard": tendance_retard,
        "vaccins_populaires": vaccins_populaires,
        "alertes_recentes": alertes_recentes
    }

    return render_template("analyses.html", stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'parent')
        # Vérifier si l'utilisateur existe déjà
        if Utilisateur.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé.', 'error')
            return render_template('register.html')
        # Créer et sauvegarder le nouvel utilisateur
        user = Utilisateur(email=email, role=role)
        user.set_password(password)
        user.save()
        flash('Compte créé avec succès. Vous pouvez vous connecter.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/politique')
def politique():
    return render_template('politique.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Ici, vous pouvez traiter le formulaire de contact si besoin
        flash('Votre message a bien été envoyé. Merci de nous avoir contactés.', 'success')
        return render_template('contact.html')
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

# Routes API pour les enfants
@app.route('/api/enfants', methods=['GET'])
def get_enfants():
    enfants = Enfant.query.all()
    return jsonify({
        'success': True,
        'data': [enfant.to_dict() for enfant in enfants]
    })

@app.route('/enfant/modifier/<int:id>', methods=['POST'])
@login_required
def modifier_enfant(id):
    enfant = db.session.get(Enfant, id)
    if not enfant:
        flash("Enfant introuvable", "error")
        return redirect(url_for('enfants'))

    try:
        enfant.prenom = request.form.get('prenom')
        enfant.nom = request.form.get('nom')
        enfant.sexe = request.form.get('sexe')
        enfant.date_naissance = datetime.strptime(request.form.get('date_naissance'), '%Y-%m-%d').date()
        db.session.commit()
        flash("Informations de l’enfant mises à jour.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erreur lors de la mise à jour : " + str(e), "error")

    return redirect(url_for('enfants'))

@app.route('/api/enfants', methods=['POST'])
def create_enfant():
    data = request.get_json()
    try:
        enfant = Enfant(**data)
        enfant.save()
        return jsonify({'success': True, 'data': enfant.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/enfant/<int:id>')
@login_required
def get_enfant(id):
    enfant = db.session.get(Enfant, id)
    if not enfant:
        return jsonify({'success': False, 'message': 'Enfant introuvable'}), 404

    vaccinations = Vaccination.query.filter_by(id_enfant=enfant.id_enfant).all()

    if not vaccinations:
        statut = "en retard"
    elif all(v.statut_vaccination == "à jour" for v in vaccinations):
        statut = "à jour"
    else:
        statut = "en retard"

    return jsonify({
        "prenom": enfant.prenom,
        "nom": enfant.nom,
        "sexe": enfant.sexe,
        "date_naissance": enfant.date_naissance.isoformat(),
        "age": calculate_age(enfant.date_naissance),
        "statut_vaccinal": statut,
        "parent": db.session.get(Utilisateur, enfant.parent_id).email if enfant.parent_id else "Non assigné"
    })


@app.route('/api/enfants/<int:id>', methods=['DELETE'])
def delete_enfant(id):
    try:
        enfant = Enfant.query.get_or_404(id)

        # Supprimer les vaccinations liées
        vaccinations = Vaccination.query.filter_by(id_enfant=enfant.id_enfant).all()
        for v in vaccinations:
            db.session.delete(v)

        # Supprimer les alertes liées
        alertes = Alerte.query.filter_by(enfant_id=enfant.id_enfant).all()
        for a in alertes:
            db.session.delete(a)

        # Enfin supprimer l’enfant
        db.session.delete(enfant)
        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print("Erreur de suppression :", e)
        return jsonify({'success': False, 'message': str(e)}), 400



# Routes API pour les vaccins
@app.route('/api/vaccins', methods=['GET'])
def get_vaccins():
    vaccins = Vaccin.query.all()
    return jsonify({
        'success': True,
        'data': [vaccin.to_dict() for vaccin in vaccins]
    })

@app.route('/api/vaccins', methods=['POST'])
def create_vaccin():
    data = request.get_json()
    try:
        vaccin = Vaccin(**data)
        vaccin.save()
        return jsonify({'success': True, 'data': vaccin.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/vaccins/<int:id>', methods=['PUT'])
def update_vaccin(id):
    vaccin = db.session.get(Vaccin, id)
    if not vaccin:
        return jsonify({'success': False, 'message': 'Vaccin introuvable'}), 404

    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(vaccin, key, value)
        vaccin.save()
        return jsonify({'success': True, 'data': vaccin.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/vaccins/<int:id>', methods=['DELETE'])
def delete_vaccin(id):
    vaccin = Vaccin.query.get_or_404(id)
    try:
        vaccin.delete()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/vaccin/<int:id>', methods=['GET'])
@login_required
def get_vaccin(id):
    vaccin = db.session.get(Vaccin, id)
    if not vaccin:
        return jsonify({'success': False, 'message': 'Vaccin introuvable'}), 404

    return jsonify({
        'nom': vaccin.nom_vaccin,
        'type': vaccin.type_vaccin,
        'age_recommande': vaccin.age_recommande,
        'nombre_doses': vaccin.nombre_doses,
        'intervalle': vaccin.intervalle,
        'description': vaccin.description
    })

# Routes API pour les vaccinations
@app.route('/api/vaccinations', methods=['GET'])
def get_vaccinations():
    vaccinations = Vaccination.query.all()
    return jsonify({
        'success': True,
        'data': [vaccination.to_dict() for vaccination in vaccinations]
    })

@app.route('/api/vaccinations', methods=['POST'])
def create_vaccination():
    data = request.get_json()
    try:
        vaccination = Vaccination(**data)
        mettre_a_jour_statut_vaccination(vaccination)
        vaccination.save()
        return jsonify({'success': True, 'data': vaccination.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/api/vaccinations/<int:id>', methods=['PUT'])
def update_vaccination(id):
    vaccination = db.session.get(Vaccination, id)
    if not vaccination:
        return jsonify({'success': False, 'message': 'Vaccination introuvable'}), 404

    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(vaccination, key, value)
        vaccination.save()
        return jsonify({'success': True, 'data': vaccination.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/vaccinations/<int:id>', methods=['DELETE'])
def delete_vaccination(id):
    vaccination = Vaccination.query.get_or_404(id)
    try:
        vaccination.delete()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Routes API pour les alertes
@app.route('/api/alertes', methods=['GET'])
def get_alertes():
    alertes = Alerte.query.all()
    return jsonify({
        'success': True,
        'data': [alerte.to_dict() for alerte in alertes]
    })

@app.route('/api/alertes', methods=['POST'])
def create_alerte():
    data = request.get_json()
    try:
        alerte = Alerte(**data)
        alerte.save()
        return jsonify({'success': True, 'data': alerte.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/alertes/<int:id>', methods=['PUT'])
def update_alerte(id):
    alerte = db.session.get(Alerte, id)
    if not alerte:
        return jsonify({'success': False, 'message': 'Alerte introuvable'}), 404

    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(alerte, key, value)
        alerte.save()
        return jsonify({'success': True, 'data': alerte.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/alertes/<int:id>', methods=['DELETE'])
def delete_alerte(id):
    alerte = Alerte.query.get_or_404(id)
    try:
        alerte.delete()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Routes API pour les guides
@app.route('/api/guides/<guide_id>')
def get_guide(guide_id):
    # Logique pour récupérer le contenu d'un guide
    return jsonify({'success': True, 'content': ''})

# Routes API pour le support
@app.route('/api/support/contact', methods=['POST'])
def contact_support():
    data = request.get_json()
    try:
        # Logique pour envoyer un email au support
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# Gestion des erreurs
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True) 