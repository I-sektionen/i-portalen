/**
 * Created by andreas on 09/11/15.
 */
$(document).ready(function() {
  var menuToggle = $('#js-centered-navigation-mobile-menu').unbind();
  var js_center_nav_menu = $('#js-centered-navigation-menu');
  js_center_nav_menu.removeClass("show");

  menuToggle.on('click', function(e) {
    e.preventDefault();
    js_center_nav_menu.slideToggle(function(){
      if(js_center_nav_menu.is(':hidden')) {
        js_center_nav_menu.removeAttr('style');
      }
    });
  });
});

