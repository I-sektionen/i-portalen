/**
 * Created by isac on 2016-01-17.
 */
$(document).ready(function () {
    var tabs = $('.accordion-tabs');
  tabs.each(function(index) {
      //The original code line from bourbon refils:
      //$(this).children('li').first().children('a').addClass('is-active').next().addClass('is-open').show();
      //Was changed to this. (This searches for is-active and activates this tab.
      $(this).children('li').each(function(index){
          if($(this).children('a').hasClass('is-active')){
              $(this).children('a').addClass('is-active').next().addClass('is-open').show();
              return false;
          }
      });
      //End changes.

  });
  tabs.on('click', 'li > a.tab-link', function(event) {
    if (!$(this).hasClass('is-active')) {
      event.preventDefault();
      var accordionTabs = $(this).closest('.accordion-tabs');
      accordionTabs.find('.is-open').removeClass('is-open').hide();

      $(this).next().toggleClass('is-open').toggle();
      accordionTabs.find('.is-active').removeClass('is-active');
      $(this).addClass('is-active');
    } else {
      event.preventDefault();
    }
  });
});