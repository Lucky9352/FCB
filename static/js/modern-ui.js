/**
 * TapNex Arena - Modern UI Utilities
 * Enhanced user experience with smooth interactions
 * Version: 2.0
 */

// ===== TOAST NOTIFICATION SYSTEM =====
class ToastManager {
  constructor() {
    this.container = this.createContainer();
    this.toasts = [];
  }

  createContainer() {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    return container;
  }

  show(options = {}) {
    const {
      type = 'info',
      title = '',
      message = '',
      duration = 5000,
      icon = null
    } = options;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const iconMap = {
      success: '<svg class="toast-icon" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>',
      error: '<svg class="toast-icon" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>',
      warning: '<svg class="toast-icon" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>',
      info: '<svg class="toast-icon" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>'
    };

    toast.innerHTML = `
      ${icon || iconMap[type] || iconMap.info}
      <div class="toast-content">
        ${title ? `<div class="toast-title">${title}</div>` : ''}
        <div class="toast-message">${message}</div>
      </div>
      <button class="toast-close" aria-label="Close">
        <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
        </svg>
      </button>
    `;

    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => this.remove(toast));

    this.container.appendChild(toast);
    this.toasts.push(toast);

    if (duration > 0) {
      setTimeout(() => this.remove(toast), duration);
    }

    return toast;
  }

  remove(toast) {
    toast.style.animation = 'fadeOut 0.3s ease-out';
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
      this.toasts = this.toasts.filter(t => t !== toast);
    }, 300);
  }

  success(message, title = 'Success') {
    return this.show({ type: 'success', title, message });
  }

  error(message, title = 'Error') {
    return this.show({ type: 'error', title, message });
  }

  warning(message, title = 'Warning') {
    return this.show({ type: 'warning', title, message });
  }

  info(message, title = 'Info') {
    return this.show({ type: 'info', title, message });
  }
}

// Create global toast instance
window.toast = new ToastManager();

// ===== SMOOTH SCROLL =====
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// ===== LAZY LOADING IMAGES =====
function initLazyLoading() {
  const images = document.querySelectorAll('img[data-src]');
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        img.classList.add('animate-fadeIn');
        observer.unobserve(img);
      }
    });
  });

  images.forEach(img => imageObserver.observe(img));
}

// ===== SCROLL REVEAL ANIMATIONS =====
function initScrollReveal() {
  const elements = document.querySelectorAll('[data-reveal]');
  
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const element = entry.target;
        const animation = element.dataset.reveal || 'fadeInUp';
        const delay = element.dataset.revealDelay || 0;
        
        setTimeout(() => {
          element.classList.add(`animate-${animation}`);
        }, delay);
        
        revealObserver.unobserve(element);
      }
    });
  }, { threshold: 0.1 });

  elements.forEach(el => revealObserver.observe(el));
}

// ===== FORM VALIDATION =====
class FormValidator {
  constructor(form) {
    this.form = form;
    this.init();
  }

  init() {
    const inputs = this.form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
      input.addEventListener('blur', () => this.validateField(input));
      input.addEventListener('input', () => this.clearError(input));
    });

    this.form.addEventListener('submit', (e) => {
      if (!this.validateForm()) {
        e.preventDefault();
      }
    });
  }

  validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute('required');

    if (required && !value) {
      this.showError(field, 'This field is required');
      return false;
    }

    if (type === 'email' && value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        this.showError(field, 'Please enter a valid email address');
        return false;
      }
    }

    if (type === 'tel' && value) {
      const phoneRegex = /^[0-9]{10}$/;
      if (!phoneRegex.test(value.replace(/\D/g, ''))) {
        this.showError(field, 'Please enter a valid phone number');
        return false;
      }
    }

    if (field.hasAttribute('minlength')) {
      const minLength = parseInt(field.getAttribute('minlength'));
      if (value.length < minLength) {
        this.showError(field, `Minimum ${minLength} characters required`);
        return false;
      }
    }

    this.clearError(field);
    return true;
  }

  validateForm() {
    const inputs = this.form.querySelectorAll('input, textarea, select');
    let isValid = true;

    inputs.forEach(input => {
      if (!this.validateField(input)) {
        isValid = false;
      }
    });

    return isValid;
  }

  showError(field, message) {
    this.clearError(field);
    field.classList.add('form-input-error');
    
    const error = document.createElement('div');
    error.className = 'form-error';
    error.textContent = message;
    
    field.parentNode.appendChild(error);
  }

  clearError(field) {
    field.classList.remove('form-input-error');
    const error = field.parentNode.querySelector('.form-error');
    if (error) {
      error.remove();
    }
  }
}

// ===== MODAL MANAGER =====
class ModalManager {
  constructor() {
    this.modals = new Map();
    this.init();
  }

