$(document).ready(function () {
    let btnValidCheckout = $('#validCheckout');
    let csrftoken = getCookie('csrftoken');
    let cartNotEmpty = $('#noneProductInCart');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    if (cartNotEmpty.length === 1) {
        btnValidCheckout.attr('disabled', true);
    }

    btnValidCheckout.on('click', function () {
        let lastName = $('#formLastName');
        let firstName = $('#formFirstName');
        let adress = $('#formAdress');
        let city = $('#formCity');
        let dep = $('#formDep');
        let postalCode = $('#formPostalCode');
        let email = $('#formEmail');
        let phoneNumber = $('#formPhoneNumber');
        let note = $('#checkout-mess');
        let checkOtherAdress = $('#ship-box:checked').length;
        let checkData = false;
        let dataForm = {
            'last_name': lastName,
            'first_name': firstName,
            'adress': adress,
            'city': city,
            'dep': dep,
            'postal_code': postalCode,
            'email': email,
            'phone_number': phoneNumber,
            'note': note,
            'another_adress': false,
        };

        if (checkOtherAdress === 1) {
            dataForm['another_adress'] = true;
            dataForm['anLN'] = $('#AnotherFormLN');
            dataForm['anFN'] = $('#AnotherFormFN');
            dataForm['anAd'] = $('#AnotherFormAd');
            dataForm['anCi'] = $('#AnotherFormCi');
            dataForm['anDe'] = $('#AnotherFormDe');
            dataForm['anCP'] = $('#AnotherFormCP');
            dataForm['anEm'] = $('#AnotherFormEm');
            dataForm['anPN'] = $('#AnotherFormPN');
        }

        bloc_for: {
            for (const [key, val] of Object.entries(dataForm)) {
                if (key != "another_adress") {
                    if (val[0].id != "checkout-mess") {
                        if (val.val() === "") {
                            val.addClass("is-invalid");
                            checkData = false;
                            break bloc_for;
                        } else {
                            dataForm[key] = val.val();
                            checkData = true;
                        }
                    } else {
                        dataForm[key] = val.val();
                    }
                }
            }
        }

        
        if (checkData && cartNotEmpty.length === 0) {
            this.setAttribute('disabled', true);
            this.innerHTML = "VALIDATION EN COURS...<span class='ml-3 spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>";

            setTimeout(function() {
                $.ajax({
                    url: '/order/',
                    type: 'POST',
                    dataType: 'json',
                    data: dataForm,
                });
            }, 2000);
        }

    });
});