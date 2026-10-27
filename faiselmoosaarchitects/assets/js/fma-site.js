/*-----------------------------------------------------------------------------------
    Faisel Moosa Architects – site-wide behaviour.
    Smooth in-page scrolling for the section links (#about, #services, #projects):
    eases to the section with breathing room under the fixed header; the About
    section is centred vertically in the viewport when it fits.
    Loaded on every page after main.js.
-----------------------------------------------------------------------------------*/
(function () {
    "use strict";

    var SPACE_BELOW_HEADER = 32;   // px of air between the header and the section top
    var CENTERED = { about: '.row' }; // sections centred on their content block instead of top-aligned

    function headerHeight() {
        var h = document.getElementById('header-sticky');
        return h ? h.getBoundingClientRect().height : 0;
    }

    function targetFor(section) {
        var rect = section.getBoundingClientRect();
        var top = rect.top + window.pageYOffset;
        var inner = CENTERED[section.id] ? section.querySelector(CENTERED[section.id]) : null;
        if (inner) {
            var r = inner.getBoundingClientRect();
            var usable = window.innerHeight - headerHeight();
            if (r.height < usable) {
                // centre the content block in the space below the header
                return r.top + window.pageYOffset - headerHeight() - (usable - r.height) / 2;
            }
        }
        return top - headerHeight() - SPACE_BELOW_HEADER;
    }

    function easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    var raf;
    function scrollToY(y, done) {
        var start = window.pageYOffset;
        var max = document.documentElement.scrollHeight - window.innerHeight;
        y = Math.max(0, Math.min(y, max));
        var dist = y - start;
        if (Math.abs(dist) < 2) { if (done) done(); return; }
        var duration = Math.min(1400, Math.max(650, Math.abs(dist) * 0.55));
        var t0 = null;
        if (raf) cancelAnimationFrame(raf);
        function step(ts) {
            if (t0 === null) t0 = ts;
            var p = Math.min(1, (ts - t0) / duration);
            window.scrollTo(0, start + dist * easeInOutCubic(p));
            if (p < 1) raf = requestAnimationFrame(step); else if (done) done();
        }
        raf = requestAnimationFrame(step);
    }

    function sectionFromHref(href) {
        if (!href) return null;
        var hash = href.indexOf('#') >= 0 ? href.slice(href.indexOf('#') + 1) : '';
        if (!hash) return null;
        var path = href.slice(0, href.indexOf('#'));
        var here = location.pathname.split('/').pop() || 'index.html';
        if (path && path !== here) return null;          // link to another page
        return document.getElementById(hash);
    }

    document.addEventListener('click', function (e) {
        var a = e.target.closest ? e.target.closest('a[href*="#"]') : null;
        if (!a || a.target === '_blank') return;
        var section = sectionFromHref(a.getAttribute('href'));
        if (!section) return;
        e.preventDefault();
        scrollToY(targetFor(section), function () {
            if (history.replaceState) history.replaceState(null, '', '#' + section.id);
        });
        // close the mobile offcanvas if it is open
        var panel = document.querySelector('.offcanvas__area.info-open');
        var closeBtn = document.querySelector('.offcanvas-close-icon');
        if (panel && closeBtn) closeBtn.click();
    });

    // Arriving from another page with a hash (index.html#about): re-position after
    // the browser's native jump, once layout (fonts, images) has settled.
    if (location.hash) {
        var section = document.getElementById(location.hash.slice(1));
        if (section) {
            if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
            window.addEventListener('load', function () {
                setTimeout(function () { scrollToY(targetFor(section)); }, 350);
            });
        }
    }
})();
