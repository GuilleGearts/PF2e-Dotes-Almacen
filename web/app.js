let allFeats = [];
let filteredFeats = [];
const RENDER_LIMIT = 50;
let currentRenderCount = 0;

// DOM Elements
const searchInput = document.getElementById('search-input');
const specificTraitFilter = document.getElementById('specific-trait-filter');
const categoryFiltersContainer = document.getElementById('category-filters');
const levelFilter = document.getElementById('level-filter');
const featsGrid = document.getElementById('feats-grid');
const resultsCount = document.getElementById('results-count');
const clearFiltersBtn = document.getElementById('clear-filters');
const themeSelector = document.getElementById('theme-selector');
const languageSelector = document.getElementById('language-selector');

// State
const state = {
    searchQuery: '',
    selectedSpecificTrait: '',
    selectedCategories: new Set(),
    selectedLevel: '',
    language: 'en'
};

// Initialize
async function init() {
    try {
        // Load Theme and Language
        const savedTheme = localStorage.getItem('pf2e-theme') || 'pf2e';
        document.documentElement.setAttribute('data-theme', savedTheme);
        themeSelector.value = savedTheme;

        const savedLanguage = localStorage.getItem('pf2e-lang') || 'en';
        state.language = savedLanguage;
        languageSelector.value = savedLanguage;

        const response = await fetch('feats_data.json?v=' + Date.now());
        if (!response.ok) throw new Error('Failed to load feats data');
        const data = await response.json();
        
        allFeats = Object.values(data).sort((a, b) => a.en.name.localeCompare(b.en.name));
        filteredFeats = [...allFeats];
        
        buildFilters();
        renderFeats(true);
        setupEventListeners();
        
    } catch (error) {
        featsGrid.innerHTML = `<div class="loader">Error loading feats: ${error.message}</div>`;
    }
}

function buildFilters() {
    const categories = new Set();
    const levels = new Set();
    const traits = new Set();

    allFeats.forEach(feat => {
        if (feat.category) categories.add(feat.category);
        if (feat.level !== undefined && feat.level !== null) levels.add(feat.level);
        if (feat.traits && Array.isArray(feat.traits)) {
            feat.traits.forEach(t => traits.add(t));
        }
    });

    // Render Categories
    Array.from(categories).sort().forEach(cat => {
        const label = document.createElement('label');
        label.className = 'checkbox-label';
        label.innerHTML = `<input type="checkbox" value="${cat}" class="cat-cb"> ${formatTrait(cat)}`;
        categoryFiltersContainer.appendChild(label);
    });

    // Render Levels
    Array.from(levels).sort((a, b) => a - b).forEach(lvl => {
        const option = document.createElement('option');
        option.value = lvl;
        option.textContent = `Level ${lvl}`;
        levelFilter.appendChild(option);
    });

    // Render Specific Traits (Dropdown)
    Array.from(traits).sort().forEach(trait => {
        const option = document.createElement('option');
        option.value = trait;
        option.textContent = formatTrait(trait);
        specificTraitFilter.appendChild(option);
    });
}

function setupEventListeners() {
    themeSelector.addEventListener('change', (e) => {
        const theme = e.target.value;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('pf2e-theme', theme);
    });

    languageSelector.addEventListener('change', (e) => {
        state.language = e.target.value;
        localStorage.setItem('pf2e-lang', state.language);
        applyFilters(); // Re-render and re-filter using new language
    });

    searchInput.addEventListener('input', (e) => {
        state.searchQuery = e.target.value.toLowerCase();
        applyFilters();
    });

    specificTraitFilter.addEventListener('change', (e) => {
        state.selectedSpecificTrait = e.target.value;
        applyFilters();
    });

    levelFilter.addEventListener('change', (e) => {
        state.selectedLevel = e.target.value;
        applyFilters();
    });

    document.querySelector('.sidebar').addEventListener('change', (e) => {
        if (e.target.classList.contains('cat-cb')) {
            if (e.target.checked) state.selectedCategories.add(e.target.value);
            else state.selectedCategories.delete(e.target.value);
            applyFilters();
        }
    });

    clearFiltersBtn.addEventListener('click', () => {
        state.searchQuery = '';
        state.selectedCategories.clear();
        state.selectedLevel = '';
        state.selectedSpecificTrait = '';
        
        searchInput.value = '';
        levelFilter.value = '';
        specificTraitFilter.value = '';
        
        document.querySelectorAll('.cat-cb').forEach(cb => cb.checked = false);
        
        applyFilters();
    });
    
    window.addEventListener('scroll', () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
            if (currentRenderCount < filteredFeats.length) {
                renderMoreFeats();
            }
        }
    });
}

