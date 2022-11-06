$('#createBtn').click(function() {
    const files = $('#imageInput')[0].files;
    const name = $('#nameInput').val();
    const description = $('#descriptionInput').val();
    const price = $('#priceInput').val();
    if (files.length > 0 && name.length > 0 && description.length > 0 && price.length > 0) {
        if (price.match(/^\d+(.)?\d{1,2}$/)) {
            const image = files[0];
            const formData = new FormData();
            formData.append('image', image);
            formData.append('name', name)
            formData.append('description', description);
            formData.append('price', price);
            $.ajax({
                url: '/create',
                method: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function (res) {
                    alert(res)
                    $('#imageInput').val('');
                    $('#nameInput').val('');
                    $('#descriptionInput').val('');
                    $('#priceInput').val('');
                }
            })
        } else {
            document.getElementById('error').innerHTML = 'Please enter a proper price.';
        }
    } else {
        document.getElementById('error').innerHTML = 'Please provide image, name, description, and price.';
    }
})


function get_all_products() {
    $.get('/get-all-products', function (products) {
        const productsDisplay = document.getElementById('products');
        for (const product of products) {
            productsDisplay.innerHTML += 'image' + product['product_image'] + '</br>' +
                'product: ' + product['product_name'] + '<br/>' +
                'descroption: ' + product['product_description'] + '<br/>' +
                'price: ' + product['product_price'] + '<br/>' + '<br/>';
        }
    })
}

