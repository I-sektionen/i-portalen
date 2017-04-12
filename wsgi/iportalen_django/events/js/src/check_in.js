/**
 * Created by jonathan on 2015-11-09.
 */
function check_in_admin(url){
    init_csrf();
    var input_field = $("#id_user");
    var force_field = $("#id_force_check_in");
    var s_list = $("#list").find("ol");
    var submit_btn = $("#submit-button");
    var msg_box = $("#message-box");

    submit_btn.click(function(e) {
        submit_btn.prop("disabled", true);
        e.preventDefault();
        var data = {
            'user': input_field.val(),
            'force_check_in': force_field.is(":checked")
        };
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": url,
            "data": data,
            "success": function(result) {
                msg_box.empty();
                message_iportalen(result.status, result.message);
                force_field.prop('checked', false);
                submit_btn.prop("disabled", false);
            }
        });
        input_field.val('');
    });
}

