$(document).ready(function () {
    let alerts = [
        'alertChangePwd',
        'alertFailChangePwd',
        'alertChangeUserInfos',
        'alertFailChangeUserInfos'
    ]

    for (const alert of alerts) {
        $(`#${alert} > button`).on('click', function () {
            $(`#${alert}`).removeClass('show');
        });
    }

});