/*-----------------------------------------------------------------------------------
    Faisel Moosa Architects – cookie consent.
    The site sets no cookies of its own; the only consent-relevant content is the
    Google Maps embed on the Contact page (third-party cookies set by Google).
    Categories:
      necessary – the consent preference itself (localStorage, no cookie)
      embeds    – third-party embedded content (Google Maps)
    Embedded content is marked up as <div data-consent="embeds" data-src="…"> and is
    only turned into an <iframe> once the "embeds" category is allowed.
    No dependencies. Loaded on every page after fma-site.js.
-----------------------------------------------------------------------------------*/
(function () {
    "use strict";

    var KEY = 'fma-cookie-consent';
    var VERSION = 1;                                   // bump when the categories change
    var CATEGORIES = [
        { id: 'necessary', label: 'Strictly necessary', locked: true,
          text: 'Remembers the choice you make here. Stored in your browser, not sent to us, and not a cookie.' },
        { id: 'embeds', label: 'Embedded content (Google Maps)', locked: false,
          text: 'Loads the map of our office on the Contact page from Google, which may set its own cookies. The page works without it – the address is shown as text.' }
    ];

    // ---- storage -----------------------------------------------------------
    function read() {
        try {
            var raw = localStorage.getItem(KEY);
            if (!raw) return null;
            var v = JSON.parse(raw);
            return v && v.version === VERSION ? v : null;
        } catch (e) { return null; }
    }
    function write(prefs) {
        var v = { version: VERSION, date: new Date().toISOString(), embeds: !!prefs.embeds };
        try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) { /* storage blocked: popup shows again next visit */ }
        return v;
    }

    // ---- apply consent to the page --------------------------------------------
    function applyConsent(prefs) {
        var blocks = document.querySelectorAll('[data-consent="embeds"]');
        for (var i = 0; i < blocks.length; i++) {
            var el = blocks[i];
            if (prefs && prefs.embeds) {
                if (!el.querySelector('iframe')) {
                    var f = document.createElement('iframe');
                    f.src = el.getAttribute('data-src');
                    f.width = '100%';
                    f.height = el.getAttribute('data-height') || '450';
                    f.style.border = '0';
                    f.loading = 'lazy';
                    f.referrerPolicy = 'no-referrer-when-downgrade';
                    f.title = el.getAttribute('data-title') || 'Embedded content';
                    f.setAttribute('allowfullscreen', '');
                    el.innerHTML = '';
                    el.appendChild(f);
                    el.classList.add('is-loaded');
                }
            } else {
                el.classList.remove('is-loaded');
                el.innerHTML =
                    '<div class="fma-embed__placeholder" role="group" aria-label="' + (el.getAttribute('data-title') || 'Embedded content') + '">' +
                    '<p>' + (el.getAttribute('data-text') || 'This content is loaded from a third party that may set cookies.') + '</p>' +
                    '<button type="button" class="rr-btn fma-embed__load"><span class="btn-wrap"><span class="text-one">' + (el.getAttribute('data-button') || 'Load content') + '</span><span class="text-two">' + (el.getAttribute('data-button') || 'Load content') + '</span></span></button>' +
                    '<p class="fma-embed__note">Loading it allows cookies from the provider. See our <a href="cookie-policy.html">Cookie Policy</a>.</p>' +
                    '</div>';
            }
        }
    }

    // ---- UI ----------------------------------------------------------------
    var banner, modal, lastFocus;

    function buildBanner() {
        banner = document.createElement('div');
        banner.className = 'fma-cc';
        banner.setAttribute('role', 'region');
        banner.setAttribute('aria-label', 'Cookie consent');
        banner.innerHTML =
            '<div class="fma-cc__inner">' +
            '<div class="fma-cc__text">' +
            '<h2 class="fma-cc__title">Your privacy</h2>' +
            '<p>This website sets no cookies of its own. The map on our Contact page is loaded from Google and may set Google&rsquo;s cookies; it only loads if you allow it. ' +
            'Read our <a href="privacy-policy.html">Privacy Policy</a> and <a href="cookie-policy.html">Cookie Policy</a>.</p>' +
            '</div>' +
            '<div class="fma-cc__actions">' +
            '<button type="button" class="rr-btn fma-cc__btn" data-cc="accept"><span class="btn-wrap"><span class="text-one">Accept all</span><span class="text-two">Accept all</span></span></button>' +
            '<button type="button" class="rr-btn fma-cc__btn fma-cc__btn--ghost" data-cc="reject"><span class="btn-wrap"><span class="text-one">Reject optional</span><span class="text-two">Reject optional</span></span></button>' +
            '<button type="button" class="fma-cc__link" data-cc="manage" aria-haspopup="dialog">Manage preferences</button>' +
            '</div></div>';
        document.body.appendChild(banner);
        banner.addEventListener('click', onAction);
        // show after a beat so it animates in and never blocks first paint
        setTimeout(function () { banner.classList.add('is-visible'); }, 400);
    }

    function buildModal() {
        modal = document.createElement('div');
        modal.className = 'fma-cc-modal';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-modal', 'true');
        modal.setAttribute('aria-labelledby', 'fma-cc-modal-title');
        modal.hidden = true;
        var rows = '';
        for (var i = 0; i < CATEGORIES.length; i++) {
            var c = CATEGORIES[i];
            rows +=
                '<div class="fma-cc-modal__row">' +
                '<div class="fma-cc-modal__row-text"><h3 id="cc-' + c.id + '-label">' + c.label + (c.locked ? ' <span class="fma-cc-modal__always">Always on</span>' : '') + '</h3><p>' + c.text + '</p></div>' +
                '<label class="fma-cc-switch">' +
                '<input type="checkbox" name="' + c.id + '" aria-labelledby="cc-' + c.id + '-label"' + (c.locked ? ' checked disabled' : '') + '>' +
                '<span class="fma-cc-switch__track" aria-hidden="true"></span>' +
                '</label></div>';
        }
        modal.innerHTML =
            '<div class="fma-cc-modal__backdrop" data-cc="close"></div>' +
            '<div class="fma-cc-modal__panel">' +
            '<div class="fma-cc-modal__head"><h2 id="fma-cc-modal-title">Cookie preferences</h2>' +
            '<button type="button" class="fma-cc-modal__close" data-cc="close" aria-label="Close"><svg width="16" height="16" viewBox="0 0 18 18" fill="none" aria-hidden="true"><path d="M17 1L1 17M1 1l16 16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button></div>' +
            '<p class="fma-cc-modal__intro">Choose which optional content may load. Strictly necessary items cannot be switched off. Details in our <a href="cookie-policy.html">Cookie Policy</a>.</p>' +
            rows +
            '<div class="fma-cc-modal__actions">' +
            '<button type="button" class="rr-btn fma-cc__btn" data-cc="save"><span class="btn-wrap"><span class="text-one">Save preferences</span><span class="text-two">Save preferences</span></span></button>' +
            '<button type="button" class="fma-cc__link" data-cc="accept">Accept all</button>' +
            '<button type="button" class="fma-cc__link" data-cc="reject">Reject optional</button>' +
            '</div></div>';
        document.body.appendChild(modal);
        modal.addEventListener('click', onAction);
        modal.addEventListener('keydown', trapFocus);
    }

    function openModal() {
        if (!modal) buildModal();
        var prefs = read() || { embeds: false };
        modal.querySelector('input[name="embeds"]').checked = !!prefs.embeds;
        lastFocus = document.activeElement;
        modal.hidden = false;
        document.body.classList.add('fma-cc-open');
        requestAnimationFrame(function () {
            modal.classList.add('is-visible');
            modal.querySelector('.fma-cc-modal__close').focus();
        });
    }
    function closeModal() {
        if (!modal || modal.hidden) return;
        modal.classList.remove('is-visible');
        document.body.classList.remove('fma-cc-open');
        setTimeout(function () { modal.hidden = true; }, 250);
        if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    function trapFocus(e) {
        if (e.key === 'Escape') { e.preventDefault(); closeModal(); return; }
        if (e.key !== 'Tab') return;
        var items = modal.querySelectorAll('button:not([disabled]), input:not([disabled]), a[href]');
        var first = items[0], last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }

    function hideBanner() {
        if (!banner) return;
        banner.classList.remove('is-visible');
        setTimeout(function () { if (banner && banner.parentNode) banner.parentNode.removeChild(banner); banner = null; }, 400);
    }

    function decide(prefs) {
        var saved = write(prefs);
        applyConsent(saved);
        hideBanner();
        closeModal();
    }

    function onAction(e) {
        var t = e.target.closest ? e.target.closest('[data-cc]') : null;
        if (!t) return;
        e.preventDefault();
        switch (t.getAttribute('data-cc')) {
            case 'accept': decide({ embeds: true }); break;
            case 'reject': decide({ embeds: false }); break;
            case 'save':   decide({ embeds: modal.querySelector('input[name="embeds"]').checked }); break;
            case 'manage': openModal(); break;
            case 'close':  closeModal(); break;
        }
    }

    // ---- boot --------------------------------------------------------------
    function init() {
        var prefs = read();
        applyConsent(prefs);
        if (!prefs) buildBanner();

        // "Cookie settings" links (footer) and per-embed "Load" buttons
        document.addEventListener('click', function (e) {
            var a = e.target.closest ? e.target.closest('[data-cookie-settings]') : null;
            if (a) { e.preventDefault(); openModal(); return; }
            var b = e.target.closest ? e.target.closest('.fma-embed__load') : null;
            if (b) { e.preventDefault(); decide({ embeds: true }); }
        });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
