/*-----------------------------------------------------------------------------------
    Project portfolio grid for index-4.html ("Latest projects" section).
    Reuses the Isotope + imagesLoaded plugins already loaded by Artima, but targets
    .project-portfolio-4__grid (not .grid) so main.js's fitRows setup is untouched.
    Image popups use the .popup-image Magnific Popup gallery initialised in main.js.
-----------------------------------------------------------------------------------*/
(function ($) {
    "use strict";

    $(function () {
        var $grid = $('.project-portfolio-4__grid');
        if (!$grid.length || typeof $.fn.isotope !== 'function') {
            return;
        }

        var isoOptions = {
            itemSelector: '.project-portfolio-4__item',
            percentPosition: true,
            layoutMode: 'masonry',
            masonry: {
                columnWidth: '.project-portfolio-4__sizer',
                gutter: '.project-portfolio-4__gutter'
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

        $('.project-portfolio-4__filter').on('click', 'button', function (event) {
            event.preventDefault();
            var $btn = $(this);
            $iso.isotope({ filter: $btn.attr('data-filter') });
            $btn.addClass('active').siblings('.active').removeClass('active');
        });

        $iso.on('arrangeComplete', function () {
            if (window.ScrollTrigger && typeof window.ScrollTrigger.refresh === 'function') {
                window.ScrollTrigger.refresh();
            }
        });
    });

})(jQuery);
