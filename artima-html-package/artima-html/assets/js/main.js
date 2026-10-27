
(function ($) {
    "use strict";
    var windowOn = $(window);

    /*-----------------------------------------------------------------------------------
        Template Name: Artima – Modern Architecture & Interior HTML5 Template
        Author: RRDevs
        Support: https://support.rrdevs.net
        Description: Artima – Modern Architecture & Interior HTML5 Template.
        Version: 1.0
        Developer Github: Rana Ahmmed (https://github.com/mdranaahmed-dev)
    -----------------------------------------------------------------------------------

     */
    /*======================================
    Data Css js
    ========================================*/
    $("[data-background]").each(function () {
        $(this).css(
            "background-image",
            "url( " + $(this).attr("data-background") + "  )"
        );
    });

    $("[data-width]").each(function () {
        $(this).css("width", $(this).attr("data-width"));
    });


    class GSAPAnimation {
        static Init() {
            /*title-animation*/
            this.upDownScrollTriggerAnimation('.b-t__scroll');
            $('.right-separetor').length && this.width100ScrollTriggerAnimation('.right-separetor');
            $('.left-separetor').length && this.width100ScrollTriggerAnimation('.left-separetor');
            $('.title-animation').length && this.sectionTitleAnimation('.title-animation');
        }

        static sectionTitleAnimation(activeClass) {
            let sectionTitleLines = gsap.utils.toArray(activeClass);

            sectionTitleLines.forEach(sectionTextLine => {
                const tl = gsap.timeline({
                    scrollTrigger: {
                        trigger: sectionTextLine,
                        start: 'top 90%',
                        end: 'bottom 60%',
                        scrub: false,
                        markers: false,
                        toggleActions: 'play none none none'
                    }
                });

                const itemSplitted = new SplitText(sectionTextLine, { type: "chars, words" });
                gsap.set(sectionTextLine, { perspective: 100 });
                itemSplitted.split({ type: "words" })
                tl.from(itemSplitted.words, {
                    opacity: 0,
                    autoAlpha: 0,
                    transformOrigin: "top center -50",
                    y: "10px",
                    duration: 0.9,
                    stagger: 0.1,
                    ease: "power2.out",
                });
            });
        }

        static width100ScrollTriggerAnimation(activeClass) {
            let Lines = gsap.utils.toArray(activeClass);
            Lines.forEach(Line => {
                const maxWidth = Line.getAttribute('data-width') || '100%';
                gsap.fromTo(Line, {
                    width: "0"
                }, {
                    opacity: 1,
                    width: maxWidth,
                    duration: 0.9,
                    ease: "power2.out",
                    scrollTrigger: {
                        trigger: Line,
                        start: 'top 100%',
                        end: 'top 10%',
                        scrub: true,
                        markers: false,
                        toggleActions: 'play none none none'
                    }
                });
            });
        }

        static upDownScrollTriggerAnimation(titleClass) {
            let Title = gsap.utils.toArray(titleClass);

            Title.forEach(TitleSingle => {
                const TitleSingleTarget = TitleSingle.getAttribute('data-target');
                const TitleSingleTargetHeight = TitleSingle.getAttribute('data-target-height');

                gsap.to(TitleSingle, {
                    scrollTrigger: {
                        trigger: TitleSingle,
                        start: "top 20%",
                        end: () => {
                            let totalHeight = 0;
                            if (TitleSingleTarget) {
                                totalHeight += $(TitleSingleTarget).innerHeight();
                                totalHeight -= $(TitleSingle).innerHeight();
                            }
                            if (TitleSingleTargetHeight) {
                                totalHeight += parseInt(TitleSingleTargetHeight);
                            }
                            return `+=${totalHeight}`;
                        },
                        pin: true,
                        pinSpacing: false,
                        scrub: true,
                        markers: false,
                    }
                });
            });
        }
    }

    class RRDEVS {
        constructor() {
            this.isLoaded = false;
        }
        static LoadedAfterDoted() {
            if (this.isLoaded) {
                return false;
            }
            this.isLoaded = true;
            $('#preloader').delay(1).fadeOut(0);

            $('.odometer').waypoint(function (direction) {
                if (direction === 'down') {
                    let countNumber = $(this.element).attr("data-count");
                    $(this.element).html(countNumber);
                }
            }, {
                offset: '80%'
            });

            /*Wow Js*/
            if ($('.wow').length) {
                var wow = new WOW({
                    boxClass: 'wow',
                    animateClass: 'animated',
                    offset: 0,
                    mobile: false,
                    live: true
                });
                wow.init();
            }

            /*GSAPAnimation*/
            GSAPAnimation.Init();
        }

        delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
    }

    /*======================================
      Preloader activation with multiple
     ========================================*/
    const preloaders = $("[data-preloader]");
    preloaders.each(function (index, item) {
        if ($(item).data('preloader') === 'active') {
            if ($(item).data('loaded') === 'progress') {
                const RRDevsInit = new RRDEVS();
                $(".preloader-close").on("click", () => RRDevsInit.LoadedAfterProgress('click'));
                $(window).on('load', () => RRDevsInit.LoadedAfterProgress('load'));
            } else if ($(item).data('loaded') === 'doted') {
                $(".preloader-close").on("click", () => RRDEVS.LoadedAfterDoted());
                $(window).on('load', () => RRDEVS.LoadedAfterDoted());
            }
        }
    });

    window.addEventListener('resize', function () {
        gsap.globalTimeline.clear();
    });

    /*======================================
      Mobile Menu Js
      ========================================*/
    $("#mobile-menu").meanmenu({
        meanMenuContainer: ".mobile-menu",
        meanScreenWidth: "1199",
        meanExpand: ['<i class="fa-regular fa-angle-right"></i>'],
    });

    /*======================================
      Mobile Menu Js
      ========================================*/
    $("#mobile-main-menu").meanmenu({
        meanMenuContainer: ".mobile-main-menu",
        meanScreenWidth: "9999",
        meanExpand: ['<i class="fa-regular fa-angle-right"></i>'],
    });

    /*======================================
      Sidebar Toggle
      ========================================*/
    $(".offcanvas__close,.offcanvas__overlay").on("click", function () {
        $(".offcanvas__area").removeClass("info-open");
        $(".offcanvas__overlay").removeClass("overlay-open");
    });
    // Scroll to bottom then close navbar
    $(window).scroll(function () {
        if ($("body").scrollTop() > 0 || $("html").scrollTop() > 0) {
            $(".offcanvas__area").removeClass("info-open");
            $(".offcanvas__overlay").removeClass("overlay-open");
        }
    });
    $(".sidebar__toggle").on("click", function () {
        $(".offcanvas__area").addClass("info-open");
        $(".offcanvas__overlay").addClass("overlay-open");
    });

    /*======================================
      Body overlay Js
      ========================================*/
    $(".body-overlay").on("click", function () {
        $(".offcanvas__area").removeClass("opened");
        $(".body-overlay").removeClass("opened");
    });

    /*======================================
      Sticky Header Js
      ========================================*/
    $(window).scroll(function () {
        if ($(this).scrollTop() > 10) {
            $("#header-sticky").addClass("rr-sticky");
        } else {
            $("#header-sticky").removeClass("rr-sticky");
        }
    });

    /*======================================
      MagnificPopup image view
      ========================================*/
    $(".popup-image").magnificPopup({
        type: "image",
        gallery: {
            enabled: true,
        },
    });

    /*======================================
      MagnificPopup video view
      ========================================*/
    $(".popup-video").magnificPopup({
        type: "iframe",
    });

    /*======================================
      Page Scroll Percentage
      ========================================*/
    const scrollTopPercentage = () => {
        const scrollPercentage = () => {
            const scrollTopPos = document.documentElement.scrollTop;
            const calcHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrollValue = Math.round((scrollTopPos / calcHeight) * 100);
            const scrollElementWrap = $("#scroll-percentage");

            scrollElementWrap.css("background", `conic-gradient( var(--rr-theme-primary) ${scrollValue}%, var(--rr-heading-primary) ${scrollValue}%)`);

            if (scrollTopPos > 100) {
                scrollElementWrap.addClass("active");
            } else {
                scrollElementWrap.removeClass("active");
            }

            if (scrollValue < 96) {
                $("#scroll-percentage-value").text(`${scrollValue}%`);
            } else {
                $("#scroll-percentage-value").html('<i class="fa-solid fa-angle-up"></i>');
            }
        }
        window.onscroll = scrollPercentage;
        window.onload = scrollPercentage;

        // Back to Top
        function scrollToTop() {
            document.documentElement.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }

        $("#scroll-percentage").on("click", scrollToTop);
    }
    scrollTopPercentage();

    /*======================================
    One Page Scroll Js
    ========================================*/
    var link = $('.onepagenav #mobile-menu ul li a, .onepagenav .mean-nav ul li a');
    link.on('click', function (e) {
        var target = $($(this).attr('href'));
        $('html, body').animate({
            scrollTop: target.offset().top - 76
        }, 600);
        $(this).parent().addClass('active');
        e.preventDefault();
    });
    $(window).on('scroll', function () {
        scrNav();
    });

    function scrNav() {
        var sTop = $(window).scrollTop();
        $('section').each(function () {
            var id = $(this).attr('id'),
                offset = $(this).offset().top - 1,
                height = $(this).height();
            if (sTop >= offset && sTop < offset + height) {
                link.parent().removeClass('active');
                $('.main-menu').find('[href="#' + id + '"]').parent().addClass('active');
            }
        });
    }
    scrNav();

    /*======================================
    Smoth animatio Js
    ========================================*/
    $(document).on('click', '.smoth-animation', function (event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: $($.attr(this, 'href')).offset().top - 50
        }, 300);
    });

    //slider-text
    const scrollers = document.querySelectorAll(".rr-scroller");
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        addAnimation();
    }
    function addAnimation() {
        scrollers.forEach((scroller) => {
            scroller.setAttribute("data-animated", true);

            const scrollerInner = scroller.querySelector(".rr-scroller__inner");
            const scrollerContent = Array.from(scrollerInner.children);

            scrollerContent.forEach((item) => {
                const duplicatedItem = item.cloneNode(true);
                duplicatedItem.setAttribute("aria-hidden", true);
                scrollerInner.appendChild(duplicatedItem);
            });
        });
    }


    /*testimonial__slider***/
    let clienttestimonial__slider = new Swiper(".testimonial__slider", {
        slidesPerView: 3,
        spaceBetween: 30,
        loop: true,
        centeredSlides: true,
        clickable: true,
        autoplay: {
            delay: 3000,
        },
        pagination: {
            el: ".testimonial__slider-dot",
            clickable: true,
        },
        breakpoints: {
            1200: {
                slidesPerView: 3,
            },
            992: {
                slidesPerView: 2,
            },
            0: {
                slidesPerView: 1,
            },
        }
    });

    /*latest-article__slider***/
    let latest_article__slider = new Swiper(".latest-article__slider", {
        slidesPerView: 3,
        spaceBetween: 30,
        loop: true,
        centeredSlides: true,
        clickable: true,
        autoplay: {
            delay: 3000,
        },
        pagination: {
            el: ".latest-article__slider-dot",
            clickable: true,
        },
        breakpoints: {
            1200: {
                slidesPerView: 3,
            },
            992: {
                slidesPerView: 2,
            },
            0: {
                slidesPerView: 1,
            },
        }
    });

    /* image compare js ***/
    var ctrl = jQuery('.filter__container .comparison-ctrl');
    var pic_right = jQuery('.filter__container .pic--right');
    Draggable.create(ctrl, {
        bounds: ctrl.parent(),
        type: "x",
        onDrag: function () {
            pic_right.css('left', 'calc(50% + ' + (this.x - 2) + 'px)');
        }
    });


    /*testimonial-2__slider***/
    let testimonial2slider = new Swiper(".testimonial-2__slider", {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        centeredSlides: true,
        clickable: true,
        autoplay: {
            delay: 3000,
        },
        pagination: {
            el: ".testimonial-2__slider-dot",
            clickable: true,
        },
    });

    if ($(".count-bar").length) {
        $(".count-bar").appear(
            function () {
                var el = $(this);
                var percent = el.data("percent");
                $(el).css("width", percent).addClass("counted");
            }, {
            accY: -50
        }
        );
    }



    $('.header__top__lang-select-select select, .contact__form-input-select select').niceSelect();

    $(".search-open-btn").on("click", function () {
        $(".search__popup").addClass("search-opened");
    });
    $(".search-close-btn").on("click", function () {
        $(".search__popup").removeClass("search-opened");
    });


    /*team__slider***/
    let team__slider = new Swiper(".team__slider", {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        clickable: true,
        pagination: {
            el: ".team__slider-dot",
            clickable: true,
        },
        autoplay: {
            delay: 3000,
        },
        breakpoints: {
            1200: {
                slidesPerView: 3,
            },
            768: {
                slidesPerView: 2,
            },
            0: {
                slidesPerView: 1,
            },
        },
    });



    function lastNobullet() {
        $(".last_no_bullet ul").each(function () {
            var $listItems = $(this).find("li");

            if ($listItems.length > 1) {
                $listItems.last().addClass("no_bullet");
            }
        });
    }

    lastNobullet();

    $(window).resize(function () {
        lastNobullet();
    });

    $('#contact-us-message__form').submit(function (event) {
        event.preventDefault();
        var form = $(this);
        var valid = true;

        form.find('.error-message').remove();
        form.find('.success-message').remove();

        form.find('input, textarea, select').each(function () {
            if ($(this).val().trim() === '') {
                valid = false;
                $(this).parent().after('<p class="error-message  mt-3 mb-0">This field is required.</p>');
            }
        });

        if (!valid) {
            return;
        }

        $('.loading-form').show();

        setTimeout(function () {
            $.ajax({
                type: form.attr('method'),
                url: form.attr('action'),
                data: form.serialize()
            }).done(function (data) {
                $('.loading-form').hide();
                form.append('<p class="success-message mt-3 mb-0">Your message has been sent successfully.</p>');
            }).fail(function (data) {
                $('.loading-form').hide();
                form.append('<p class="error-message mt-3 mb-0">Something went wrong. Please try again later.</p>');
            });
        }, 1000);
    });

    $('.carouselTicker-nav').carouselTicker({});

    /*** pricing table2 */
    const pricingMonthlyBtn = $("#monthly-btn"),
        pricingYearlyBtn = $("#yearly-btn"),
        pricingValues = $(".pricing-2__card-price h2, .yearly p");

    if (pricingMonthlyBtn[0] && pricingYearlyBtn[0] && pricingValues.length > 0) {
        pricingMonthlyBtn[0].addEventListener("click", function () {
            updatePricingValuestop("monthly");
            pricingYearlyBtn[0].classList.remove("active");
            pricingMonthlyBtn[0].classList.add("active");
        });

        pricingYearlyBtn[0].addEventListener("click", function () {
            updatePricingValuestop("yearly");
            pricingMonthlyBtn[0].classList.remove("active");
            pricingYearlyBtn[0].classList.add("active");
        });
    }

    function updatePricingValuestop(option) {
        pricingValues.each(function () {
            const pricingValue = $(this);
            const yearlyValue = pricingValue.attr("data-yearly");
            const monthlyValue = pricingValue.attr("data-monthly");

            const newValue = option === "monthly" ? monthlyValue : yearlyValue;
            pricingValue.html(newValue);
        });
    }

    function updatePricingValues(option) {
        pricingValues1.each(function () {
            const pricingValue = $(this);
            const yearlyValue = pricingValue.attr("data-yearly");
            const monthlyValue = pricingValue.attr("data-monthly");

            const newValue = option === "monthly" ? monthlyValue : yearlyValue;
            pricingValue.html(newValue);
        });
    }

    class MagneticButton {
        constructor(options) {
            this.settings = $.extend({
                target: $('[data-magnetic]'),
                class: 'magnetizing',
                attraction: 0.45,
                distance: 100,
                onEnter: function (data) { },
                onExit: function (data) { },
                onUpdate: function (data) { },
            }, options);

            if (!this.settings.target.length) return;

            this.init();
        }

        init() {
            $(window).on('mousemove', (e) => this.magnetize(e));
        }

        distanceFromMouse($target, mouseX, mouseY) {
            let centerX = $target.offset().left + $target.outerWidth() / 2,
                centerY = $target.offset().top + $target.outerHeight() / 2,
                pointX = mouseX - centerX,
                pointY = mouseY - centerY,
                distance = Math.sqrt(Math.pow(pointX, 2) + Math.pow(pointY, 2));

            return Math.floor(distance);
        }

        magnetize(e) {
            let mouseX = e.pageX, mouseY = e.pageY;

            this.settings.target.each((index, element) => {
                let $this = $(element),
                    centerX = $this.offset().left + $this.outerWidth() / 2,
                    centerY = $this.offset().top + $this.outerHeight() / 2,
                    attraction = $this.data('magnetic-attraction') || this.settings.attraction,
                    distance = $this.data('magnetic-distance') || this.settings.distance,
                    deltaX = Math.floor(centerX - mouseX) * -1 * attraction,
                    deltaY = Math.floor(centerY - mouseY) * -1 * attraction,
                    mouseDistance = this.distanceFromMouse($this, mouseX, mouseY),
                    isEnter = $this.data('isEnter') || false,
                    data = { target: $this, y: deltaY, x: deltaX, distance: mouseDistance };

                if (mouseDistance < distance) {
                    gsap.to($this, { y: deltaY, x: deltaX });

                    if (!isEnter) {
                        $this.data('isEnter', true);
                        $this.addClass(this.settings.class);
                        this.settings.onEnter(data);
                    }

                    this.settings.onUpdate(data);
                } else {
                    gsap.to($this, { y: 0, x: 0 });

                    if (isEnter) {
                        $this.data('isEnter', false);
                        $this.removeClass(this.settings.class);
                        this.settings.onExit(data);
                    }
                }
            });
        }
    }

    new MagneticButton({
        attraction: (data) => data.target[0].dataset.magneticAttraction,
        distance: (data) => data.target[0].dataset.magneticDistance,
        onEnter: function (data) {
            gsap.to(data.target, { scale: data.target[0].dataset.magneticZoom });
        },
        onExit: function (data) {
            gsap.to(data.target, { scale: 1 });
        },
        onUpdate: function (data) { }
    });


    var slider = new Swiper('.banner__slider', {
        slidesPerView: 1,
        centeredSlides: true,
        autoplay: true,
        loop: true,
        loopedSlides: 6,
        autoplay: {
            delay: 3000,
        },
        navigation: {
            prevEl: ".banner__slider__arrow-prev",
            nextEl: ".banner__slider__arrow-next",
        },
    });

    var thumbs = new Swiper('.gallery-thumbs', {
        slidesPerView: 'auto',
        spaceBetween: 1,
        centeredSlides: true,
        loop: true,
        slideToClickedSlide: true,
    });

    slider.controller.control = thumbs;
    thumbs.controller.control = slider;

    /*client-testimonial__slider***/
    let expert__slider = new Swiper(".expert__slider", {
        slidesPerView: 3,
        spaceBetween: 30,
        loop: true,
        clickable: true,
        autoplay: {
            delay: 3000,
        },
        pagination: {
            el: ".expert__slider-dot",
            clickable: true,
        },

        breakpoints: {
            1200: {
                slidesPerView: 3,
            },
            992: {
                slidesPerView: 2,
            },
            0: {
                slidesPerView: 1,
            },
        }
    });

    /*======================================
    recent-project__active
    ========================================*/
    let recent_project__active = new Swiper(".recent-project__active", {
        loop: true,
        slidesPerView: 3,
        spaceBetween: 30,
        centeredSlides: true,
        navigation: {
            prevEl: ".recent-project__slider__arrow-prev",
            nextEl: ".recent-project__slider__arrow-next",
        },
        autoplay: {
            delay: 3000,
        },
        initialSlide: 5,
        breakpoints: {
            1200: {
                slidesPerView: 3,
            },
            768: {
                slidesPerView: 2,
            },
            575: {
                slidesPerView: 1,
            },
            0: {
                slidesPerView: 1,
            },
        },
    });

    /*clients-testimonial__slider***/
    let clients_testimonial__slider__slider = new Swiper(".clients-testimonial__slider", {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        centeredSlides: true,
        clickable: true,
        autoplay: {
            delay: 3000,
        },
        navigation: {
            prevEl: ".clients-testimonial__slider__arrow-prev",
            nextEl: ".clients-testimonial__slider__arrow-next",
        }
    });

    /*banner-2__slider***/
    let banner_2__slider = new Swiper(".banner-2__slider", {
        slidesPerView: 1,
        spaceBetween: 30,
        loop: true,
        centeredSlides: true,
        clickable: true,
        autoplay: {
            delay: 3000,
        },
        navigation: {
            prevEl: ".banner-2__slider__arrow-prev",
            nextEl: ".banner-2__slider__arrow-next",
        }
    });

    /* our-featured-service***/
    let our_featured_service__slider = new Swiper(".our-featured-service__active", {
        slidesPerView: 4,
        spaceBetween: 30,
        loop: true,
        clickable: true,
        autoplay: {
            delay: 3000,
        },
        navigation: {
            prevEl: ".our-featured-service__slider__arrow-prev",
            nextEl: ".our-featured-service__slider__arrow-next",
        },
        breakpoints: {
            1200: {
                slidesPerView: 4,
            },
            992: {
                slidesPerView: 2,
            },
            0: {
                slidesPerView: 1,
            },
        }
    });

    /* our-team__slider__slider***/
    let our_team__slider__slider = new Swiper(".our-team__slider", {
        slidesPerView: 3,
        spaceBetween: 30,
        loop: true,
        centeredSlides: true,
        clickable: true,
        autoplay: {
            delay: 3000,
        },
        navigation: {
            prevEl: ".our-team__slider__arrow-prev",
            nextEl: ".our-team__slider__arrow-next",
        },
        breakpoints: {
            1200: {
                slidesPerView: 3,
            },
            992: {
                slidesPerView: 2,
            },
            0: {
                slidesPerView: 1,
            },
        }
    });


    $('.grid').imagesLoaded(function () {
        var $grid = $('.grid').isotope({
            itemSelector: '.grid-item',
            layoutMode: 'fitRows'
        });

        $('.masonary-menu').on('click', 'button', function () {
            var filterValue = $(this).attr('data-filter');
            $grid.isotope({ filter: filterValue });
        });
        $('.masonary-menu button').on('click', function (event) {
            $(this).siblings('.active').removeClass('active');
            $(this).addClass('active');
            event.preventDefault();
        });
    });

    const instagramwiper = new Swiper('.rr-instagram-active', {
        // Optional parameters
        loop: true,
        slidesPerView: 5,
        autoplay: true,
        spaceBetween: 0,
        breakpoints: {
            '1400': {
                slidesPerView: 5,
            },
            '1200': {
                slidesPerView: 4,
            },
            '992': {
                slidesPerView: 3,
            },
            '768': {
                slidesPerView: 2,
            },
            '576': {
                slidesPerView: 2,
            },
            '0': {
                slidesPerView: 1,
            },

        },
    });


    /*======================================
     circle text 
    ========================================*/
    const text = document.querySelector(".circle-text");
    if (text) {
        text.innerHTML = text.innerText
            .split("")
            .map(
                (char, i) => `<span style="transform:rotate(${i * 8.5}deg)">${char}</span>`
            )
            .join("");
    }

    // Update-js =========================================================
    function createRotationAnimation(elementSelector, rotationAmount) {
        const elements = document.querySelectorAll(elementSelector);
        if (elements.length === 0) return; // Exit if no elements are found

        elements.forEach(element => {
            gsap.to(element, {
                rotation: rotationAmount,
                ease: "none",
                scrollTrigger: {
                    trigger: element,
                    start: "top 100%",
                    end: "bottom 1%",
                    scrub: 1,
                    toggleActions: "play reverse play reverse",
                    markers: false
                }
            });
        });
    }

    // Run the animation for all .rotating-image elements
    createRotationAnimation(".rotating-image", 180);


    // Apply the animation to elements with the selector
    //=========================================================
    function createZoomInAnimation(elementSelector) {
        const elements = document.querySelectorAll(elementSelector);
        if (elements.length === 0) return; // Exit if no elements are found

        elements.forEach(element => {
            gsap.fromTo(element,
                { scale: 0.5 }, // Start at 50% size
                {
                    scale: 1, // End at 100% size
                    ease: "none",
                    scrollTrigger: {
                        trigger: element,
                        start: "top 100%", // Adjust as needed
                        end: "top 60%",   // Adjust as needed
                        scrub: true,
                        toggleActions: "play reverse play reverse",
                        markers: false // Set to true if you want to see start/end markers for debugging
                    }
                }
            );
        });
    }

    createZoomInAnimation(".zoom-in-section");



    /*latest-project-2__active***/
    const latest_work__slider = new Swiper(".latest-project-2__active", {
        slidesPerView: 4,
        spaceBetween: 30,
        loop: true,
        clickable: true,
        centeredSlides: true,
        autoplay: {
            delay: 3000,
        },
        breakpoints: {
            '1200': {
                slidesPerView: 4,
            },
            '992': {
                slidesPerView: 3,
            },
            '768': {
                slidesPerView: 2,
            },
            '576': {
                slidesPerView: 2,
            },
            '0': {
                slidesPerView: 1,
            },
        },
    });

    /*======================================
    recent-project__active
    ========================================*/
    let client_slider__active = new Swiper(".client-slider__active", {
        loop: true,
        slidesPerView: 3,
        spaceBetween: 30,
        centeredSlides: false,
        autoplay: true,
        navigation: {
            prevEl: ".client-slider__slider__arrow-prev",
            nextEl: ".client-slider__slider__arrow-next",
        },
        autoplay: {
            delay: 3000,
        },
        initialSlide: 5,
        breakpoints: {
            1200: {
                slidesPerView: 3,
            },
            768: {
                slidesPerView: 2,
            },
            575: {
                slidesPerView: 1,
            },
            0: {
                slidesPerView: 1,
            },
        },
    });

    const rr_instagram_2_active = new Swiper('.rr-instagram-2-active', {
        // Optional parameters
        loop: true,
        slidesPerView: 5,
        autoplay: true,
        spaceBetween: 10,
        breakpoints: {
            '1200': {
                slidesPerView: 4,
            },
            '992': {
                slidesPerView: 3,
            },
            '768': {
                slidesPerView: 2,
            },
            '576': {
                slidesPerView: 2,
            },
            '0': {
                slidesPerView: 1,
            },

        },
    });

    /*======================================
    Banner-actve
    ========================================*/
    document.addEventListener('DOMContentLoaded', function () {
        // Select the elements
        let next = document.querySelector('.banner-4 .next');
        let prev = document.querySelector('.banner-4 .prev');
        let slideContainer = document.querySelector('.banner-4__slide');
        let items = document.querySelectorAll('.banner-4__item');
        let autoplayInterval;
        const autoplayDelay = 4000;
        const mobileWidth = 768;

        if (!next || !prev || !slideContainer || items.length === 0) {
            return;
        }

        function isMobileDevice() {
            return window.innerWidth <= mobileWidth;
        }

        function goToNextSlide() {
            items = document.querySelectorAll('.banner-4__item');
            slideContainer.appendChild(items[0]);
        }

        function goToPrevSlide() {
            items = document.querySelectorAll('.banner-4__item');
            slideContainer.prepend(items[items.length - 1]);
        }

        function startAutoplay() {
            if (!isMobileDevice()) {
                autoplayInterval = setInterval(goToNextSlide, autoplayDelay);
            }
        }

        function stopAutoplay() {
            clearInterval(autoplayInterval);
        }
        next.addEventListener('click', function () {
            stopAutoplay();
            goToNextSlide();
            startAutoplay();
        });

        prev.addEventListener('click', function () {
            stopAutoplay();
            goToPrevSlide();
            startAutoplay();
        });

        startAutoplay();

        window.addEventListener('resize', function () {
            if (isMobileDevice()) {
                stopAutoplay();
            } else {
                startAutoplay();
            }
        });
    });


    // Testi Carousel
    var testimonial_3_active = new Swiper(".testimonial-7-active", {
        slidesPerView: 2,
        spaceBetween: 10,
        // slidesPerGroup: 1,
        loop: true,
        autoplay: true,
        speed: 600,
        navigation: {
            nextEl: ".rr-button-next",
            prevEl: ".rr-button-prev",
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        breakpoints: {
            320: {
                slidesPerView: 1,
                slidesPerGroup: 1,
            },
            576: {
                slidesPerView: 2,
                slidesPerGroup: 1,
            },
            767: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            993: {
                slidesPerView: 3,
                slidesPerGroup: 1,
            },
            1200: {
                slidesPerView: 4,
                slidesPerGroup: 1,
            },
            1400: {
                slidesPerView: 4,
                slidesPerGroup: 1,
            },
        },
    });


    // Testi Carousel
    var testimonial_3_active = new Swiper(".testimonial-6-active", {
        slidesPerView: 2,
        spaceBetween: 10,
        loop: true,
        autoplay: true,
        speed: 600,
    
        navigation: {
            nextEl: ".rr-button-next",
            prevEl: ".rr-button-prev",
        },
    
        pagination: {
            el: ".testimonial-6-pagination",
            clickable: true,
            renderBullet: function (index, className) {
                let number = index + 1;
                return `<span class="${className}">${number}</span>`;
            },
        },
    
        breakpoints: {
            320: {
                slidesPerView: 1,
                slidesPerGroup: 1,
            },
        },
    });
    
    

    // Testi Carousel
    // Big Image Swiper
    const hero10BgImages = [
        "assets/imgs/update-2/banner/banner-10-bg-img.jpg",
        "assets/imgs/update-2/banner/banner-10-bg-img-3.jpg",
        "assets/imgs/update-2/banner/banner-10-bg-img-2.jpg",
    ];

    const hero10Wrapper = document.querySelector(".banner-10__wrapper");

    var hero10Swiper = new Swiper(".hero-10-active", {
        slidesPerView: 2,
        spaceBetween: 20,
        loop: true,
        speed: 800,
        autoplay: {
            delay: 4000,
            disableOnInteraction: false,
        },
        navigation: {
            nextEl: ".rr-button-next",
            prevEl: ".rr-button-prev",
        },
        breakpoints: {
            320: { slidesPerView: 2 },
            576: { slidesPerView: 2 },
            768: { slidesPerView: 3 },
            993: { slidesPerView: 3 },
        },
        on: {
            init: function () {
                setHeroBg(this);
                updateHero10Counter(this);
            },
            slideChange: function () {
                setHeroBg(this);
                updateHero10Counter(this);
            },
        },
    });

    function setHeroBg(swiper) {
        const index = swiper.realIndex;
        const bg = hero10BgImages[index];

        hero10Wrapper.classList.remove("bg-animating");

        // force reflow (important for animation restart)
        void hero10Wrapper.offsetWidth;

        hero10Wrapper.style.backgroundImage = `url(${bg})`;
        hero10Wrapper.classList.add("bg-animating");
    }

    function updateHero10Counter(swiper) {
        let current = swiper.realIndex + 1;
        document.querySelector(".hero-10-counter .current").innerHTML =
            current < 10 ? "0" + current : current;
    }


    /*======================================
    testimonial-3__active
    ========================================*/
    let testimonial_3__active = new Swiper(".testimonial-3__active", {
        loop: true,
        slidesPerView: 1,
        centeredSlides: false,
        autoplay: true,
        navigation: {
            prevEl: ".testimonial-3__slider__arrow-prev",
            nextEl: ".testimonial-3__slider__arrow-next",
        },
        autoplay: {
            delay: 3000,
        },
    });


    // 18. webgl images hover animation //
    if ($('.rr--hover-item').length) {
        let hoverAnimation__do = function (t, n) {
            let a = new hoverEffect({
                parent: t.get(0),
                intensity: t.data("intensity") || void 0,
                speedIn: t.data("speedin") || void 0,
                speedOut: t.data("speedout") || void 0,
                easing: t.data("easing") || void 0,
                hover: t.data("hover") || void 0,
                image1: n.eq(0).attr("src"),
                image2: n.eq(0).attr("src"),
                displacementImage: t.data("displacement"),
                imagesRatio: n[0].height / n[0].width,
                hover: !1
            });
            t.closest(".rr--hover-item").on("mouseenter", function () {
                a.next()
            }).on("mouseleave", function () {
                a.previous()
            })
        }
        let hoverAnimation = function () {
            $(".rr--hover-img").each(function () {
                let n = $(this);
                let e = n.find("img");
                let i = e.eq(0);
                i[0].complete ? hoverAnimation__do(n, e) : i.on("load", function () {
                    hoverAnimation__do(n, e)
                })
            })
        }
        hoverAnimation();
    }

    // pricing-4__active ----------------------------------
    let pricingMonthlyBtnn = $("#Monthly"),
        pricingYearlyBtnn = $("#Annually"),
        pricingValuess = $(".pricing-4__card__price h2, .yearly p");

    if (pricingMonthlyBtnn[0] && pricingYearlyBtn[0] && pricingValues.length > 0) {
        pricingMonthlyBtnn[0].addEventListener("click", function () {
            updatePricingValuestop("monthly");
            pricingYearlyBtn[0].classList.remove("active");
            pricingMonthlyBtnn[0].classList.add("active");
        });

        pricingYearlyBtn[0].addEventListener("click", function () {
            updatePricingValuestop("yearly");
            pricingMonthlyBtnn[0].classList.remove("active");
            pricingYearlyBtn[0].classList.add("active");
        });
    }

    function updatePricingValuestop(option) {
        pricingValues.each(function () {
            const pricingValue = $(this);
            const yearlyValue = pricingValue.attr("data-Annually");
            const monthlyValue = pricingValue.attr("data-Monthly");

            const newValue = option === "monthly" ? monthlyValue : yearlyValue;
            pricingValue.html(newValue);
        });
    }
    // --------------------------------------------------------------------------------------------
    const pricingSwitch = $("#checkbox"),
        pricingValues1 = $(".pricing-4__card__price h2");

    if (pricingSwitch[0] && pricingValues1.length > 0) {
        pricingSwitch[0].addEventListener("change", function () {
            if (pricingSwitch[0].checked) {
                updatePricingValues("yearly");
                $("#Annually").addClass("active");
                $("#Monthly").removeClass("active");
            } else {
                updatePricingValues("monthly");
                $("#Monthly").addClass("active");
                $("#Annually").removeClass("active");
            }
        });
    }

    function updatePricingValues(option) {
        pricingValues1.each(function () {
            const pricingValue = $(this);
            const yearlyValue = pricingValue.attr("data-Annually");
            const monthlyValue = pricingValue.attr("data-Monthly");

            const newValue = option === "monthly" ? monthlyValue : yearlyValue;
            pricingValue.html(newValue);
        });
    }

    // Home 10 about Animation
    const listItems = document.querySelectorAll(".about-section-8__list li");

    listItems.forEach((item) => {
        ScrollTrigger.create({
            trigger: item,
            start: "top 50%",
            end: "top 60%",
            onEnter: () => item.classList.add("active"),
            onLeaveBack: () => item.classList.remove("active"),
        });
    });


    // featured-6-active
    var featured6 = new Swiper(".featured-6-active", {
        slidesPerView: 2,
        spaceBetween: 20,
        loop: true,
        speed: 600,
        autoplay: true,
        pagination: {
            el: ".featured-pagination",
            clickable: true,
        },
        breakpoints: {
            320: { slidesPerView: 1 },
            576: { slidesPerView: 2 },
            993: { slidesPerView: 3 },
            1200: { slidesPerView: 4 },
            1400: { slidesPerView: 5 },
        },
    });
    



})(jQuery);