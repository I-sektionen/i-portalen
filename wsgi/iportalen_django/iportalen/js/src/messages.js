/**
 * Created by elonbrange on 16-03-06.
 */

function message_iportalen(message_type, message){
    var message = '<div class="'+message_type+'"><span>'+message+'</span> <button type="button" onclick="closeMessage(this)">&times;</button> </div>'
    $('#message-box').append(message);
}