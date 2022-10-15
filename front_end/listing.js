

$('#createBtn').click(function() {
    const files = $('#imageInput')[0].files;
    const description = $('#descriptionInput').val();
    const price = $('#priceInput').val();
    if (files.length > 0 && description.length > 0 &&price.length > 0) {
        if (price.match(/^\d{1,}$/)) {
            const image = files[0];
            const formData = new FormData();
            formData.append('image', image);
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
                    $('#descriptionInput').val('');
                    $('#priceInput').val('');
                }
            })
        } else {
         alert('Please enter a proper price.')
        }
    } else {
        alert('Please provide image, description, and price.')
    }
})
