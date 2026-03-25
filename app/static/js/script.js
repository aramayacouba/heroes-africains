// Initialisation globale
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeSearch();
});

// Initialiser la navigation
function initializeNavigation() {
    // Charger les catégories
    fetch('/api/categories')
        .then(response => response.json())
        .then(data => {
            const menu = document.getElementById('categoriesMenu');
            if (menu) {
                menu.innerHTML = '';
                data.categories.forEach(cat => {
                    const li = document.createElement('li');
                    li.innerHTML = `<a class="dropdown-item" href="/category/${cat.id}">
                        ${cat.icon} ${cat.name}
                    </a>`;
                    menu.appendChild(li);
                });
            }
        })
        .catch(error => console.error('Erreur lors du chargement des catégories:', error));
}

// Initialiser la recherche
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    let searchTimeout;
    searchInput.addEventListener('keyup', function(e) {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();

        if (query.length < 2) {
            document.getElementById('searchResults').innerHTML = '';
            return;
        }

        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
}

// Effectuer une recherche
function performSearch(query) {
    fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            if (data.results && data.results.length > 0) {
                let resultsHTML = '<div class="dropdown-menu show" style="position: absolute; top: 100%; left: 0; right: 0; z-index: 1000;">';
                
                data.results.forEach(hero => {
                    resultsHTML += `
                        <a class="dropdown-item" href="/hero/${hero.id}">
                            <strong>${hero.name}</strong>
                            <small class="text-muted d-block">${hero.country} • ${hero.era}</small>
                        </a>
                    `;
                });
                
                resultsHTML += '</div>';
                // Afficher les résultats (vous pouvez créer un dropdown pour cela)
            }
        })
        .catch(error => console.error('Erreur lors de la recherche:', error));
}

// Formatage des nombres
function formatNumber(num) {
    return new Intl.NumberFormat('fr-FR').format(num);
}

// Notification toast
function showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.innerHTML = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}