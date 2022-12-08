function getAllOnSaleProducts() {
    $.get('/get_all_on_sale_products', function (products) {
        const productsDisplay = document.getElementById('products');
        for (const product of products) {
            if (product['auction_end_time'] == null) {
                const info = '<br/>' + 'Product: ' + product['product_name'] + '<br/>' +
                'Price: ' + parseFloat(product['product_price']).toFixed(2) + '<br/>';

                productsDisplay.innerHTML += '<button onclick="toInfoPage(' + product['_id'] + ');"><img src="/' + product['product_image'] + '" width="300" height="300">' + info + '</button>';
            } else {
                const info = '<br/>' + 'Product: ' + product['product_name'] + '<br/>' +
                'Auction Deadline: ' + product['auction_end_time'] + '<br/>';

                productsDisplay.innerHTML += '<button onclick="toInfoPage(' + product['_id'] + ');"><img src="/' + product['product_image'] + '" width="300" height="300">' + info + '</button>';
            }
        }
    })
}


function toInfoPage(product_id) {
    location.href = '/info_page/' + product_id;
}








