// AWKWARD LEGACY - Application JavaScript

// Configuration API
const API_CONFIG = {
    baseURL: 'http://localhost:8000/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
};

// État de l'application
const AppState = {
    user: null,
    token: null,
    currentPage: 'home',
    persons: [],
    families: [],
    searchResults: [],
    statistics: {
        totalPersons: 0,
        totalFamilies: 0,
        avgChildren: 0,
        maxGenerations: 0
    }
};

// Classe API pour gérer les requêtes
class APIClient {
    constructor(config) {
        this.config = config;
        this.token = localStorage.getItem('authToken');
    }

    async request(endpoint, options = {}) {
        const url = `${this.config.baseURL}${endpoint}`;
        const headers = {
            ...this.config.headers,
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers,
                timeout: this.config.timeout
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            showToast('Erreur de connexion à l\'API', 'error');
            throw error;
        }
    }

    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('authToken', token);
        } else {
            localStorage.removeItem('authToken');
        }
    }

    // Auth endpoints
    async login(email, password) {
        const response = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        this.setToken(response.token);
        return response;
    }

    async register(name, email, password) {
        return await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password })
        });
    }

    async logout() {
        await this.request('/auth/logout', { method: 'POST' });
        this.setToken(null);
    }

    // Person endpoints
    async searchPersons(criteria) {
        const params = new URLSearchParams(criteria).toString();
        return await this.request(`/persons/search?${params}`);
    }

    async getPerson(id) {
        return await this.request(`/persons/${id}`);
    }

    async createPerson(data) {
        return await this.request('/persons', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updatePerson(id, data) {
        return await this.request(`/persons/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // Family endpoints
    async getFamilies() {
        return await this.request('/families');
    }

    async getFamily(id) {
        return await this.request(`/families/${id}`);
    }

    async createFamily(data) {
        return await this.request('/families', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // Tree endpoints
    async getTree(personId, type = 'full', generations = 4) {
        return await this.request(`/tree/${personId}?type=${type}&generations=${generations}`);
    }

    // Statistics endpoints
    async getStatistics() {
        return await this.request('/statistics');
    }

    // Activity endpoints
    async getRecentActivity() {
        return await this.request('/activity/recent');
    }

    // RGPD endpoints
    async exportUserData() {
        return await this.request('/rgpd/export', { method: 'POST' });
    }

    async deleteUserData() {
        return await this.request('/rgpd/delete', { method: 'DELETE' });
    }
}

// Initialiser le client API
const api = new APIClient(API_CONFIG);

// Gestion de la navigation
function navigateToPage(pageName) {
    // Masquer toutes les pages
    document.querySelectorAll('.page').forEach(page => {
        page.style.display = 'none';
    });

    // Afficher la page demandée
    const targetPage = document.getElementById(`${pageName}Page`);
    if (targetPage) {
        targetPage.style.display = 'block';
        AppState.currentPage = pageName;
    }

    // Mettre à jour la navigation active
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-page') === pageName) {
            link.classList.add('active');
        }
    });

    // Charger les données spécifiques à la page
    loadPageData(pageName);
}

// Charger les données de la page
async function loadPageData(pageName) {
    switch(pageName) {
        case 'home':
            await loadHomeData();
            break;
        case 'search':
            // Les données se chargent lors de la recherche
            break;
        case 'tree':
            await loadTreeData();
            break;
        case 'stats':
            await loadStatistics();
            break;
    }
}

// Charger les données de la page d'accueil
async function loadHomeData() {
    try {
        // Charger les statistiques
        const stats = await api.getStatistics();
        updateHomeStatistics(stats);

        // Charger l'activité récente
        const activity = await api.getRecentActivity();
        updateRecentActivity(activity);
    } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
    }
}

// Mettre à jour les statistiques de la page d'accueil
function updateHomeStatistics(stats) {
    document.getElementById('statPersons').textContent = stats.totalPersons || '0';
    document.getElementById('statFamilies').textContent = stats.totalFamilies || '0';
    document.getElementById('statGenerations').textContent = stats.maxGenerations || '0';
    document.getElementById('lastUpdate').textContent = formatDate(stats.lastUpdate) || '-';
}

// Mettre à jour l'activité récente
function updateRecentActivity(activities) {
    const container = document.getElementById('recentActivity');

    if (!activities || activities.length === 0) {
        container.innerHTML = '<p class="text-muted">Aucune activité récente</p>';
        return;
    }

    container.innerHTML = activities.map(activity => `
        <div class="activity-item d-flex align-items-center">
            <div class="activity-icon">
                <i class="bi ${getActivityIcon(activity.type)}"></i>
            </div>
            <div class="flex-grow-1">
                <div>${activity.description}</div>
                <small class="activity-time">${formatTimeAgo(activity.timestamp)}</small>
            </div>
        </div>
    `).join('');
}

// Obtenir l'icône pour un type d'activité
function getActivityIcon(type) {
    const icons = {
        'create': 'bi-plus-circle',
        'update': 'bi-pencil',
        'delete': 'bi-trash',
        'view': 'bi-eye',
        'login': 'bi-box-arrow-in-right',
        'logout': 'bi-box-arrow-right'
    };
    return icons[type] || 'bi-circle';
}

// Recherche rapide
document.getElementById('quickSearchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = document.getElementById('quickSearch').value;

    if (query.trim()) {
        navigateToPage('search');
        await performSearch({ query });
    }
});

// Recherche avancée
document.getElementById('advancedSearchForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const criteria = {
        firstName: document.getElementById('searchFirstName').value,
        lastName: document.getElementById('searchLastName').value,
        birthYear: document.getElementById('searchBirthYear').value,
        deathYear: document.getElementById('searchDeathYear').value,
        place: document.getElementById('searchPlace').value
    };

    await performSearch(criteria);
});

// Effectuer une recherche
async function performSearch(criteria) {
    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '<div class="spinner-container"><div class="spinner-border text-primary"></div></div>';

    try {
        const results = await api.searchPersons(criteria);
        AppState.searchResults = results;
        displaySearchResults(results);
    } catch (error) {
        resultsContainer.innerHTML = '<p class="text-danger">Erreur lors de la recherche</p>';
    }
}

// Afficher les résultats de recherche
function displaySearchResults(results) {
    const container = document.getElementById('searchResults');

    if (!results || results.length === 0) {
        container.innerHTML = '<p class="text-muted">Aucun résultat trouvé</p>';
        return;
    }

    container.innerHTML = results.map(person => `
        <div class="search-result-item" data-person-id="${person.id}">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h5>${person.firstName} ${person.lastName}</h5>
                    <p class="mb-1">
                        ${person.birthDate ? `Né(e) le ${formatDate(person.birthDate)}` : ''}
                        ${person.birthPlace ? `à ${person.birthPlace}` : ''}
                    </p>
                    ${person.deathDate ? `
                        <p class="mb-1">
                            Décédé(e) le ${formatDate(person.deathDate)}
                            ${person.deathPlace ? `à ${person.deathPlace}` : ''}
                        </p>
                    ` : ''}
                    <div class="mt-2">
                        ${person.father ? `<span class="badge bg-secondary">Père: ${person.father.name}</span>` : ''}
                        ${person.mother ? `<span class="badge bg-secondary">Mère: ${person.mother.name}</span>` : ''}
                        ${person.spouse ? `<span class="badge bg-info">Conjoint: ${person.spouse.name}</span>` : ''}
                    </div>
                </div>
                <div class="btn-group-vertical">
                    <button class="btn btn-sm btn-outline-primary" onclick="viewPerson('${person.id}')">
                        <i class="bi bi-eye"></i> Voir
                    </button>
                    <button class="btn btn-sm btn-outline-success" onclick="viewTree('${person.id}')">
                        <i class="bi bi-diagram-3"></i> Arbre
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Voir une personne
async function viewPerson(personId) {
    try {
        const person = await api.getPerson(personId);
        showPersonModal(person);
    } catch (error) {
        showToast('Erreur lors du chargement de la personne', 'error');
    }
}

// Afficher l'arbre d'une personne
async function viewTree(personId) {
    navigateToPage('tree');
    document.getElementById('treePersonSelect').value = personId;
    await generateTree();
}

// Charger les données de l'arbre
async function loadTreeData() {
    try {
        const persons = await api.searchPersons({});
        const select = document.getElementById('treePersonSelect');

        select.innerHTML = '<option value="">Sélectionner une personne...</option>' +
            persons.map(p => `<option value="${p.id}">${p.firstName} ${p.lastName}</option>`).join('');
    } catch (error) {
        console.error('Erreur lors du chargement des personnes:', error);
    }
}

// Générer l'arbre
document.getElementById('generateTreeBtn').addEventListener('click', generateTree);

async function generateTree() {
    const personId = document.getElementById('treePersonSelect').value;
    const generations = document.getElementById('treeGenerations').value;
    const type = document.querySelector('.btn-group .btn.active')?.textContent.toLowerCase() || 'full';

    if (!personId) {
        showToast('Veuillez sélectionner une personne', 'warning');
        return;
    }

    const container = document.getElementById('treeContainer');
    container.innerHTML = '<div class="spinner-container"><div class="spinner-border text-primary"></div></div>';

    try {
        const treeData = await api.getTree(personId, type, generations);
        renderTree(treeData);
    } catch (error) {
        container.innerHTML = '<p class="text-danger text-center">Erreur lors du chargement de l\'arbre</p>';
    }
}

// Rendre l'arbre généalogique
function renderTree(treeData) {
    const container = document.getElementById('treeContainer');
    container.innerHTML = '';

    // Implémentation simplifiée de l'affichage de l'arbre
    // Dans un cas réel, utiliser une librairie comme D3.js ou vis.js
    const centerX = container.offsetWidth / 2;
    const centerY = container.offsetHeight / 2;

    // Créer le nœud central
    const centralNode = createTreeNode(treeData.root, centerX - 75, centerY - 30);
    container.appendChild(centralNode);

    // Ajouter les ancêtres et descendants
    // Cette partie nécessiterait une implémentation plus complexe
}

// Créer un nœud d'arbre
function createTreeNode(person, x, y) {
    const node = document.createElement('div');
    node.className = 'tree-node';
    node.style.left = `${x}px`;
    node.style.top = `${y}px`;
    node.innerHTML = `
        <h6>${person.firstName} ${person.lastName}</h6>
        <small>${person.birthYear || '?'} - ${person.deathYear || ''}</small>
    `;
    node.onclick = () => viewPerson(person.id);
    return node;
}

// Charger les statistiques
async function loadStatistics() {
    try {
        const stats = await api.getStatistics();

        // Mettre à jour les cartes de statistiques
        document.getElementById('totalPersonsStat').textContent = stats.totalPersons || '0';
        document.getElementById('totalFamiliesStat').textContent = stats.totalFamilies || '0';
        document.getElementById('avgChildrenStat').textContent = (stats.avgChildren || 0).toFixed(1);
        document.getElementById('maxGenerationsStat').textContent = stats.maxGenerations || '0';

        // Créer les graphiques
        createCenturyChart(stats.centuryDistribution);
        createSurnameChart(stats.topSurnames);
    } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error);
    }
}

// Créer le graphique de répartition par siècle
function createCenturyChart(data) {
    const ctx = document.getElementById('centuryChart').getContext('2d');

    if (!data) {
        // Données de démonstration
        data = {
            '18ème': 12,
            '19ème': 45,
            '20ème': 120,
            '21ème': 23
        };
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Nombre de personnes',
                data: Object.values(data),
                backgroundColor: 'rgba(13, 110, 253, 0.5)',
                borderColor: 'rgba(13, 110, 253, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Créer le graphique des noms de famille
function createSurnameChart(data) {
    const ctx = document.getElementById('surnameChart').getContext('2d');

    if (!data) {
        // Données de démonstration
        data = {
            'Martin': 15,
            'Bernard': 12,
            'Dubois': 10,
            'Thomas': 8,
            'Robert': 7
        };
    }

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: [
                    'rgba(13, 110, 253, 0.8)',
                    'rgba(25, 135, 84, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(220, 53, 69, 0.8)',
                    'rgba(108, 117, 125, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Gestion de l'authentification
document.getElementById('loginBtn').addEventListener('click', () => {
    const modal = new bootstrap.Modal(document.getElementById('loginModal'));
    modal.show();
});

document.getElementById('registerBtn').addEventListener('click', () => {
    const modal = new bootstrap.Modal(document.getElementById('registerModal'));
    modal.show();
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await api.login(email, password);
        AppState.user = response.user;
        AppState.token = response.token;

        updateUserInterface(response.user);
        bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
        showToast('Connexion réussie!', 'success');

        // Recharger les données
        await loadPageData(AppState.currentPage);
    } catch (error) {
        showToast('Échec de la connexion', 'error');
    }
});

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const passwordConfirm = document.getElementById('registerPasswordConfirm').value;

    if (password !== passwordConfirm) {
        showToast('Les mots de passe ne correspondent pas', 'error');
        return;
    }

    try {
        await api.register(name, email, password);
        bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
        showToast('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success');
    } catch (error) {
        showToast('Échec de l\'inscription', 'error');
    }
});

document.getElementById('logoutBtn').addEventListener('click', async () => {
    try {
        await api.logout();
        AppState.user = null;
        AppState.token = null;
        updateUserInterface(null);
        showToast('Déconnexion réussie', 'info');
    } catch (error) {
        console.error('Erreur lors de la déconnexion:', error);
    }
});

// Mettre à jour l'interface utilisateur
function updateUserInterface(user) {
    const username = document.getElementById('username');
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const profileBtn = document.getElementById('profileBtn');
    const settingsBtn = document.getElementById('settingsBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const userDivider = document.getElementById('userDivider');

    if (user) {
        username.textContent = user.name;
        loginBtn.parentElement.style.display = 'none';
        registerBtn.parentElement.style.display = 'none';
        userDivider.classList.remove('d-none');
        profileBtn.classList.remove('d-none');
        settingsBtn.classList.remove('d-none');
        logoutBtn.classList.remove('d-none');
    } else {
        username.textContent = 'Invité';
        loginBtn.parentElement.style.display = 'block';
        registerBtn.parentElement.style.display = 'block';
        userDivider.classList.add('d-none');
        profileBtn.classList.add('d-none');
        settingsBtn.classList.add('d-none');
        logoutBtn.classList.add('d-none');
    }
}

// Afficher un toast
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toastId = `toast-${Date.now()}`;

    const toastHTML = `
        <div id="${toastId}" class="toast ${type}" role="alert">
            <div class="toast-header">
                <i class="bi ${getToastIcon(type)} me-2"></i>
                <strong class="me-auto">${getToastTitle(type)}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });
    toast.show();

    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Obtenir l'icône du toast
function getToastIcon(type) {
    const icons = {
        'success': 'bi-check-circle-fill text-success',
        'error': 'bi-x-circle-fill text-danger',
        'warning': 'bi-exclamation-triangle-fill text-warning',
        'info': 'bi-info-circle-fill text-info'
    };
    return icons[type] || icons.info;
}

// Obtenir le titre du toast
function getToastTitle(type) {
    const titles = {
        'success': 'Succès',
        'error': 'Erreur',
        'warning': 'Avertissement',
        'info': 'Information'
    };
    return titles[type] || titles.info;
}

// Formater une date
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR');
}

// Formater le temps écoulé
function formatTimeAgo(timestamp) {
    const now = new Date();
    const date = new Date(timestamp);
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return 'À l\'instant';
    if (seconds < 3600) return `Il y a ${Math.floor(seconds / 60)} minutes`;
    if (seconds < 86400) return `Il y a ${Math.floor(seconds / 3600)} heures`;
    if (seconds < 604800) return `Il y a ${Math.floor(seconds / 86400)} jours`;
    return formatDate(timestamp);
}

// Gestion de la navigation par clic
document.querySelectorAll('[data-page]').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = e.currentTarget.getAttribute('data-page');
        if (page) {
            navigateToPage(page);
        }
    });
});

// Gestion des boutons de type d'arbre
document.querySelectorAll('#treeTypeAscendant, #treeTypeDescendant, #treeTypeFull').forEach(btn => {
    btn.addEventListener('click', (e) => {
        document.querySelectorAll('.btn-group .btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
    });
});

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', async () => {
    // Vérifier le token existant
    const token = localStorage.getItem('authToken');
    if (token) {
        api.setToken(token);
        // Essayer de récupérer les infos utilisateur
        try {
            const response = await api.request('/auth/me');
            AppState.user = response.user;
            updateUserInterface(response.user);
        } catch (error) {
            // Token invalide, le supprimer
            api.setToken(null);
        }
    }

    // Charger la page d'accueil
    await loadPageData('home');

    // Afficher un message de bienvenue
    showToast('Bienvenue sur AWKWARD LEGACY', 'info');
});

// Export des fonctions pour usage externe
window.viewPerson = viewPerson;
window.viewTree = viewTree;