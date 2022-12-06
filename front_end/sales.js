function getSales() {
    $.get('/get_sales', function (products) {
        const forSaleDisplay = document.getElementById('forSale');
        const soldDisplay = document.getElementById('sold');
        const forSale = products['for_sale'];
        const sold = products['sold'];
        for (const product of forSale) {
             if (product['auction_end_time'] == null) {
                 forSaleDisplay.innerHTML +=
                     '<table>' +
                     '<tr>' +
                     '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
                     '<td>Name: ' + product['product_name'] + '<br>' +
                     'Description: ' + product['product_description'] + '<br>' +
                     'Price: ' + parseFloat(product['product_price']).toFixed(2) + '</td>' +
                     '</tr>' +
                     '</table>';
             } else {
                 forSaleDisplay.innerHTML =
                     '<table>' +
                     '<tr>' +
                     '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
                     '<td>Name: ' + product['product_name'] + '<br>' +
                     'Description: ' + product['product_description'] + '<br>' +
                     'Auction Deadline: ' + product['auction_end_time'].replace('T', ' ') + '</td>' +
                     '</tr>' +
                     '</table>';
             }
        }
        for (const product of sold) {
            if (product['auction_end_time'] == null) {
                soldDisplay.innerHTML +=
                    '<table>' +
                    '<tr>' +
                    '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
                    '<td>Name: ' + product['product_name'] + '<br>' +
                    'Description: ' + product['product_description'] + '<br>' +
                    'Price: ' + parseFloat(product['product_price']).toFixed(2) + '</td>' +
                    '</tr>' +
                    '</table>';
            } else {
                soldDisplay.innerHTML =
                    '<table>' +
                    '<tr>' +
                    '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
                    '<td>Name: ' + product['product_name'] + '<br>' +
                    'Description: ' + product['product_description'] + '<br>' +
                    'Price: ' + parseFloat(product['product_price']).toFixed(2) + '<br>' +
                    'Auction Deadline: ' + product['auction_end_time'].replace('T', ' ') + '</td>' +
                    '</tr>' +
                    '</table>';
            }
        }
    })
}