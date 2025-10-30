// AWKWARD LEGACY - Application JavaScript Complète
// Gestion de toutes les fonctionnalités: API, Consanguinité, Lignées, GEDCOM, etc.

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api',
    TIMEOUT: 10000
};

// État global de l'application
const AppState = {
    user: null,
    token: localStorage.getItem('authToken'),
    currentPage: 'home',
    persons: [],
    families: [],
    statistics: null,
    selectedPerson: null
};

// ============================================================================
// API CLIENT
// ============================================================================

class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (AppState.token) {
            headers['Authorization'] = `Bearer ${AppState.token}`;
        }
        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;

        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...this.getHeaders(),
                    ...options.headers
                }
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Erreur serveur' }));
                throw new Error(error.detail || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            showToast(error.message, 'error');
            throw error;
        }
    }

    // Auth
    async login(email, password) {
        const response = await this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        AppState.token = response.access_token;
        localStorage.setItem('authToken', response.access_token);
        return response;
    }

    async register(full_name, email, password) {
        return await this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ full_name, email, password })
        });
    }

    async logout() {
        await this.request('/auth/logout', { method: 'POST' });
        AppState.token = null;
        localStorage.removeItem('authToken');
    }

    // Persons
    async getPersons(skip = 0, limit = 100) {
        return await this.request(`/persons?skip=${skip}&limit=${limit}`);
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

    async deletePerson(id) {
        return await this.request(`/persons/${id}`, {
            method: 'DELETE'
        });
    }

    async getAncestors(id, generations = 4) {
        return await this.request(`/persons/${id}/ancestors?generations=${generations}`);
    }

    async getDescendants(id, generations = 4) {
        return await this.request(`/persons/${id}/descendants?generations=${generations}`);
    }

    // Families
    async getFamilies(skip = 0, limit = 100) {
        return await this.request(`/families?skip=${skip}&limit=${limit}`);
    }

    // Search
    async search(params) {
        const queryString = new URLSearchParams(params).toString();
        return await this.request(`/search?${queryString}`);
    }

    // Statistics
    async getStatistics() {
        return await this.request('/statistics');
    }

    async getSurnames(limit = 20) {
        return await this.request(`/statistics/names/surnames?limit=${limit}`);
    }

    async getFirstnames(limit = 20) {
        return await this.request(`/statistics/names/firstnames?limit=${limit}`);
    }

    async getTimeline() {
        return await this.request('/statistics/timeline');
    }

    // Health
    async health() {
        return await this.request('/health');
    }
}

const api = new APIClient(CONFIG.API_BASE_URL);

// ============================================================================
// UI UTILITIES
// ============================================================================

