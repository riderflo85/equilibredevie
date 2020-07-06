$(document).ready(function () {
    let select = $('#id_filter_choice').children();
    let categ = $('#categSelected').data('categ');
    let inputCateg = $('#id_filter_categ');

    console.log('test', categ.length);
    if (categ.length > 0) {
        inputCateg.attr('value', categ);
    } else {
        inputCateg.attr('disabled', true);
    }

    $(select[0]).attr('disabled', true);
});