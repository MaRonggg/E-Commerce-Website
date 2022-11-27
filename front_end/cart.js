function delete_from_cart(product_image) {
        const formData = new FormData();
        formData.append('image', product_image);
      $.ajax({
            url: '/delete_from_cart',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (res) {
                alert("deleted")
            }
        })
}

$('#checkout').click(function() {
        $.ajax({
            url: '/checkout_cart',
            method: 'GET',
            contentType: false,
            processData: false,
            success: function (res) {
                alert("bought")
            }
        })
})




