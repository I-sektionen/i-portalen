/**
 * Created by jonathan on 2016-01-15.
 */
function cookiemonster() {
    if (Cookies.get('SKVCookieAlert')) {
        jQuery('.alertWrp').hide();
    } else {
        jQuery('.alertWrp').fadeIn('slow');
    }
    jQuery('#cookieClose').click(function(){
       jQuery('.alertWrp').fadeOut('slow');
        Cookies.set('SKVCookieAlert', 'agree', { expires: 300, path: '/' });
    });
}
