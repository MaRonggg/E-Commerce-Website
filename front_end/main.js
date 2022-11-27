function getAllProducts() {
    $.get('/get_all_products', function (products) {
        const productsDisplay = document.getElementById('products');
        for (const product of products) {
            const info = '<br/>' + 'Product: ' + product['product_name'] + '<br/>' +
                'Price: ' + product['product_price'] + '<br/>';

            productsDisplay.innerHTML += '<button onclick="toInfoPage(' + product['_id'] + ');"><img src="/' + product['product_images'] + '" width="300" height="300">' + info + '</button>';
        }
    })
}


function toInfoPage(product_id) {
    location.href = '/info_page/' + product_id;
}








