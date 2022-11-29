function getOrders() {
    $.get('/get_orders', function (products) {
        const ordersDisplay = document.getElementById('orders');
        for (const product of products) {
             ordersDisplay.innerHTML +=
                 '<table>' +
                 '<tr>' +
                 '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
                 '<td>Name: ' + product['product_name'] + '<br>' +
                 'Description: ' + product['product_description'] + '<br>' +
                 'Price: ' + product['product_price'] + '</td>' +
                 '</tr>' +
                 '</table>';
        }
    })
}