$(document).ready(function () {
    let inputPwd = $("#id_pwd");
    let pwd;

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
        } else {
            this.classList.add('is-invalid');
        }
    });
});