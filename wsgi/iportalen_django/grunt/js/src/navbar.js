/*global $*/
$(document).ready(function () {
    'use strict';
    var menuToggle = $('#menu-toggle').unbind();
    var navigationMenu = $('#navigation-menu').removeClass('show');
    var submenuWrapper = $('#submenu-wrapper').removeClass('show');

    $('li.more').click(function(e){
        e.preventDefault()

        $(this).children('.submenu-wrapper').slideToggle('fast')


    })

    menuToggle.on('click', function (event) {
        event.preventDefault();
        navigationMenu.toggleClass('show');
    });

    /*
    $('#navigation-menu > li.more').on('touchstart click', function (event) {
        event.stopPropagation();
        event.preventDefault();
        // Prevents the doubleclick (hover and click on the first click) while on touchdevices
        if(event.handled !== true) {
            if (!$(event.target).closest('.submenu-wrapper').length && $('.submenu-wrapper').hasClass("show")) {
                closeSubMenu();
                console.log("Closing submenu click");
            } else {
                // I can't use the openSubMenu since "this" dosen't follow with it -
                // might work on a solution on this later
                //openSubMenu();

                $(".submenu-wrapper").removeClass("show");
                $(this).children(".submenu-wrapper").addClass("show");
                console.log("Opening submenu click");
            }
            event.handled = true;
        } else {
            return false;
        }
    });
*/

});
