function expander_trigger_exchange_portal(url) {
    $('.expander-trigger').click(function(){
        $('.expander-content').slideToggle( "fast" );
        $(this).toggleClass("expander-hidden");
    });
}

// Click-function for the dropdwon. When someone clicks on the dropdown-btn, the content for that dropdown will show.
$(".dropdown-btn").on('click', function() {
  $(this).parent().children(".dropdown-content").slideToggle('fast');
});

$(document).click(function(){
  $(".dropdown-content").hide();
});

$(".dropdown-btn").click(function(e){
  e.stopPropagation();
});




$(".button_exchange_portal").on('click', function(event) {
  $(".button_exchange_portal").removeClass("current");
  $(event.target).addClass("current");
  if(event.target.id == "courses_button") {
    $("#travel_stories").addClass("hidden");
    $("#courses_section").removeClass("hidden");
  } else if (event.target.id == "travel_stories_button") {
    $("#travel_stories").removeClass("hidden");
    $("#courses_section").addClass("hidden");
  } else if (event.target.id == "links_button") {

  }
});


function sortTable(table_id, n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById(table_id);
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.getElementsByTagName("TR");
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

$(document).ready(function() {
  var js_nav_menu = $('#js-navigation-exchange-portal-menu');
  var menuToggle = $('#js-mobile-exchange-portal-menu').unbind();
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
;