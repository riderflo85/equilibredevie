$(document).ready(function () {
    let alerts = [
        'alertChangePwd',
        'alertFailChangePwd',
        'alertChangeUserInfos',
        'alertFailChangeUserInfos',
        'alertErrorForm',
        'alertSubscribe',
        'alertFailSubscribe',
        'alertUnsubscribe',
        'alertFailUnsubscribe'
    ]

    for (const alert of alerts) {
        $(`#${alert} > button`).on('click', function () {
            $(`#${alert}`).removeClass('show');
        });
    }

});