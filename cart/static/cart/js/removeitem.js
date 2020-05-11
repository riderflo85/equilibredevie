$(document).ready(function () {
    let csrftoken = getCookie('csrftoken');
    let countItems = document.getElementById('countItemsCart')

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    
    for (const item of $('.cart-delete')) {
        
        item.addEventListener('click', function () {
            let quantity = this.getAttribute('data-quantity');
            let idItem =this.getAttribute('data-id-product');

            $.ajax({
                url: `/panier/remove_mini_cart/${idItem}/`,
                type: 'GET',
                success: function (res) {
                    if (res['success']) {
                        let newCount = (Number(countItems.textContent) - Number(quantity)).toString();
                        $(`#product${idItem}`).slideUp('slow', function () {
                            countItems.textContent = newCount;
                            if (newCount === "0") {
                                let baliseEmptyCart = "<li class='single-product-cart' id='newContentCartNoItem' style='display: none;'><h4>Votre panier est vide</h4></li>";
                                $(baliseEmptyCart).prependTo($("#contentCart"));
                                $('#newContentCartNoItem').slideDown('slow');
                                $('#btnCheckout').fadeOut('slow');

                            }
                        });
                    }
                    
                },
                error: function (err) {
                    console.warn(err);
                },
            });
        });
    }

});