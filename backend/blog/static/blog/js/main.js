/* filepath: c:\Users\frus84312\AppPython\backend\blog\static\blog\js\main.js */

// Fonction pour adapter l'image selon ses dimensions
document.addEventListener('DOMContentLoaded', function() {
    // Gestion des images d'articles
    const articleImage = document.getElementById('articleImage');
    if (articleImage) {
        articleImage.onload = function() {
            const aspectRatio = this.naturalWidth / this.naturalHeight;
            
            // Si l'image est très large (paysage)
            if (aspectRatio > 2) {
                this.classList.add('wide-image');
            }
            // Si l'image est très haute (portrait)
            else if (aspectRatio < 0.7) {
                this.classList.add('tall-image');
            }
        };
        
        // Si l'image est déjà chargée
        if (articleImage.complete) {
            articleImage.onload();
        }
    }
    
    // Gestion des formulaires de modification d'image
    initImageManagement();
    
    // Fermeture automatique des alertes
    autoCloseAlerts();
    
    // Animations au scroll
    initScrollAnimations();
});

// Fonctions pour le modal d'image
function openImageModal(imageSrc) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    if (modal && modalImage) {
        modal.style.display = 'block';
        modalImage.src = imageSrc;
        document.body.style.overflow = 'hidden';
    }
}

function closeImageModal() {
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Gestion des images dans les formulaires
function initImageManagement() {
    const removeImageCheckbox = document.getElementById('remove_image');
    const imageInput = document.querySelector('input[type="file"]');
    const currentImageSection = document.querySelector('.current-image-section');
    
    if (removeImageCheckbox && imageInput) {
        // Quand on coche "supprimer l'image"
        removeImageCheckbox.addEventListener('change', function() {
            if (this.checked) {
                imageInput.disabled = true;
                imageInput.value = '';
                if (currentImageSection) {
                    currentImageSection.style.opacity = '0.5';
                }
            } else {
                imageInput.disabled = false;
                if (currentImageSection) {
                    currentImageSection.style.opacity = '1';
                }
            }
        });
        
        // Quand on sélectionne un nouveau fichier
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                removeImageCheckbox.checked = false;
                if (currentImageSection) {
                    currentImageSection.style.opacity = '1';
                }
            }
        });
    }
}

// Fermeture automatique des alertes
function autoCloseAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.transition = 'all 0.5s ease';
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000);
    });
}

// Animations au scroll
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observer les éléments à animer
    const elementsToAnimate = document.querySelectorAll('.card, .article-card, .form-container');
    elementsToAnimate.forEach(el => {
        observer.observe(el);
    });
}

// Gestion des événements clavier
document.addEventListener('keydown', function(event) {
    // Fermer le modal avec Échap
    if (event.key === 'Escape') {
        closeImageModal();
    }
    
    // Raccourcis clavier pour la navigation
    if (event.ctrlKey && event.key === 'h') {
        event.preventDefault();
        window.location.href = '/';
    }
});

// Confirmation de suppression
function confirmDelete(message = 'Êtes-vous sûr de vouloir supprimer cet élément ?') {
    return confirm(message);
}

// Validation côté client pour les formulaires
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Prévisualisation d'image avant upload
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById(previewId);
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Utilitaires
const Utils = {
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Format date
    formatDate: function(date) {
        return new Intl.DateTimeFormat('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    // Scroll vers un élément
    scrollTo: function(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    }
};