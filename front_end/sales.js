function getSales() {
    $.get('/get_sales', function (products) {
        const salesDisplay = document.getElementById('sales');
        for (const product of products) {
             salesDisplay.innerHTML +=
                 '<table>' +
                 '<tr>' +
                 '<td><img src="/' + product['product_images'] + '" width="300" height="300"></td>' +
                 '<td>Name: ' + product['product_name'] + '<br>' +
                 'Description: ' + product['product_description'] + '<br>' +
                 'Price: ' + product['product_price'] + '</td>' +
                 '</tr>' +
                 '</table>';
        }
    })
}