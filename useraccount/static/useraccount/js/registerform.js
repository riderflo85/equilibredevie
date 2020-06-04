$(document).ready(function () {

    let inputPwd = $("#id_password");
    let inputEmail = $("#id_email");
    let pwd;

    /* Update the content form */
    $("span").remove();
    $("br").remove();
    $("input").addClass('form-control');
    $("select").addClass('form-control mb-4');
    inputEmail.after("<p class='mb-3'><small class='text-muted'>Merci de renseigner une adresse email valide.</small></p>");
    inputEmail.addClass('mb-1');
    inputPwd.attr('minlength', '8');
    inputPwd.after("<p class='mb-3'><small class='text-muted'>Le mot de passe doit faire au minimum 8 characters.</small></p>");
    inputPwd.addClass('mb-1');
    document.getElementById('id_first_name').required = true;
    document.getElementById('id_last_name').required = true;
    document.getElementById('id_password').type = "password";
    document.getElementById('id_phone_number').pattern = "^0+[0-9]{1}[0-9]{2}[0-9]{2}[0-9]{2}[0-9]{2}";
    document.getElementById('id_postal_code').pattern = "[0-9]{5}";
    /* ************************ */

    /* If error in the form */
    try {
        $('ul').addClass('text-danger');
        let errorMsg = document.getElementById('errorForm').getAttribute('data-error-form');

        if (errorMsg === "mot de passe non identique") {
            $('#id_confirm_password').addClass('is-invalid');
        }
    } catch (e) {
        //pass
    }
    /* ******************* */

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

    $('#id_confirm_password').on('keyup', function () {
        if (pwd === this.value) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        } else {
            this.classList.add('is-invalid');
        }
    });


    $('#id_phone_number').on('keyup', function () {
        console.log(this.value.length);
        if (this.value.length <= 9 || this.value.length >= 11) {
            this.classList.add('is-invalid');
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
        
    });

    $('#id_postal_code').on('keyup', function () {
        console.log(this.value.length);
        if (this.value.length <= 4 || this.value.length >= 6) {
            this.classList.add('is-invalid');
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }

    });
});