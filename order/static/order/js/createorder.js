$(document).ready(function () {
    let btnValidCheckout = $('#validCheckout');

    btnValidCheckout.on('click', function () {
        let lastName = $('#formLastName').val();
        let firstName = $('#formFirstName').val();
        let adress = $('#formAdress').val();
        let city = $('#formCity').val();
        let dep = $('#formDep').val();
        let postalCode = $('#formPostalCode').val();
        let email = $('#formEmail').val();
        let phoneNumber = $('#formPhoneNumber').val();
        let checkOtherAdress = $('#ship-box').val();
    });
});