  init() {
    // Setup modal triggers
    document.querySelectorAll('[data-modal-trigger]').forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.preventDefault();
        const modalId = trigger.dataset.modalTrigger;
        this.open(modalId);
      });
    });

    // Setup close buttons
    document.querySelectorAll('[data-modal-close]').forEach(closeBtn => {
      closeBtn.addEventListener('click', () => {
        const modal = closeBtn.closest('.modal');
        if (modal) {
          this.close(modal.id);
        }
      });
    });

    // Close on overlay click
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          const modal = document.querySelector('.modal[style*="display"]');
          if (modal) {
            this.close(modal.id);
          }
        }
      });
    });

    // Close on ESC key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const openModal = Array.from(this.modals.entries())
          .find(([_, isOpen]) => isOpen);
        if (openModal) {
          this.close(openModal[0]);
        }
      }
    });
  }

  open(modalId) {
    const modal = document.getElementById(modalId);
    const overlay = modal?.previousElementSibling;
    
    if (modal && overlay) {
      modal.style.display = 'flex';
      overlay.style.display = 'block';
      document.body.style.overflow = 'hidden';
      this.modals.set(modalId, true);
      
      // Focus first focusable element
      const focusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (focusable) {
        setTimeout(() => focusable.focus(), 100);
      }
    }
  }

  close(modalId) {
    const modal = document.getElementById(modalId);
    const overlay = modal?.previousElementSibling;
    
    if (modal && overlay) {
      modal.style.display = 'none';
      overlay.style.display = 'none';
      document.body.style.overflow = '';
      this.modals.set(modalId, false);
    }
  }
}

// ===== PARTICLE BACKGROUND =====
class ParticleBackground {
  constructor(container) {
    this.container = container;
    this.particles = [];
    this.init();
  }

  init() {
    const particleCount = window.innerWidth < 768 ? 30 : 50;
    
    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.cssText = `
        position: absolute;
        width: ${Math.random() * 4 + 1}px;
        height: ${Math.random() * 4 + 1}px;
        background: rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2});
        border-radius: 50%;
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation: float ${Math.random() * 10 + 10}s ease-in-out infinite;
        animation-delay: ${Math.random() * 5}s;
      `;
      
      this.container.appendChild(particle);
      this.particles.push(particle);
    }
  }
}

// ===== RIPPLE EFFECT =====
function createRipple(event) {
  const button = event.currentTarget;
  const ripple = document.createElement('span');
  const diameter = Math.max(button.clientWidth, button.clientHeight);
  const radius = diameter / 2;

  ripple.style.width = ripple.style.height = `${diameter}px`;
  ripple.style.left = `${event.clientX - button.offsetLeft - radius}px`;
  ripple.style.top = `${event.clientY - button.offsetTop - radius}px`;
  ripple.classList.add('ripple');

  const existingRipple = button.querySelector('.ripple');
  if (existingRipple) {
    existingRipple.remove();
  }

  button.appendChild(ripple);
}

// ===== COPY TO CLIPBOARD =====
async function copyToClipboard(text, showToast = true) {
  try {
    await navigator.clipboard.writeText(text);
    if (showToast && window.toast) {
      window.toast.success('Copied to clipboard!');
    }
    return true;
  } catch (err) {
    console.error('Failed to copy:', err);
    if (showToast && window.toast) {
      window.toast.error('Failed to copy to clipboard');
    }
    return false;
  }
}

// ===== DEBOUNCE UTILITY =====
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ===== THROTTLE UTILITY =====
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// ===== INITIALIZE ON DOM READY =====
document.addEventListener('DOMContentLoaded', () => {
  // Initialize smooth scroll
  initSmoothScroll();
  
  // Initialize lazy loading
  initLazyLoading();
  
  // Initialize scroll reveal
  initScrollReveal();
  
  // Initialize modals
  window.modalManager = new ModalManager();
  
  // Initialize form validation
  document.querySelectorAll('form[data-validate]').forEach(form => {
    new FormValidator(form);
  });
  
  // Initialize ripple effects on buttons
  document.querySelectorAll('.btn-ripple').forEach(button => {
    button.addEventListener('click', createRipple);
  });
  
  // Initialize particle backgrounds
  document.querySelectorAll('.particles-container').forEach(container => {
    new ParticleBackground(container);
  });
  
  // Add loading class removal
  window.addEventListener('load', () => {
    document.body.classList.add('loaded');
    const preloader = document.getElementById('preloader');
    if (preloader) {
      setTimeout(() => {
        preloader.classList.add('fade-out');
        setTimeout(() => preloader.remove(), 500);
      }, 500);
    }
  });
});

// Export utilities for global use
window.TapNexUI = {
  toast: window.toast,
  copyToClipboard,
  debounce,
  throttle,
  createRipple
};
