/**
 * Created by jonathan on 2016-01-15.
 */
function son_of_the_devil() {
    var ua = window.navigator.userAgent;

    var msie = ua.indexOf('MSIE ');
    if (msie > 0) {
        // IE 10 or older => return version number
        return true;
    }

    var trident = ua.indexOf('Trident/');
    if (trident > 0) {
        // IE 11 => return version number
        var rv = ua.indexOf('rv:');
        return true;
    }
    var edge = ua.indexOf('Edge/');
    if (edge > 0) {
       // Edge (IE 12+) => return version number
       return true;
    }
    // other browser
    return false;
}
function closeDevilMessage(element){
    $(element).parent().hide();
    Cookies.set('DevilsBrowser', 'agree', { expires: 7, path: '/' });
}
try {
   if (son_of_the_devil() && !(Cookies.get('DevilsBrowser'))){
        jQuery('#message-box').append('<div class="warning"><span>Du använder en osupportad webbläsare</span><button type="button" onclick="closeDevilMessage(this)">&times;</button></div>')
    }
}
catch(err) {
    jQuery('#message-box').append('<div class="warning"><span>Du använder en osupportad webbläsare</span><button type="button" onclick="closeDevilMessage(this)">&times;</button></div>')
}

