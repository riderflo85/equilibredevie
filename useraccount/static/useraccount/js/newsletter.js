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

function actualiseNewsletterButton (state) {
    let unsubscribeBtn = `<button type="button" class="btn-user-unsubscribe btn-hover ml-2" id="unsubscribeNewsletter">Se désincrire de la newsletter <i class="fas fa-envelope"></i></button>`;

    let subscribeBtn = `<button type="button" class="btn-user-account btn-hover ml-2" id="subscribeNewsletter">S'inscrire à la newsletter <i class="fas fa-envelope-open-text"></i></button>`;

    let allButtons = $('#boxButton').children();

    $(allButtons[0]).remove();

    if (state['subscribe']) {
        $('#changePwd').before(unsubscribeBtn);
    } else {
        $('#changePwd').before(subscribeBtn);
    }
}

function subscribe () {
    let alerts = [
        $('#alertSubscribe'),
        $('#alertFailSubscribe')
    ]

    $.ajax({
        url: '/user/newsletter/',
        type: 'POST',
        dataType: 'json',
        data: {'state': 'subscribe'},
        success: function (res) {
            if (res['success']) {
                // display an success alert. (success alert for subscribe is done.)
                alerts[0].addClass('show');
                actualiseNewsletterButton({'subscribe': true });
            } else {
                // display an error alert
                alerts[1].addClass('show');
            }
        },
        error: function (err) {
            console.warn(err);
        }
    });
}

function unsubscribe () {
    let alerts = [
        $('#alertUnsubscribe'),
        $('#alertFailUnsubscribe'),
    ]

    $.ajax({
        url: '/user/newsletter/',
        type: 'POST',
        dataType: 'json',
        data: { 'state': 'unsubscribe' },
        success: function (res) {
            if (res['success']) {
                // display an success alert. (success alert for unsubscribe is done.)
                alerts[0].addClass('show');
                actualiseNewsletterButton({'subscribe': false});
            } else {
                // display an error alert
                alerts[1].addClass('show');
            }
        },
        error: function (err) {
            console.warn(err);
        }
    });
}


$(document).ready(function () {
    let btnSubscribeNewsletter = $('#subscribeNewsletter');
    let btnUnsubscribeNewsletter = $('#unsubscribeNewsletter');

    if (btnSubscribeNewsletter.length > 0) {
        btnSubscribeNewsletter.on('click', function () {
            subscribe();
        });
    }

    if (btnUnsubscribeNewsletter.length > 0) {
        btnUnsubscribeNewsletter.on('click', function () {
            unsubscribe();
        });
    }

});