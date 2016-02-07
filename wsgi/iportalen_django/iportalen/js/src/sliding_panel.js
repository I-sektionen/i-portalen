/**
 * Created by MagnusForzelius on 2015-10-31.
 */

var sliding_panel = function (){
    $('.sliding-panel-button,.sliding-panel-fade-screen,.sliding-panel-close').on('click touchstart',function (e) {
        $('.sliding-panel-content,.sliding-panel-fade-screen').toggleClass('is-visible');
        e.preventDefault();
    });
};