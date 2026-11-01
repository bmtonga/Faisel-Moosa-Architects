/*-----------------------------------------------------------------------------------
    Project portfolio grid on index.html ("Projects" section).
    Reuses the Isotope + imagesLoaded plugins already loaded by Artima, but targets
    .project-portfolio__grid (not .grid) so main.js's fitRows setup is untouched.
    Image popups use the .popup-image Magnific Popup gallery initialised in main.js.
-----------------------------------------------------------------------------------*/
(function ($) {
    "use strict";

    $(function () {
        var $grid = $('.project-portfolio__grid');
        if (!$grid.length || typeof $.fn.isotope !== 'function') {
            return;
        }

        var isoOptions = {
            itemSelector: '.project-portfolio__item',
            percentPosition: true,
            layoutMode: 'masonry',
            masonry: {
                columnWidth: '.project-portfolio__sizer',
                gutter: '.project-portfolio__gutter'
            }
        };

        var $iso = $grid.isotope(isoOptions);

        var relayout = function () {
            $iso.isotope('layout');
            if (window.ScrollTrigger && typeof window.ScrollTrigger.refresh === 'function') {
                window.ScrollTrigger.refresh();
            }
        };

        if (typeof $.fn.imagesLoaded === 'function') {
            $grid.imagesLoaded().progress(relayout).always(relayout);
        } else {
            $(window).on('load', relayout);
        }

        function applyFilter(selector) {
            var $btn = $('.project-portfolio__filter button[data-filter="' + selector + '"]');
            if (!$btn.length) { return false; }
            $iso.isotope({ filter: selector });
            $btn.addClass('active').siblings('.active').removeClass('active');
            return true;
        }

        $('.project-portfolio__filter').on('click', 'button', function (event) {
            event.preventDefault();
            applyFilter($(this).attr('data-filter'));
        });

        // Deep links to a collection: #projects-residential, #projects-commercial,
        // #projects-refurbishment (used by the Projects menu); #projects shows all.
        function filterFromHash() {
            var m = /^#projects(?:-([a-z]+))?$/.exec(window.location.hash || '');
            if (!m) { return; }
            applyFilter(m[1] ? '.' + m[1] : '*');
        }
        window.fmaApplyProjectFilterFromHash = filterFromHash;
        $(window).on('hashchange', filterFromHash);
        filterFromHash();

        $iso.on('arrangeComplete', function () {
            if (window.ScrollTrigger && typeof window.ScrollTrigger.refresh === 'function') {
                window.ScrollTrigger.refresh();
            }
        });
    });

})(jQuery);
