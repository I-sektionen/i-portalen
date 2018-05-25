
$(document).ready(function() {
  var js_nav_menu = $('#js-navigation-alumni-portal-menu');
  var menuToggle = $('#js-mobile-alumni-portal-menu').unbind();
  js_nav_menu.removeClass("show");

  menuToggle.on('click', function(e) {
    e.preventDefault();
    js_nav_menu.slideToggle(function(){
      if(js_nav_menu.is(':hidden')) {
        js_nav_menu.removeAttr('style');
      }
    });
  });
});