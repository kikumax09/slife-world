// Animation des compteurs
document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const current = +counter.innerText;
            const increment = target / 100;
            if (current < target) {
                counter.innerText = Math.ceil(current + increment);
                setTimeout(updateCount, 20);
            } else {
                counter.innerText = target;
            }
        };
        updateCount();
    });

    // Toggle menu mobile
document.querySelector('.menu-toggle')?.addEventListener('click', function() {
    document.querySelector('.nav-menu')?.classList.toggle('active');
});

// Fermer le menu après un clic sur un lien (optionnel)
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        document.querySelector('.nav-menu')?.classList.remove('active');
    });
});

    // Exemple de chargement équipe (à adapter)
    const teamGrid = document.getElementById('teamGrid');
    if (teamGrid) {
        teamGrid.innerHTML = '<p>Équipe à venir...</p>';
    }
});

// Filtrage des publications
const filterButtons = document.querySelectorAll('.filter-btn');
const cards = document.querySelectorAll('.publication-card');

filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const filter = btn.getAttribute('data-filter');
        
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        cards.forEach(card => {
            if (filter === 'all' || card.getAttribute('data-category') === filter) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Animation des compteurs (si présents)
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const current = +counter.innerText;
            const increment = target / 100;
            if (current < target) {
                counter.innerText = Math.ceil(current + increment);
                setTimeout(updateCount, 20);
            } else {
                counter.innerText = target;
            }
        };
        updateCount();
    });
});
