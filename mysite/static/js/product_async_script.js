window.onload = function () {
    $('.products-conteiner').on('click', 'input[type="button"]', function () {
        let target_href = event.target.closest("div").querySelector('.quantity-num');

        if (target_href) {
            $.ajax({
                url: "/basket/add/" + target_href.name + "/" + target_href.value + "/",

                success: function (data) {
                    $('.sign-in-position').html(data.result);
                    $('.quantity-num').html(target_href.value=0);
                },
            });
        }
        event.preventDefault();
    });
}