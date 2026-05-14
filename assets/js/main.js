(function () {
  'use strict';

  const LINK_SINGLE = 'https://buy.stripe.com/7sYaEQ9FbdVqfyAfp7c7u07';
  const LINK_DUO    = 'https://buy.stripe.com/00w7sEcRn8B6aeg0udc7u08';

  /* ── Language ──────────────────────────────── */
  function detectLang() {
    const saved = localStorage.getItem('wb-lang');
    if (saved && T[saved]) return saved;
    const bl = (navigator.language || 'en').toLowerCase();
    if (bl.startsWith('nl')) return 'nl';
    if (bl.startsWith('fr')) return 'fr';
    return 'en';
  }

  function applyLang(lang) {
    if (!T[lang]) return;
    localStorage.setItem('wb-lang', lang);
    document.documentElement.lang = lang;

    document.querySelectorAll('[data-k]').forEach(el => {
      const key = el.dataset.k;
      if (T[lang][key] !== undefined) {
        el.innerHTML = T[lang][key];
      }
    });

    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.lang === lang);
    });
  }

  /* ── Scroll reveal ─────────────────────────── */
  function initReveal() {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  }

  /* ── FAQ accordion ─────────────────────────── */
  function initFaq() {
    document.querySelectorAll('.faq-item').forEach(item => {
      item.querySelector('.faq-q').addEventListener('click', () => {
        const isOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
        if (!isOpen) item.classList.add('open');
      });
    });
  }

  /* ── Sticky nav shadow ─────────────────────── */
  function initNav() {
    const nav = document.querySelector('nav');
    if (!nav) return;
    window.addEventListener('scroll', () => {
      nav.style.boxShadow = window.scrollY > 60 ? '0 4px 40px rgba(0,0,0,.7)' : 'none';
    }, { passive: true });
  }

  /* ── Smooth CTA scroll ─────────────────────── */
  function initScrollLinks() {
    document.querySelectorAll('a[href="#pricing"]').forEach(a => {
      a.addEventListener('click', e => {
        e.preventDefault();
        document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  /* ── Buy buttons ───────────────────────────── */
  function initBuyButtons() {
    document.querySelectorAll('[data-buy="single"]').forEach(btn => {
      btn.addEventListener('click', () => {
        if (typeof fbq === 'function') {
          fbq('track', 'InitiateCheckout', { value: 59.00, currency: 'EUR', content_ids: ['wovo-band-single'], content_type: 'product' });
        }
        window.location.href = LINK_SINGLE;
      });
    });
    document.querySelectorAll('[data-buy="duo"]').forEach(btn => {
      btn.addEventListener('click', () => {
        if (typeof fbq === 'function') {
          fbq('track', 'InitiateCheckout', { value: 99.00, currency: 'EUR', content_ids: ['wovo-band-duo'], content_type: 'product' });
        }
        window.location.href = LINK_DUO;
      });
    });
  }

  /* ── Product image gallery ─────────────────── */
  function initGallery() {
    const stageImg = document.getElementById('stage-img');

    document.querySelectorAll('.gallery-thumb').forEach(thumb => {
      thumb.addEventListener('click', () => {
        document.querySelectorAll('.gallery-thumb').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
        if (stageImg) {
          stageImg.style.opacity = '0';
          stageImg.style.transform = 'scale(0.96)';
          setTimeout(() => {
            stageImg.src = thumb.dataset.target;
            stageImg.alt = thumb.dataset.alt;
            stageImg.style.opacity = '1';
            stageImg.style.transform = '';
          }, 200);
        }
      });
    });
  }

  /* ── Init ──────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', () => {
    applyLang(detectLang());

    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', () => applyLang(btn.dataset.lang));
    });

    initReveal();
    initFaq();
    initNav();
    initScrollLinks();
    initBuyButtons();
    initGallery();
  });
})();
