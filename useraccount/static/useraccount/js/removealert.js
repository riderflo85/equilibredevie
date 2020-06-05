$(document).ready(function () {
    let alerts = [
        'alertChangePwd',
        'alertFailChangePwd',
        'alertChangeUserInfos',
        'alertFailChangeUserInfos',
        'alertErrorForm'
    ]

    for (const alert of alerts) {
        $(`#${alert} > button`).on('click', function () {
            $(`#${alert}`).removeClass('show');
        });
    }

});