(function() {
    function scrollHorizontally(e) {
        e = window.event || e;
        let delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
        document.querySelector('.scroll-similar-products').scrollLeft -= (delta*80);
        e.preventDefault();
    }
    if (document.querySelector('.scroll-similar-products').addEventListener) {
        // IE9, Chrome, Safari, Opera
        document.querySelector('.scroll-similar-products').addEventListener("mousewheel", scrollHorizontally, false);
        // Firefox
        document.querySelector('.scroll-similar-products').addEventListener("DOMMouseScroll", scrollHorizontally, false);
    } else {
        // IE 6/7/8
        document.querySelector('.scroll-similar-products').attachEvent("onmousewheel", scrollHorizontally);
    }
    })();