(function() {
    function scrollHorizontally(e) {
        e = window.event || e;
        let delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
        document.getElementById('yourDiv').scrollLeft -= (delta*80); // Multiplied by 40
        e.preventDefault();
    }
    if (document.getElementById('yourDiv').addEventListener) {
        // IE9, Chrome, Safari, Opera
        document.getElementById('yourDiv').addEventListener("mousewheel", scrollHorizontally, false);
        // Firefox
        document.getElementById('yourDiv').addEventListener("DOMMouseScroll", scrollHorizontally, false);
    } else {
        // IE 6/7/8
        document.getElementById('yourDiv').attachEvent("onmousewheel", scrollHorizontally);
    }
    })();