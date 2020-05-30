$(document).ready(function () {
    let btnEditUserInfos = $('#changeInfosUser');
    let btnValidEdit = $('#confirmInfosUser');
    let btnCancelEdit = $('#cancel');
    let prependInfos = $('#titleInfosUser').children();

    btnEditUserInfos.on('click', function () {
        let count = 0;
    
        $('#contentUserInfos').hide(500, function () {
            $('#contentFormUserInfos').show(500);
            for (const el of prependInfos) {
                if (count === 0) {
                    el.classList.add('size-edit-first');
                } else if (count === 5) {
                    el.classList.add('d-none');
                } else {
                    el.classList.add('size-edit');
                }
                count++;
            }
        });
    
        $('#changeInfosUser').hide(500, function () {
            $('#cancel').show(500);
            $('#confirmInfosUser').show(500);
        });
    });

    btnCancelEdit.on('click', function () {
        let count = 0;

        $('#contentFormUserInfos').hide(500, function () {
            $('#contentUserInfos').show(500);
            for (const el of prependInfos) {
                if (count === 0) {
                    el.classList.remove('size-edit-first');
                } else if (count === 5) {
                    el.classList.remove('d-none');
                } else {
                    el.classList.remove('size-edit');
                }
                count++;
            }
        });
    
        $('#cancel').hide(500, function () {
            $('#changeInfosUser').show(500);
        });
        $('#confirmInfosUser').hide(500);
    });
});