$('#Submit').click(function() {

    const Account = $('#CartAccount').val();
    const Password = $('#CartPassword').val();


    if (Account.length > 0 && Password.length > 0 ) {
            const formData = new FormData();
            formData.append('id', Account);
            $.ajax({
            url: '/checkinfor',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (res) {
                eppass= res["password"]
                }
            });
        if (Password===eppass) {
            $.ajax({
                url: '/showcart',
                method: 'GET',
                data: formData,
                contentType: false,
                processData: false,
                success: function (res) {

                    $('#CartAccount').val('');
                    $('#CartPassword').val('');
                }
            })
        } else {
            document.getElementById('error').innerHTML = 'Incorrect Account or Password';

        }
    } else {
        document.getElementById('error').innerHTML = 'Please provide a valid account and password';

    }
})



