// Gestion des messages flash
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Gestion du menu utilisateur moderne
const userDropdown = document.querySelector('.user-dropdown');
if (userDropdown) {
    const userBtn = userDropdown.querySelector('.user-btn');
    userBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        userDropdown.classList.toggle('open');
    });
    document.addEventListener('click', function(e) {
        if (!userDropdown.contains(e.target)) {
            userDropdown.classList.remove('open');
        }
    });
}

// Gestion des formulaires
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', async (e) => {
        if (form.dataset.confirm) {
            e.preventDefault();
            if (confirm(form.dataset.confirm)) {
                form.submit();
            }
        }
    });
});

// Gestion des tableaux de données
const tables = document.querySelectorAll('.table');
tables.forEach(table => {
    const searchInput = table.parentElement.querySelector('.table-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
});

// Gestion des modales
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

// Fermeture des modales en cliquant en dehors
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        closeModal(e.target.id);
    }
});

// Gestion des notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Gestion des dates
function formatDate(date) {
    return new Date(date).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Gestion des statuts
function getStatusClass(status) {
    const statusClasses = {
        'à jour': 'status-success',
        'en retard': 'status-warning',
        'urgent': 'status-danger'
    };
    return statusClasses[status.toLowerCase()] || 'status-info';
}

// Gestion des rôles
function checkRole(requiredRole) {
    const userRole = localStorage.getItem('userRole');
    return userRole === requiredRole;
}

// Gestion des permissions
function updateUIByRole() {
    const userRole = localStorage.getItem('userRole');
    if (!userRole) return;
    // Liens du header et actions rapides
    document.querySelectorAll('[data-role]').forEach(el => {
        const roles = el.getAttribute('data-role').split(' ');
        el.style.display = roles.includes(userRole) ? '' : 'none';
    });
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    // Stocke le rôle de l'utilisateur connecté (à faire côté backend lors du login)
    if (window.currentUserRole) {
        localStorage.setItem('userRole', window.currentUserRole);
    }
    updateUIByRole();
}); 