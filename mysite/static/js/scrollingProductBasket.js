(function() {
    function scrollHorizontally(e) {
        e = window.event || e;
        let delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
        document.querySelector('.posiciton-basket-record-conteiner').scrollLeft -= (delta*100);
        e.preventDefault();
    }
    if (document.querySelector('.posiciton-basket-record-conteiner').addEventListener) {
        // IE9, Chrome, Safari, Opera
        document.querySelector('.posiciton-basket-record-conteiner').addEventListener("mousewheel", scrollHorizontally, false);
        // Firefox
        document.querySelector('.posiciton-basket-record-conteiner').addEventListener("DOMMouseScroll", scrollHorizontally, false);
    } else {
        // IE 6/7/8
        document.querySelector('.posiciton-basket-record-conteiner').attachEvent("onmousewheel", scrollHorizontally);
    }
    })();