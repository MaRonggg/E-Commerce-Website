function checkImage() {
    const files = $('#imageInput')[0].files;
    const flag = files.length > 0;
    return flag;
}


document.getElementById('nameInput').onblur = checkName;
function checkName() {
    const name = $('#nameInput').val().trim();
    const flag = name.length > 0;
    if (flag) {
        document.getElementById('name_error').style.display = 'none';
    } else {
        document.getElementById('name_error').style.display = '';
    }
    return flag;
}


document.getElementById('descriptionInput').onblur = checkDescription;
function checkDescription() {
    const description = $('#descriptionInput').val().trim();
    const flag = description.length > 0;
    if (flag) {
        document.getElementById('description_error').style.display = 'none';
    } else {
        document.getElementById('description_error').style.display = '';
    }
    return flag;
}


document.getElementById('priceInput').onblur = checkPrice;
function checkPrice() {
    const price = $('#priceInput').val().trim();
    const flag = price.match(/^\d+(.\d{1,2})?$/);
    if (flag) {
        document.getElementById('price_error').style.display = 'none';
    } else {
        document.getElementById('price_error').style.display = '';
    }
    return flag;
}


$('#createBtn').click(function() {
    if (checkImage() && checkName() && checkDescription() && checkPrice()) {
        const image = $('#imageInput')[0].files[0];
        const name = $('#nameInput').val();
        const description = $('#descriptionInput').val();
        const price = $('#priceInput').val();
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
    }
})

