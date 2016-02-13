/**
 * Created by jonathan on 2015-11-09.
 */
function speaker_list_view(url) {
    init_csrf();

    var s_list = $("#speaker_list").find("ol");
    var t=setInterval(reload_list, 1000);
    function reload_list() {

        var data = {
            'method': 'all'
        };
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": url,
            "data": data,
            "success": function (result) {
                if (result.status === "ok") {
                    var speakerlist = result.speaker_list;
                    var arrayLength = speakerlist.length;
                    s_list.empty();
                    for (var i = 0; i < arrayLength; i++) {
                        s_list.append('<li>' + speakerlist[i].first_name + ' ' + speakerlist[i].last_name + '</li>');
                    }
                } else {
                    console.log(result.status);
                }
            }
        });
    }
}