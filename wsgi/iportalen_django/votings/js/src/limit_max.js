/**
 * Created by jers on 11/02/16.
 */

function limit_max_choice(choices, max){
    $(choices).on('change',function(evt){
        if($(choices+':checked').length>max){
            this.checked=false
        }
    });
}