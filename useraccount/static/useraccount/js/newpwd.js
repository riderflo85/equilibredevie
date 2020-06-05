function sendNewPwd(validSend, pwd) {
    let btnValid = $('#changePwd');
    let alerts = [
        $('#alertChangePwd'),
        $('#alertFailChangePwd'),
    ]

    // ************* see the secureajax.js file for more details ******************************
    let csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // ****************************************************************************************

    if (validSend) {
        
        btnValid.on('click', function () {
            $.ajax({
                url: '/user/change_pwd/',
                type: 'POST',
                dataType: 'json',
                data: {'new_pwd': pwd},
                success: function (res) {
                    if (res['success']) {
                        alerts[0].addClass('show');
                        setTimeout(function() {
                            document.location.reload(true);
                        }, 5000);
                    } else {
                        alerts[1].addClass('show');
                    }
                },
                error: function (err) {
                    console.warn(err);
                }
            });
        });
    }
}


$(document).ready(function () {
    let inputPwd = $("#id_pwd");
    let pwd;
    let validSend = false;


    inputPwd.on('keyup', function () {
        if (this.value.length <= 7) {
            this.classList.add('is-invalid');
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });

    inputPwd.on('blur', function () {
        pwd = this.value;
    });

    $('#id_confirm_pwd').on('keyup', function () {
        if (pwd === this.value) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
            validSend = true;
            sendNewPwd(validSend, this.value);
        } else {
            this.classList.add('is-invalid');
        }
    });
});