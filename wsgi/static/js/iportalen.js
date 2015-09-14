/*global $*/
$(document).ready(function () {
    'use strict';
    var menuToggle = $('#menu-toggle').unbind();
    var navigationMenu = $('#navigation-menu').removeClass('show');
    var submenuWrapper = $('.submenu-wrapper').removeClass('show');

    menuToggle.on('mouseover', openSubMenu);
    $('#navigation-menu > li').on('mouseover', openSubMenu);
    $(".nav-bar").on('mouseover', closeSubMenu);
    $('.hero').on('mouseover', closeSubMenu);

    function openSubMenu() {
        $(".submenu-wrapper").removeClass("show");
        //closeSubMenu();
        $(this).children(".submenu-wrapper").addClass('show');
        //$(this).find('ul').toggleClass('show');
    };

    function closeSubMenu() {
        $(".submenu-wrapper").removeClass("show");
    };

});
