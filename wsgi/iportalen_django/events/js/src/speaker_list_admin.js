/**
 * Created by jonathan on 2015-11-09.
 */
function speaker_list_admin(url){
    init_csrf();
    var input_field = $("#id_speech_nr");
    var s_list = $("#list").find("ol");
    $("#post").click(function(e) {
        e.preventDefault();
        var data = {
            'method':'add',
            'speech_nr': input_field.val()
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
        input_field.val('');
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
    $("#remove").click(function(e) {
        e.preventDefault();
        var data = {
            'method':'remove',
            'speech_nr': input_field.val()
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
        input_field.val('');
    });
}