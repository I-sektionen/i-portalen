/**
 * Created by jonathan on 2015-11-09.
 */
function speaker_list_view(url) {
    init_csrf();

    var s_list = $("#list ol");
    var t=setInterval(reload_list, 3000);
    function reload_list() {

        var data = {
            'method': 'all',
        };
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": url,
            "data": data,
            "success": function (result) {
                if (result.status === "ok") {
                    console.log(result.status);
                } else {
                    console.log(result.status);
                }
            }
        });
        $("#id_speech_nr").val('');
    }
}