function user_cart(){
    $.get('/displaycart',function (res){
        const cartDisplay = document.getElementById('items');
        let total = 0
        let temp_contain =""
        for (const product of res){
            const info = '<br/>' + 'Product: ' + product['product_name'] + '<br/>' +
                'Price: ' + product['product_price'] + '<br/>';
            total = total+ parseInt(product['product_price'])
            temp_contain = temp_contain + '<button onclick="delete_from_cart(' + product['_id'] + ');"><img src="/' + product['product_image'] + '" width="300" height="300">' + info + '</button>';

        }
        temp_contain= temp_contain+ '<br/>'+'Total: '+ total +'<br/>' +'<button onclick="checkout();">checkout</button>';
        cartDisplay.innerHTML = temp_contain
    })
}

function delete_from_cart(product_id) {
        const formData = new FormData();
        formData.append('delete_id', product_id);
        let total = 0
        const new_display = document.getElementById('items');
        let temp_contain =""
      $.ajax({
            url: '/delete_from_cart',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (res) {

                for (const product of res) {
                const info = '<br/>' + 'Product: ' + product['product_name'] + '<br/>' +
                'Price: ' + product['product_price'] + '<br/>';
                total = total+ parseInt(product['product_price'])

                temp_contain = temp_contain+ '<button onclick="delete_from_cart(' + product['_id'] + ');"><img src="/' + product['product_image'] + '" width="300" height="300">' + info + '</button>';

        }
        temp_contain= temp_contain+ '<br/>'+'Total: '+ total +'<br/>' +'<button onclick="checkout();">checkout</button>';
        new_display.innerHTML = temp_contain
            }
        })
}
function addToCart(product_id){
     const formData = new FormData();
     formData.append('add_id', product_id);

      $.ajax({
            url: '/add_to_cart',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (res) {
              alert(res)
            }
        })

}
function checkout(){
    $.get('/checkout_cart',function (res){
        const check_out = document.getElementById('items');
        check_out.innerHTML= "<br/>"+res
    })

}







