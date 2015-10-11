/*global $*/
$(document).ready(function () {
    'use strict';
    var menuToggle = $('#menu-toggle').unbind();
    var navigationMenu = $('#navigation-menu').removeClass('show');
    var submenuWrapper = $('.submenu-wrapper').removeClass('show');

    menuToggle.on('click', function (event) {
        event.preventDefault();
        navigationMenu.toggleClass('show');
    });


    $('#navigation-menu > li ').on('click', function (event) {
        // Does NOT prevents the doubleclick (hover and click on the first click) while on touchdevices
        if (!$(event.target).closest('.submenu-wrapper').length && $('.submenu-wrapper').hasClass("show")) {
            closeSubMenu();
        } else {
            // I can't use the openSubMenu since "this" dosen't follow with it -
            // might work on a solution on this later
            //openSubMenu();

            $(".submenu-wrapper").removeClass("show");
            $(this).children(".submenu-wrapper").addClass("show");
        }
    });

    // Works the hover aspect while not on a mobile device
    $('#navigation-menu > li').hover(openSubMenu);

    function openSubMenu() {
        if (!$(this).children(".submenu-wrapper").hasClass("show")){
            closeSubMenu();
            $(this).children(".submenu-wrapper").addClass('show');
        }
    };

    function closeSubMenu() {
        if ($(".submenu-wrapper").hasClass("show")){
            $(".submenu-wrapper").removeClass("show");
        };
    };

    // Closes the hover aspect of the menu when mouse gets on another part of the page
    $(".nav-bar").on('mouseover', closeSubMenu);
    $('.hero').on('mouseover', closeSubMenu);

    /*
    This was supposed to be a solution to the double-hover-click
    But I can only either get the submenus on touch-devi to work
    or the submenus on non-touch.. Need to look into this some more
    but right now it is best to just have a need for doube-touch while
    on a mobile device
    */
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
