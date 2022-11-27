function user_cart(){
    $.get('/displaycart',function (res){
        const cartDisplay = document.getElementById('items');
        let total = 0
        for (const product of res) {

            const info = '<br/>' + 'Product: ' + product['product_name'] + '<br/>' +
                'Price: ' + product['product_price'] + '<br/>';
            total = total+ parseInt(product['product_price'])
            cartDisplay.innerHTML += '<button onclick="delete_from_cart(' + product['_id'] + ');"><img src="/' + product['product_images'] + '" width="300" height="300">' + info + '</button>';
        }
        cartDisplay.innerHTML+= '<br/>'+'Total: '+ total +'<br/>'
        cartDisplay.innerHTML += '<button onclick="checkout();"> </button>';
    })
}

function delete_from_cart(product_id) {
        const formData = new FormData();
        formData.append('delete_id', product_id);
        const new_display = document.getElementById('items');
      $.ajax({
            url: '/delete_from_cart',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (res) {
                let totalprice = 0
                for (const product of res) {

                const info = '<br/>' + 'Product: ' + product['product_name'] + '<br/>' +
                'Price: ' + product['product_price'] + '<br/>';
                totalprice = totalprice+ parseInt(product['product_price'])
                new_display.innerHTML += '<button onclick="delete_from_cart(' + product['_id'] + ');"><img src="/' + product['product_images'] + '" width="300" height="300">' + info + '</button>';
                }
                new_display.innerHTML+= '<br/>'+'Total: '+ totalprice +'<br/>'
                new_display.innerHTML += '<button onclick="checkout();"> </button>';
            }
        })
}
function addToCart(product_id){
     const formData = new FormData();
     formData.append('add_id', product_id);
     const add_display = document.getElementById('items');
      $.ajax({
            url: '/add_to_cart',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (res) {
                let totalprice = 0
                for (const product of res) {

                const info = '<br/>' + 'Product: ' + product['product_name'] + '<br/>' +
                'Price: ' + product['product_price'] + '<br/>';
                totalprice = totalprice+ parseInt(product['product_price'])
                add_display.innerHTML += '<button onclick="delete_from_cart(' + product['_id'] + ');"><img src="/' + product['product_images'] + '" width="300" height="300">' + info + '</button>';
                }
                add_display.innerHTML+= '<br/>'+'Total: '+ totalprice +'<br/>'
                add_display.innerHTML += '<button onclick="checkout();"> </button>';
            }
        })

}
function checkout(){
    $.get('/checkout_cart',function (res){
        const check_out = document.getElementById('items');
        check_out.innerHTML+= "<br/>"+res
    })

}








