/**
 * Created by elonbrange on 16-03-06.
 */

/**
 * Created by jonathan on 2015-11-09.
 */
function remove_noshow(button, url, user_id, event_id) {
    init_csrf();

        console.log(user_id, event_id)
        var data = {
            'user_id': user_id,
            'event_id': event_id
        };
        $.ajax({
            "type": "POST",
            "dataType": "json",
            "url": url,
            "data": data,
            "success": function (result) {

                if(result.status==='OK'){
                    $(button).closest('li').remove()
                     message_iportalen('success', 'No show borttagen');
                }
                else{
                     message_iportalen('error', result.status);

                }

            },
            error: function (request, status, error) {
                message_iportalen('error', request.responseText);
            }
        });

}