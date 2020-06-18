function filterProduct(products, filter) {
    let afterProducts = [];
    for (const product of products) {
        let name = $(product).find("a.name-product").text();
        let price = $(product).find("span.price-product").text();

        price = price.replace(",", ".");
        name = name.toLowerCase();

        afterProducts.push(
            {
                'name': name,
                'price': parseFloat(price),
                'block': product
            }
        );
    }
    if (filter === "price_increasing") {
        afterProducts.sort(function (a, b) {
            if (a.price < b.price) {
                return -1;
            } else if (a.price > b.price) {
                return 1;
            }
        });
    } else if (filter === "price_decreasing") {
        afterProducts.sort(function (a, b) {
            if (a.price < b.price) {
                return 1;
            } else if (a.price > b.price) {
                return -1;
            }
        });
    } else if (filter === "a_to_z") {
        afterProducts.sort(function (a, b) {
            if (a.name < b.name) {
                return -1;
            } else if (a.name > b.name) {
                return 1;
            }
        });
    } else if (filter === "z_to_a") {
        afterProducts.sort(function (a, b) {
            if (a.name < b.name) {
                return 1;
            } else if (a.name > b.name) {
                return -1;
            }
        });
    }

    return afterProducts;
}

function refreshScreenProducts(container, spinner, products) {
    container.fadeOut('slow', function () {
        spinner.fadeIn('slow');
        setTimeout(function () {
            for (let i = 0; i < products.length; i++) {
                container.append(products[i].block);
            }
            spinner.fadeOut('slow', function () {
                container.fadeIn('slow');
            });
        }, 2000);
    });
}

$(document).ready(function () {
    let btnValidFilter = $('#btnValidFilter');
    let spinner = $('#spinner');
    
    btnValidFilter.on('click', function () {
        let wrapper = $('#wrapper');
        let allProducts = wrapper.find('div.active').children().children();
        let filter = $('#selectFilter').val();
        let products = filterProduct(allProducts, filter);
        let contentAllProducts = wrapper.find('div.active').children()

        refreshScreenProducts(contentAllProducts, spinner, products);
        
    });

});