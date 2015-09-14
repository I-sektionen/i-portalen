/*global $*/
$(document).ready(function () {
    'use strict';
    var menuToggle = $('#menu-toggle').unbind();
    var navigationMenu = $('#navigation-menu').removeClass('show');
    var submenuWrapper = $('.submenu-wrapper').removeClass('show');

    menuToggle.on('click', function (event) {
        event.preventDefault();
        navigationMenu.toggleClass('show');
        console.log("menuToggle click");
    });

    $('#navigation-menu > li').on('touchstart click', function (event) {
        event.stopPropagation();
        event.preventDefault();
        // Prevents the doubleclick while on touchdevices
        if(event.handled !== true) {
            if ($(".submenu-wrapper").hasClass("show")) {
                closeSubMenu();
            } else {
                // I can't use the openSubMenu since "this" dosen't follow with it -
                // might work on a solution on this later
                //openSubMenu();

                $(".submenu-wrapper").removeClass("show");
                $(this).children(".submenu-wrapper").addClass("show");
            }
            event.handled = true;
        } else {
            return false;
        }
    });

    // Works the hover aspect while not on a mobile device
    $('#navigation-menu > li ').hover(openSubMenu);


    function openSubMenu() {
        closeSubMenu();
        $(this).children(".submenu-wrapper").addClass('show');
    };

    function closeSubMenu() {
        $(".submenu-wrapper").removeClass("show");
    };

    // Closes the hover aspect of the menu when mouse gets on another part of the page
    $(".nav-bar").on('mouseover', closeSubMenu);
    $('.hero').on('mouseover', closeSubMenu);

});
