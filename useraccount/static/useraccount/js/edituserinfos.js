$(document).ready(function () {
    let btnEditUserInfos = $('#changeInfosUser');
    let btnValidEdit = $('#confirmInfosUser');
    let btnCancelEdit = $('#cancel');
    let prependInfos = $('#titleInfosUser').children();
    let inputPhoneNumber = $('#id_phone_number');
    let inputPostalCode = $('#id_postal_code');
    let alerts = [
        $('#alertChangeUserInfos'),
        $('#alertFailChangeUserInfos'),
        $('#alertErrorForm')
    ]
    let phoneNumberValid = true;
    let postalCodeValid = true;

    btnEditUserInfos.on('click', function () {
        let count = 0;
    
        $('#contentUserInfos').hide(500, function () {
            $('#contentFormUserInfos').show(500);
            for (const el of prependInfos) {
                if (count === 0) {
                    el.classList.add('size-edit-first');
                } else if (count === 4) {
                    el.classList.add('mb-5', 'mmt-4');
                } else if (count === 5) {
                    el.classList.add('d-none');
                } else {
                    el.classList.add('size-edit');
                }
                count++;
            }
        });
    
        $('#changeInfosUser').hide(500, function () {
            $('#cancel').show(500);
            $('#confirmInfosUser').show(500);
        });
    });

    btnCancelEdit.on('click', function () {
        let count = 0;

        $('#contentFormUserInfos').hide(500, function () {
            $('#contentUserInfos').show(500);
            for (const el of prependInfos) {
                if (count === 0) {
                    el.classList.remove('size-edit-first');
                } else if (count === 4) {
                    el.classList.remove('mb-5', 'mmt-4', 'size-edit');
                } else if (count === 5) {
                    el.classList.remove('d-none');
                } else {
                    el.classList.remove('size-edit');
                }
                count++;
            }
        });
    
        $('#cancel').hide(500, function () {
            $('#changeInfosUser').show(500);
        });
        $('#confirmInfosUser').hide(500);
        alerts[2].removeClass('show');
    });


    inputPhoneNumber.on('keyup', function () {
        if (this.value.length < 10 || this.value.length > 10) {
            this.classList.add('is-invalid');
            phoneNumberValid = false;
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
            phoneNumberValid = true;
        }
    });

    inputPostalCode.on('keyup', function () {
        if (this.value.length < 5 || this.value.length > 5) {
            this.classList.add('is-invalid');
            postalCodeValid = false;
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
            postalCodeValid = true;
        }
    });


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

    btnValidEdit.on('click', function () {
        let allData = {};
        let error = false;

        block_send_data: {
            for (const field of $('#contentFormUserInfos > div > input')) {
                if (field.id === "id_phone_number") {
                    if (!phoneNumberValid) {
                        error = true;
                        break block_send_data;
                    } else {
                        allData[field.id] = field.value;
                    }
                } else if (field.id === "id_postal_code") {
                    if (!postalCodeValid) {
                        error = true;
                        break block_send_data;
                    } else {
                        allData[field.id] = field.value;
                    }
                } else {
                    allData[field.id] = field.value;
                }
            }
            console.log(allData);
            
            $.ajax({
                url: '/user/change_infos/',
                type: 'POST',
                dataType: 'json',
                data: allData,
                success: function (res) {
                    if (res['success']) {
                        alerts[1].removeClass('show');
                        alerts[2].removeClass('show');
                        alerts[0].addClass('show');
                        for (const field of $('#contentFormUserInfos > div > input')) {
                            field.setAttribute('disabled', true);
                        }
                        setTimeout(function() {
                            document.location.reload(true);
                        }, 5000);
                    } else {
                        alerts[0].removeClass('show');
                        alerts[2].removeClass('show');
                        alerts[1].addClass('show');
                    }
                },
                error: function (err) {
                    console.warn(err);
                }
            });
        }

        if (error) {
            alerts[2].addClass('show');
        }
    });

});