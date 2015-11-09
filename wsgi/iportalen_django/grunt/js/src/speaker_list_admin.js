/**
 * Created by jonathan on 2015-11-09.
 */
function speaker_list_admin(url){
    init_csrf();

    var s_list = $("#list ol");
    $("#post").click(function(e) {
        e.preventDefault();
        var data = {
            'method':'add',
            'speech_nr': $("#id_speech_nr").val()
        };
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": url,
            "data": data,
            "success": function(result) {
                if (result.status === "ok"){

                    console.log(result.first_name);
                    console.log(result.last_name);
                    s_list.append('<li>' + result.first_name + ' ' + result.last_name + '</li>');
                } else {
                    console.log(result.status);
                }
            }
        });
        $("#id_speech_nr").val('');
    });
    $("#next").click(function(e) {
        e.preventDefault();
        s_list.find('li:first').remove();
        var data = {
            'method':'pop'
        };
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": url,
            "data": data,
            "success": function(result) {
                if (result.status === "ok"){

                } else {
                    console.log(result.status);
                }
            }
        });
    });
    $("#clear").click(function(e) {
        e.preventDefault();
        s_list.empty();
        var data = {
            'method':'clear'
        };
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": url,
            "data": data,
            "success": function(result) {
                if (result.status === "ok"){

                } else {
                    console.log(result.status);
                }
            }
        });
    });
}