function applyFilters() {
    filteredFeats = allFeats.filter(feat => {
        // Obtenemos los textos en el idioma seleccionado, con fallback a inglés
        const langData = (state.language === 'es' && feat.es && feat.es.name) ? feat.es : feat.en;
        
        if (state.searchQuery) {
            const nameMatch = langData.name.toLowerCase().includes(state.searchQuery);
            const descMatch = langData.description.toLowerCase().includes(state.searchQuery);
            if (!nameMatch && !descMatch) return false;
        }

        if (state.selectedCategories.size > 0 && !state.selectedCategories.has(feat.category)) {
            return false;
        }

        if (state.selectedLevel !== '' && feat.level.toString() !== state.selectedLevel) {
            return false;
        }

        if (state.selectedSpecificTrait !== '') {
            if (!feat.traits || !feat.traits.includes(state.selectedSpecificTrait)) return false;
        }

        return true;
    });

    renderFeats(true);
}

function formatTrait(trait) {
    if (!trait) return '';
    return trait.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

function getTraitColorClass(trait) {
    const t = trait.toLowerCase();
    if (t === 'general') return 'trait-general';
    if (t === 'skill') return 'trait-skill';
    if (t.includes('class') || t === 'archetype') return 'trait-class';
    if (t === 'ancestry' || t === 'heritage') return 'trait-ancestry';
    return '';
}

function createFeatCard(feat) {
    const card = document.createElement('article');
    card.className = 'feat-card';
    
    const rarity = feat.rarity || 'common';
    const rarityBadge = rarity !== 'common' ? `<span class="trait-badge rarity-${rarity}">${formatTrait(rarity)}</span>` : '';
    
    const traitsHtml = (feat.traits || []).map(t => 
        `<span class="trait-badge ${getTraitColorClass(t)}">${formatTrait(t)}</span>`
    ).join('');

    // Obtener los datos del idioma seleccionado, con fallback a inglés
    const langData = (state.language === 'es' && feat.es && feat.es.name) ? feat.es : feat.en;
    
    // Si estamos en español y el nombre viene del inglés (por falta de traducción), añadimos un indicador visual
    const isUntranslated = (state.language === 'es' && (!feat.es || !feat.es.name));
    const untranslatedBadge = isUntranslated ? `<span class="trait-badge" style="background:#ffeb3b;color:#333;border-color:#fbc02d;" title="No traducido aún">EN</span>` : '';

    card.innerHTML = `
        <div class="feat-header">
            <h2 class="feat-title">${langData.name} ${untranslatedBadge}</h2>
            <span class="feat-level">Level ${feat.level}</span>
        </div>
        <div class="feat-meta">
            <span class="publication">${feat.publication ? 'Source: ' + feat.publication : ''}</span>
        </div>
        <div class="feat-traits">
            ${rarityBadge}
            ${traitsHtml}
        </div>
        <div class="feat-desc">
            ${langData.description}
        </div>
    `;
    return card;
}

function renderFeats(reset = false) {
    if (reset) {
        featsGrid.innerHTML = '';
        currentRenderCount = 0;
        window.scrollTo(0, 0);
    }

    resultsCount.textContent = `Showing ${filteredFeats.length} feats`;

    if (filteredFeats.length === 0) {
        featsGrid.innerHTML = '<div class="loader">No feats match your filters.</div>';
        return;
    }

    renderMoreFeats();
}

function renderMoreFeats() {
    const fragment = document.createDocumentFragment();
    const end = Math.min(currentRenderCount + RENDER_LIMIT, filteredFeats.length);
    
    for (let i = currentRenderCount; i < end; i++) {
        fragment.appendChild(createFeatCard(filteredFeats[i]));
    }
    
    featsGrid.appendChild(fragment);
    currentRenderCount = end;
}

document.addEventListener('DOMContentLoaded', init);
