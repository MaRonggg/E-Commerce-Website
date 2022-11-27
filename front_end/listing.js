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
        document.getElementById('nameError').style.display = 'none';
    } else {
        document.getElementById('nameError').style.display = '';
    }
    return flag;
}


document.getElementById('descriptionInput').onblur = checkDescription;
function checkDescription() {
    const description = $('#descriptionInput').val().trim();
    const flag = description.length > 0;
    if (flag) {
        document.getElementById('descriptionError').style.display = 'none';
    } else {
        document.getElementById('descriptionError').style.display = '';
    }
    return flag;
}


document.getElementById('auctionCheckInput').addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById('priceInput').disabled = true;
        document.getElementById('auctionDeadlineInput').disabled = false;
    } else {
        document.getElementById('priceInput').disabled = false;
        document.getElementById('auctionDeadlineInput').disabled = true;
    }
})


document.getElementById('priceInput').onblur = checkPrice;
function checkPrice() {
    const price = $('#priceInput').val().trim();
    const flag = price.match(/^\d+\.\d{2}$/);
    if (flag) {
        document.getElementById('priceError').style.display = 'none';
    } else {
        document.getElementById('priceError').style.display = '';
    }
    return flag;
}


document.getElementById('auctionDeadlineInput').onblur = checkAuctionDeadline;
function checkAuctionDeadline() {
    const auctionDeadline = $('#auctionDeadlineInput').val()
    const flag = auctionDeadline.length > 0;
    if (flag) {
        document.getElementById('auctionDeadlineError').style.display = 'none';
    } else {
        document.getElementById('auctionDeadlineError').style.display = '';
    }
    return flag;
}


$('#createBtn').click(function() {
    const auctionChecked = document.getElementById('auctionCheckInput').checked;
    if (!auctionChecked) {
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
    } else {
        if (checkImage() && checkName() && checkDescription() && checkAuctionDeadline()) {
            const image = $('#imageInput')[0].files[0];
            const name = $('#nameInput').val();
            const description = $('#descriptionInput').val();
            const auctionDeadline = $('#auctionDeadlineInput').val();
            const formData = new FormData();
            formData.append('image', image);
            formData.append('name', name)
            formData.append('description', description);
            formData.append('auction_deadline', auctionDeadline);
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
                    $('#auctionDeadlineInput').val('');
                }
            })
        }
    }
})