function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    const toastId = 'toast-' + Date.now();

    const typeConfig = {
        success: { icon: 'check-circle-fill', bg: 'success' },
        error: { icon: 'exclamation-triangle-fill', bg: 'danger' },
        warning: { icon: 'exclamation-circle-fill', bg: 'warning' },
        info: { icon: 'info-circle-fill', bg: 'info' }
    };

    const config = typeConfig[type] || typeConfig.info;

    const toastHTML = `
        <div id="${toastId}" class="toast toast-custom align-items-center text-bg-${config.bg} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi bi-${config.icon} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { autohide: true, delay: 3000 });
    toast.show();

    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function showLoading(show = true) {
    const spinner = document.getElementById('loadingSpinner');
    spinner.style.display = show ? 'block' : 'none';
}

function navigateToPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Show selected page
    const targetPage = document.getElementById(pageName + 'Page');
    if (targetPage) {
        targetPage.classList.add('active');
        AppState.currentPage = pageName;

        // Update nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelectorAll(`[data-page="${pageName}"]`).forEach(link => {
            link.classList.add('active');
        });

        // Load page content
        loadPageContent(pageName);
    }
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR');
}

function formatRelationship(relationship) {
    const relations = {
        'parent-enfant': 'Parent → Enfant',
        'frères/sœurs': 'Frères/Sœurs',
        'cousins germains': 'Cousins Germains',
        'oncle-tante/neveu-nièce': 'Oncle/Tante ↔ Neveu/Nièce'
    };
    return relations[relationship] || relationship;
}

// ============================================================================
// PAGE LOADERS
// ============================================================================

async function loadPageContent(pageName) {
    switch (pageName) {
        case 'home':
            await loadHomePage();
            break;
        case 'persons':
            await loadPersonsPage();
            break;
        case 'search':
            await loadSearchPage();
            break;
        case 'consanguinity':
            await loadConsanguinityPage();
            break;
        case 'lineages':
            await loadLineagesPage();
            break;
        case 'tree':
            await loadTreePage();
            break;
        case 'stats':
            await loadStatsPage();
            break;
        case 'import':
            await loadImportPage();
            break;
        case 'export':
            await loadExportPage();
            break;
    }
}

async function loadHomePage() {
    try {
        // Load quick stats
        const stats = await api.getStatistics();
        AppState.statistics = stats;

        document.getElementById('statPersons').textContent = stats.total_persons || 0;
        document.getElementById('statFamilies').textContent = stats.total_families || 0;
        document.getElementById('statGenerations').textContent = stats.max_generations || 0;

        const yearRange = stats.oldest_birth_year && stats.newest_birth_year
            ? `${stats.oldest_birth_year}-${stats.newest_birth_year}`
            : '-';
        document.getElementById('statYearRange').textContent = yearRange;

    } catch (error) {
        console.error('Error loading home page:', error);
    }
}

async function loadPersonsPage() {
    const personsPage = document.getElementById('personsPage');
    personsPage.innerHTML = `
        <div class="row">
            <div class="col-lg-11 mx-auto">
                <h2 class="mb-4">
                    <i class="bi bi-person-plus"></i> Gestion des Personnes
                </h2>

                <!-- System Status (3-Layer Cache) -->
                <div class="alert alert-info mb-4">
                    <h6 class="alert-heading">
                        <i class="bi bi-layers"></i> Système à 3 Couches (GeneWeb Pattern)
                    </h6>
                    <div class="row text-center mt-3">
                        <div class="col-md-4">
                            <span class="badge bg-warning fs-6">PENDING</span>
                            <p class="mb-0 mt-2 small">Modifications non committées<br><span id="pendingCount" class="fw-bold">-</span></p>
                        </div>
                        <div class="col-md-4">
                            <span class="badge bg-success fs-6">COMMITTED</span>
                            <p class="mb-0 mt-2 small">Modifications sauvegardées<br><span id="committedCount" class="fw-bold">-</span></p>
                        </div>
                        <div class="col-md-4">
                            <span class="badge bg-secondary fs-6">BASE</span>
                            <p class="mb-0 mt-2 small">Données originales<br><span id="baseCount" class="fw-bold">-</span></p>
                        </div>
                    </div>
                    <div class="text-center mt-3">
                        <button class="btn btn-sm btn-success me-2" id="commitBtn">
                            <i class="bi bi-check-circle"></i> Commit (PENDING → COMMITTED)
                        </button>
                        <button class="btn btn-sm btn-warning" id="rollbackBtn">
                            <i class="bi bi-x-circle"></i> Rollback (Annuler PENDING)
                        </button>
                    </div>
                </div>

                <!-- Create Person Form -->
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-person-plus-fill"></i> Créer une Nouvelle Personne
                        </h5>
                    </div>
                    <div class="card-body">
                        <form id="createPersonForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Prénom <span class="text-danger">*</span></label>
                                    <input type="text" class="form-control" name="first_name" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nom de famille <span class="text-danger">*</span></label>
                                    <input type="text" class="form-control" name="last_name" required>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Date de naissance</label>
                                    <input type="date" class="form-control" name="birth_date">
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Lieu de naissance</label>
                                    <input type="text" class="form-control" name="birth_place">
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Genre <span class="text-danger">*</span></label>
                                    <select class="form-select" name="sex" required>
                                        <option value="">Sélectionner...</option>
                                        <option value="M">Masculin</option>
                                        <option value="F">Féminin</option>
                                        <option value="U">Inconnu</option>
                                    </select>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Date de décès</label>
                                    <input type="date" class="form-control" name="death_date">
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Lieu de décès</label>
                                    <input type="text" class="form-control" name="death_place">
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Profession</label>
                                    <input type="text" class="form-control" name="occupation">
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">ID Père (optionnel)</label>
                                    <input type="text" class="form-control" name="father_id" placeholder="Ex: 0">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">ID Mère (optionnel)</label>
                                    <input type="text" class="form-control" name="mother_id" placeholder="Ex: 1">
                                </div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Notes</label>
                                <textarea class="form-control" name="notes" rows="2"></textarea>
                            </div>

                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <button type="reset" class="btn btn-outline-secondary">
                                    <i class="bi bi-x-circle"></i> Réinitialiser
                                </button>
                                <button type="submit" class="btn btn-primary">
                                    <i class="bi bi-plus-circle"></i> Créer Personne
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <!-- Persons List -->
                <div class="card shadow-sm">
                    <div class="card-header bg-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="bi bi-list-ul"></i> Liste des Personnes
                            <span class="badge bg-primary ms-2" id="personsCount">0</span>
                        </h5>
                        <button class="btn btn-sm btn-outline-primary" id="refreshPersonsBtn">
                            <i class="bi bi-arrow-clockwise"></i> Actualiser
                        </button>
                    </div>
                    <div class="card-body">
                        <div id="personsList">
                            <div class="text-center text-muted py-5">
                                <i class="bi bi-people" style="font-size: 3rem;"></i>
                                <p class="mt-3">Chargement...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Edit Person Modal -->
        <div class="modal fade" id="editPersonModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-warning text-dark">
                        <h5 class="modal-title">
                            <i class="bi bi-pencil-fill"></i> Modifier la Personne
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="editPersonForm">
                            <input type="hidden" name="person_id" id="editPersonId">

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Prénom</label>
                                    <input type="text" class="form-control" name="first_name" id="editFirstName">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nom de famille</label>
                                    <input type="text" class="form-control" name="last_name" id="editLastName">
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Date de naissance</label>
                                    <input type="date" class="form-control" name="birth_date" id="editBirthDate">
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Lieu de naissance</label>
                                    <input type="text" class="form-control" name="birth_place" id="editBirthPlace">
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Genre</label>
                                    <select class="form-select" name="sex" id="editSex">
                                        <option value="M">Masculin</option>
                                        <option value="F">Féminin</option>
                                        <option value="U">Inconnu</option>
                                    </select>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Date de décès</label>
                                    <input type="date" class="form-control" name="death_date" id="editDeathDate">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Lieu de décès</label>
                                    <input type="text" class="form-control" name="death_place" id="editDeathPlace">
                                </div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Notes</label>
                                <textarea class="form-control" name="notes" id="editNotes" rows="2"></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>
                        <button type="button" class="btn btn-warning" id="saveEditBtn">
                            <i class="bi bi-save"></i> Enregistrer
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Event Listeners
    setupPersonsPageEventListeners();

    // Load initial data
    await loadPersonsList();
    await loadSystemStatus();
}

