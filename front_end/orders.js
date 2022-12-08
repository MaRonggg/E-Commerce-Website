function getOrders() {
    $.get('/get_orders', function (products) {
        const ordersDisplay = document.getElementById('orders');
        for (const product of products) {
             if (product['auction_end_time'] == null) {
                 ordersDisplay.innerHTML +=
                     '<table>' +
                     '<tr>' +
                     '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
                     '<td>Name: ' + product['product_name'] + '<br>' +
                     'Description: ' + product['product_description'] + '<br>' +
                     'Price: ' + parseFloat(product['product_price']).toFixed(2) + '</td>' +
                     '</tr>' +
                     '</table>';
             } else {
                 ordersDisplay.innerHTML +=
                     '<table>' +
                     '<tr>' +
                     '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
                     '<td>Name: ' + product['product_name'] + '<br>' +
                     'Description: ' + product['product_description'] + '<br>' +
                     'Price: ' + parseFloat(product['product_price']).toFixed(2) + '<br>' +
                     'Auction Deadline: ' + product['auction_end_time'] + '</td>' +
                     '</tr>' +
                     '</table>';
             }
        }
    })
}