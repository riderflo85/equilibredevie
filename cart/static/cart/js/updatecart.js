function getProductQuantity(productsInCart) {
    let products = '';

    for (const product of productsInCart) {
        let id = product.getAttribute('data-id-product');
        let value = product.children[0].value;
        products = products + `${id},${value}`;
        products = products + '|';
    }
    return products;
}



$(document).ready(function () {

    let csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#btnUpdateCart').on('click', function () {
        let productQuantity = getProductQuantity($('.block-form-update'));

        $.ajax({
            url: '/panier/update/',
            type: 'POST',
            dataType: 'json',
            data: {'data': productQuantity},
            success: function (res) {
                if (res['success']) {
                    document.location.reload();
                } else {
                    document.location.reload();
                }
            },
            error: function (err) {
                console.warn(err);
            },
        });
    });

});