async function setupPersonsPageEventListeners() {
    // Create Person Form
    document.getElementById('createPersonForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const personData = {};

        for (let [key, value] of formData.entries()) {
            if (value) personData[key] = value;
        }

        try {
            showLoading(true);
            const newPerson = await api.createPerson(personData);
            showToast(`Personne créée: ${newPerson.first_name} ${newPerson.last_name} (ID: ${newPerson.id})`, 'success');
            e.target.reset();
            await loadPersonsList();
            await loadSystemStatus();
        } catch (error) {
            console.error('Error creating person:', error);
        } finally {
            showLoading(false);
        }
    });

    // Refresh Button
    document.getElementById('refreshPersonsBtn').addEventListener('click', async () => {
        await loadPersonsList();
        await loadSystemStatus();
        showToast('Liste actualisée', 'info');
    });

    // Commit Button
    document.getElementById('commitBtn').addEventListener('click', async () => {
        if (!confirm('Confirmer le commit des modifications PENDING vers COMMITTED ?')) return;

        try {
            showLoading(true);
            // Note: This would need a backend endpoint for commit
            showToast('Fonctionnalité commit à implémenter côté backend', 'warning');
            await loadSystemStatus();
        } catch (error) {
            console.error('Error committing:', error);
        } finally {
            showLoading(false);
        }
    });

    // Rollback Button
    document.getElementById('rollbackBtn').addEventListener('click', async () => {
        if (!confirm('Confirmer l\'annulation de toutes les modifications PENDING ?')) return;

        try {
            showLoading(true);
            // Note: This would need a backend endpoint for rollback
            showToast('Fonctionnalité rollback à implémenter côté backend', 'warning');
            await loadPersonsList();
            await loadSystemStatus();
        } catch (error) {
            console.error('Error rolling back:', error);
        } finally {
            showLoading(false);
        }
    });

    // Save Edit Button
    document.getElementById('saveEditBtn').addEventListener('click', async () => {
        const personId = document.getElementById('editPersonId').value;
        const formData = new FormData(document.getElementById('editPersonForm'));
        const updateData = {};

        for (let [key, value] of formData.entries()) {
            if (key !== 'person_id' && value) updateData[key] = value;
        }

        try {
            showLoading(true);
            const updated = await api.updatePerson(personId, updateData);
            showToast(`Personne modifiée: ${updated.first_name} ${updated.last_name}`, 'success');
            bootstrap.Modal.getInstance(document.getElementById('editPersonModal')).hide();
            await loadPersonsList();
            await loadSystemStatus();
        } catch (error) {
            console.error('Error updating person:', error);
        } finally {
            showLoading(false);
        }
    });
}

