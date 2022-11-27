function infoPage(product_id) {
    $.get('/get_one_product/' + product_id, function (product) {
        const infoDisplay = document.getElementById('info');
        infoDisplay.innerHTML =
            '<table>' +
            '<tr>' +
            '<td><img src="/' + product['product_image'] + '" width="300" height="300"></td>' +
            '<td>Name: ' + product['product_name'] + '<br>' +
            'Description: ' + product['product_description'] + '<br>' +
            'Price: ' + product['product_price'] + '<br>' +
            '<button onclick="addToCart(' + product_id + ');">Add to Cart</button>' + '<br>' +
            '<button onclick="buyNow(' + product_id + ');">Buy Now</button></td>' +
            '</tr>' +
            '</table>';
    })
}


function buyNow(product_id) {
    $.get('/buy_now/' + product_id, function (res) {
        if (res == 'Not Logged In') {
            location.href = '/login'
        } else {
            alert(res)
            location.href = '/'
        }
    })
}