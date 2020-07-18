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

// Ajouter une fonction qui actualise le bouton

$(document).ready(function () {
    let btnSubscribeNewsletter = $('#subscribeNewsletter');
    let btnUnsubscribeNewsletter = $('#unsubscribeNewsletter');

    if (btnSubscribeNewsletter.length > 0) {
        btnSubscribeNewsletter.on('click', function () {
            // execute subscribe function
            subscribe();
        });
    }

    if (btnUnsubscribeNewsletter.length > 0) {
        btnUnsubscribeNewsletter.on('click', function () {
            // execute unsubscribe function
            unsubscribe();
        });
    }

});