async function loadPersonsList() {
    try {
        const persons = await api.getPersons(0, 100);
        displayPersonsList(persons);
    } catch (error) {
        console.error('Error loading persons:', error);
        document.getElementById('personsList').innerHTML = `
            <div class="alert alert-danger">
                Erreur lors du chargement des personnes
            </div>
        `;
    }
}

function displayPersonsList(persons) {
    const personsListDiv = document.getElementById('personsList');
    const countBadge = document.getElementById('personsCount');

    if (!persons || persons.length === 0) {
        personsListDiv.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="bi bi-inbox" style="font-size: 3rem;"></i>
                <p class="mt-3">Aucune personne trouvée</p>
                <p class="small">Utilisez le formulaire ci-dessus pour créer des personnes</p>
            </div>
        `;
        countBadge.textContent = '0';
        return;
    }

    countBadge.textContent = persons.length;

    const html = `
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nom</th>
                        <th>Prénom</th>
                        <th>Naissance</th>
                        <th>Décès</th>
                        <th>Lieu</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${persons.map(person => `
                        <tr>
                            <td><code>${person.id}</code></td>
                            <td><strong>${person.last_name || '-'}</strong></td>
                            <td>${person.first_name || '-'}</td>
                            <td>${person.birth_date ? formatDate(person.birth_date) : '-'}</td>
                            <td>${person.death_date ? formatDate(person.death_date) : '—'}</td>
                            <td>${person.birth_place || '-'}</td>
                            <td>
                                <button class="btn btn-sm btn-outline-warning" onclick="editPerson('${person.id}')">
                                    <i class="bi bi-pencil"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger" onclick="deletePerson('${person.id}', '${person.first_name} ${person.last_name}')">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;

    personsListDiv.innerHTML = html;
}

async function loadSystemStatus() {
    try {
        const stats = await api.getStatistics();

        document.getElementById('pendingCount').textContent = stats.pending_modifications || 0;
        document.getElementById('committedCount').textContent = stats.committed_modifications || 0;
        document.getElementById('baseCount').textContent = stats.base_persons || 0;
    } catch (error) {
        console.error('Error loading system status:', error);
    }
}

// Global helper functions for person management
window.editPerson = async (id) => {
    try {
        const person = await api.getPerson(id);

        document.getElementById('editPersonId').value = person.id;
        document.getElementById('editFirstName').value = person.first_name || '';
        document.getElementById('editLastName').value = person.last_name || '';
        document.getElementById('editBirthDate').value = person.birth_date || '';
        document.getElementById('editBirthPlace').value = person.birth_place || '';
        document.getElementById('editSex').value = person.sex || 'U';
        document.getElementById('editDeathDate').value = person.death_date || '';
        document.getElementById('editDeathPlace').value = person.death_place || '';
        document.getElementById('editNotes').value = person.notes || '';

        const modal = new bootstrap.Modal(document.getElementById('editPersonModal'));
        modal.show();
    } catch (error) {
        showToast('Erreur lors du chargement de la personne', 'error');
    }
};

window.deletePerson = async (id, name) => {
    if (!confirm(`Êtes-vous sûr de vouloir supprimer ${name} (ID: ${id}) ?`)) return;

    try {
        showLoading(true);
        await api.deletePerson(id);
        showToast(`Personne supprimée: ${name}`, 'success');
        await loadPersonsList();
        await loadSystemStatus();
    } catch (error) {
        console.error('Error deleting person:', error);
    } finally {
        showLoading(false);
    }
};

async function loadSearchPage() {
    const searchPage = document.getElementById('searchPage');
    searchPage.innerHTML = `
        <div class="row">
            <div class="col-lg-10 mx-auto">
                <h2 class="mb-4">
                    <i class="bi bi-search"></i> Recherche Avancée
                </h2>

                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <form id="advancedSearchForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Prénom</label>
                                    <input type="text" class="form-control" name="first_name" placeholder="Jean">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nom de famille</label>
                                    <input type="text" class="form-control" name="last_name" placeholder="Martin">
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Année de naissance (min)</label>
                                    <input type="number" class="form-control" name="birth_year_min" placeholder="1900">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Année de naissance (max)</label>
                                    <input type="number" class="form-control" name="birth_year_max" placeholder="2000">
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Lieu de naissance</label>
                                    <input type="text" class="form-control" name="birth_place" placeholder="Paris">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Genre</label>
                                    <select class="form-select" name="gender">
                                        <option value="">Tous</option>
                                        <option value="M">Masculin</option>
                                        <option value="F">Féminin</option>
                                    </select>
                                </div>
                            </div>

                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <button type="reset" class="btn btn-outline-secondary">
                                    <i class="bi bi-x-circle"></i> Réinitialiser
                                </button>
                                <button type="submit" class="btn btn-primary">
                                    <i class="bi bi-search"></i> Rechercher
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <div class="card shadow-sm">
                    <div class="card-header bg-white">
                        <h5 class="mb-0">
                            <i class="bi bi-list-ul"></i> Résultats
                            <span class="badge bg-primary ms-2" id="searchResultCount">0</span>
                        </h5>
                    </div>
                    <div class="card-body">
                        <div id="searchResults">
                            <div class="text-center text-muted py-5">
                                <i class="bi bi-search" style="font-size: 3rem;"></i>
                                <p class="mt-3">Utilisez les filtres ci-dessus pour rechercher</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Event listener
    document.getElementById('advancedSearchForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const params = {};

        for (let [key, value] of formData.entries()) {
            if (value) params[key] = value;
        }

        try {
            showLoading(true);
            const results = await api.search(params);
            displaySearchResults(results);
        } catch (error) {
            console.error('Search error:', error);
        } finally {
            showLoading(false);
        }
    });
}

function displaySearchResults(results) {
    const resultsDiv = document.getElementById('searchResults');
    const countBadge = document.getElementById('searchResultCount');

    countBadge.textContent = results.total || 0;

    if (!results.results || results.results.length === 0) {
        resultsDiv.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="bi bi-inbox" style="font-size: 3rem;"></i>
                <p class="mt-3">Aucun résultat trouvé</p>
            </div>
        `;
        return;
    }

    const html = results.results.map(person => `
        <div class="card person-card mb-3">
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h5 class="card-title mb-2">
                            <i class="bi bi-person-fill"></i>
                            ${person.first_name} ${person.last_name}
                        </h5>
                        <p class="card-text text-muted mb-1">
                            <i class="bi bi-calendar"></i>
                            ${person.birth_date ? formatDate(person.birth_date) : '?'} -
                            ${person.death_date ? formatDate(person.death_date) : 'Vivant'}
                        </p>
                        ${person.birth_place ? `
                            <p class="card-text text-muted mb-0">
                                <i class="bi bi-geo-alt"></i> ${person.birth_place}
                            </p>
                        ` : ''}
                    </div>
                    <div class="col-md-4 text-md-end">
                        <button class="btn btn-sm btn-outline-primary" onclick="viewPersonDetails('${person.id}')">
                            <i class="bi bi-eye"></i> Détails
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');

    resultsDiv.innerHTML = html;
}

async function loadConsanguinityPage() {
    const page = document.getElementById('consanguinityPage');
    page.innerHTML = `
        <div class="row">
            <div class="col-lg-10 mx-auto">
                <h2 class="mb-4">
                    <i class="bi bi-dna"></i> Calculateur de Consanguinité
                </h2>

                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    <strong>Note:</strong> Le calcul de consanguinité nécessite l'intégration backend Python.
                    Cette fonctionnalité sera bientôt disponible via l'API.
                </div>

                <div class="card shadow-sm mb-4">
                    <div class="card-body">
                        <h5 class="card-title">Calculer le coefficient de parenté</h5>
                        <form id="kinshipForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Personne 1 (ID)</label>
                                    <input type="text" class="form-control" name="person1" placeholder="I1" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Personne 2 (ID)</label>
                                    <input type="text" class="form-control" name="person2" placeholder="I2" required>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-calculator"></i> Calculer
                            </button>
                        </form>

                        <div id="kinshipResult" class="mt-4" style="display: none;">
                            <div class="alert alert-success">
                                <h6>Résultat:</h6>
                                <p class="mb-1"><strong>Coefficient de parenté:</strong> <span id="kinshipCoeff">-</span></p>
                                <p class="mb-0"><strong>Relation:</strong> <span id="kinshipRelation">-</span></p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card shadow-sm">
                    <div class="card-header bg-white">
                        <h5 class="mb-0">Coefficients de référence</h5>
                    </div>
                    <div class="card-body">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Relation</th>
                                    <th>Coefficient (φ)</th>
                                    <th>Consanguinité (F)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Parent-Enfant</td>
                                    <td>0.25</td>
                                    <td>0</td>
                                </tr>
                                <tr>
                                    <td>Frères/Sœurs</td>
                                    <td>0.25</td>
                                    <td>0</td>
                                </tr>
                                <tr>
                                    <td>Cousins Germains</td>
                                    <td>0.0625</td>
                                    <td>0</td>
                                </tr>
                                <tr>
                                    <td>Enfant de Frères/Sœurs</td>
                                    <td>-</td>
                                    <td>0.25</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Event listener (simulated for now)
    document.getElementById('kinshipForm').addEventListener('submit', (e) => {
        e.preventDefault();
        showToast('Fonctionnalité en cours d\'intégration avec l\'API', 'warning');
    });
}

async function loadLineagesPage() {
    const page = document.getElementById('lineagesPage');
    page.innerHTML = `
        <div class="row">
            <div class="col-lg-10 mx-auto">
                <h2 class="mb-4">
                    <i class="bi bi-diagram-3"></i> Analyse des Lignées
                </h2>

                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    <strong>Note:</strong> L'analyse de lignées nécessite l'intégration backend Python.
                    Cette fonctionnalité sera bientôt disponible via l'API.
                </div>

                <div class="row">
                    <div class="col-md-4 mb-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-primary" id="lineageCount">-</h3>
                                <p class="text-muted mb-0">Lignées Distinctes</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-success" id="largestLineage">-</h3>
                                <p class="text-muted mb-0">Plus Grande Lignée</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <div class="card text-center">
                            <div class="card-body">
                                <h3 class="text-warning" id="isolatedCount">-</h3>
                                <p class="text-muted mb-0">Personnes Isolées</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card shadow-sm">
                    <div class="card-header bg-white">
                        <h5 class="mb-0">Liste des Lignées</h5>
                    </div>
                    <div class="card-body">
                        <div id="lineagesList">
                            <div class="text-center text-muted py-5">
                                <i class="bi bi-diagram-3" style="font-size: 3rem;"></i>
                                <p class="mt-3">Chargement des lignées...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

async function loadStatsPage() {
    const page = document.getElementById('statsPage');
    page.innerHTML = `
        <div class="row">
            <div class="col-lg-10 mx-auto">
                <h2 class="mb-4">
                    <i class="bi bi-bar-chart"></i> Statistiques
                </h2>

                <div class="row" id="statCards">
                    <!-- Stats will be loaded here -->
                </div>

                <div class="row">
                    <div class="col-md-6 mb-4">
                        <div class="card shadow-sm">
                            <div class="card-header bg-white">
                                <h5 class="mb-0">Top 10 Noms de Famille</h5>
                            </div>
                            <div class="card-body">
                                <canvas id="surnamesChart"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <div class="card shadow-sm">
                            <div class="card-header bg-white">
                                <h5 class="mb-0">Distribution par Siècle</h5>
                            </div>
                            <div class="card-body">
                                <canvas id="centuryChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    try {
        showLoading(true);
        const stats = await api.getStatistics();
        displayStatistics(stats);
    } catch (error) {
        console.error('Error loading stats:', error);
    } finally {
        showLoading(false);
    }
}

function displayStatistics(stats) {
    // Display stat cards
    const statCardsHTML = `
        <div class="col-md-3 mb-3">
            <div class="card stat-card text-center">
                <i class="bi bi-people-fill" style="font-size: 2rem;"></i>
                <div class="stat-number">${stats.total_persons || 0}</div>
                <div>Personnes</div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card stat-card text-center">
                <i class="bi bi-heart-fill" style="font-size: 2rem;"></i>
                <div class="stat-number">${stats.total_families || 0}</div>
                <div>Familles</div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card stat-card text-center">
                <i class="bi bi-gender-male" style="font-size: 2rem;"></i>
                <div class="stat-number">${stats.total_males || 0}</div>
                <div>Hommes</div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card stat-card text-center">
                <i class="bi bi-gender-female" style="font-size: 2rem;"></i>
                <div class="stat-number">${stats.total_females || 0}</div>
                <div>Femmes</div>
            </div>
        </div>
    `;
    document.getElementById('statCards').innerHTML = statCardsHTML;

    // Chart: Surnames
    if (stats.top_surnames && stats.top_surnames.length > 0) {
        const surnamesCtx = document.getElementById('surnamesChart').getContext('2d');
        new Chart(surnamesCtx, {
            type: 'bar',
            data: {
                labels: stats.top_surnames.map(s => s.name),
                datasets: [{
                    label: 'Occurrences',
                    data: stats.top_surnames.map(s => s.count),
                    backgroundColor: 'rgba(52, 152, 219, 0.8)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Chart: Century distribution
    if (stats.century_distribution && stats.century_distribution.length > 0) {
        const centuryCtx = document.getElementById('centuryChart').getContext('2d');
        new Chart(centuryCtx, {
            type: 'line',
            data: {
                labels: stats.century_distribution.map(c => c.century),
                datasets: [{
                    label: 'Naissances',
                    data: stats.century_distribution.map(c => c.count),
                    borderColor: 'rgba(46, 204, 113, 1)',
                    backgroundColor: 'rgba(46, 204, 113, 0.2)',
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
}

async function loadImportPage() {
    const page = document.getElementById('importPage');
    page.innerHTML = `
        <div class="row">
            <div class="col-lg-8 mx-auto">
                <h2 class="mb-4">
                    <i class="bi bi-upload"></i> Importer GEDCOM
                </h2>

                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Sélectionner un fichier GEDCOM</h5>
                        <p class="text-muted">
                            Le format GEDCOM est le standard pour l'échange de données généalogiques.
                            Vous pouvez importer des fichiers depuis Family Tree Maker, Ancestry.com, etc.
                        </p>

                        <form id="gedcomImportForm">
                            <div class="mb-3">
                                <label class="form-label">Fichier GEDCOM (.ged)</label>
                                <input type="file" class="form-control" accept=".ged" id="gedcomFile" required>
                            </div>

                            <div class="form-check mb-3">
                                <input class="form-check-input" type="checkbox" id="showStats" checked>
                                <label class="form-check-label" for="showStats">
                                    Afficher les statistiques après import
                                </label>
                            </div>

                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-upload"></i> Importer
                            </button>
                        </form>

                        <div id="importProgress" class="mt-4" style="display: none;">
                            <div class="progress">
                                <div class="progress-bar progress-bar-striped progress-bar-animated"
                                     role="progressbar" style="width: 100%"></div>
                            </div>
                            <p class="text-center mt-2">Import en cours...</p>
                        </div>

                        <div id="importResult" class="mt-4" style="display: none;"></div>
                    </div>
                </div>

                <div class="card shadow-sm mt-4">
                    <div class="card-header bg-white">
                        <h5 class="mb-0">Utilisation CLI</h5>
                    </div>
                    <div class="card-body">
                        <p>Vous pouvez également importer via la ligne de commande:</p>
                        <pre class="bg-dark text-light p-3 rounded"><code>./modernProject/bin/ged2gwb.py family.ged output_db --verbose --stats</code></pre>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.getElementById('gedcomImportForm').addEventListener('submit', (e) => {
        e.preventDefault();
        showToast('Import GEDCOM via frontend en développement. Utilisez le CLI pour l\'instant.', 'info');
    });
}

async function loadExportPage() {
    const page = document.getElementById('exportPage');
    page.innerHTML = `
        <div class="row">
            <div class="col-lg-8 mx-auto">
                <h2 class="mb-4">
                    <i class="bi bi-download"></i> Exporter GEDCOM
                </h2>

                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">Exporter la base de données</h5>
                        <p class="text-muted">
                            Exportez toutes vos données au format GEDCOM pour les utiliser dans d'autres logiciels.
                        </p>

                        <form id="gedcomExportForm">
                            <div class="mb-3">
                                <label class="form-label">Nom du fichier</label>
                                <input type="text" class="form-control" value="export_${new Date().toISOString().split('T')[0]}.ged" required>
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Format</label>
                                <select class="form-select">
                                    <option value="5.5.1">GEDCOM 5.5.1 (Recommandé)</option>
                                    <option value="5.5">GEDCOM 5.5</option>
                                </select>
                            </div>

                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-download"></i> Exporter
                            </button>
                        </form>
                    </div>
                </div>

                <div class="card shadow-sm mt-4">
                    <div class="card-header bg-white">
                        <h5 class="mb-0">Utilisation CLI</h5>
                    </div>
                    <div class="card-body">
                        <p>Vous pouvez également exporter via la ligne de commande:</p>
                        <pre class="bg-dark text-light p-3 rounded"><code>./modernProject/bin/gwb2ged.py input_db export.ged --verbose</code></pre>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.getElementById('gedcomExportForm').addEventListener('submit', (e) => {
        e.preventDefault();
        showToast('Export GEDCOM via frontend en développement. Utilisez le CLI pour l\'instant.', 'info');
    });
}

async function loadTreePage() {
    const page = document.getElementById('treePage');
    page.innerHTML = `
        <div class="row">
            <div class="col-12">
                <h2 class="mb-4">
                    <i class="bi bi-diagram-2"></i> Arbre Généalogique
                </h2>

                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    La visualisation d'arbres interactifs avec D3.js sera implémentée prochainement.
                </div>

                <div class="card shadow-sm">
                    <div class="card-body text-center py-5">
                        <i class="bi bi-diagram-2" style="font-size: 5rem; color: #ccc;"></i>
                        <h4 class="mt-3">Visualisation en cours de développement</h4>
                        <p class="text-muted">
                            L'arbre généalogique interactif utilisera D3.js pour une visualisation dynamique.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('AWKWARD LEGACY - Initializing...');

    // Check API health
    try {
        const health = await api.health();
        console.log('API Health:', health);
        showToast('Connexion à l\'API réussie', 'success');
    } catch (error) {
        console.error('API Health check failed:', error);
        showToast('Impossible de se connecter à l\'API. Assurez-vous que le serveur est démarré.', 'error');
    }

    // Navigation event listeners
    document.querySelectorAll('[data-page]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const pageName = e.currentTarget.getAttribute('data-page');
            navigateToPage(pageName);
        });
    });

    // Quick search form
    document.getElementById('quickSearchForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = document.getElementById('quickSearchInput').value;

        try {
            showLoading(true);
            const results = await api.search({ query, limit: 10 });

            if (results.total > 0) {
                navigateToPage('search');
                setTimeout(() => displaySearchResults(results), 100);
            } else {
                showToast('Aucun résultat trouvé', 'warning');
            }
        } catch (error) {
            console.error('Search error:', error);
        } finally {
            showLoading(false);
        }
    });

    // Auth buttons
    document.getElementById('loginBtn').addEventListener('click', () => {
        showToast('Fonctionnalité d\'authentification en développement', 'info');
    });

    document.getElementById('registerBtn').addEventListener('click', () => {
        showToast('Fonctionnalité d\'inscription en développement', 'info');
    });

    // Load initial page
    await loadHomePage();

    console.log('AWKWARD LEGACY - Ready!');
});

// Expose global functions
window.navigateToPage = navigateToPage;
window.viewPersonDetails = async (id) => {
    try {
        const person = await api.getPerson(id);
        alert(`Détails de ${person.first_name} ${person.last_name}\nFonctionnalité complète à venir`);
    } catch (error) {
        showToast('Erreur lors du chargement des détails', 'error');
    }
};
