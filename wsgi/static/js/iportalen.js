/*global $*/
$(document).ready(function () {
    'use strict';
    var menuToggle = $('#menu-toggle').unbind();
    var navigationMenu = $('#navigation-menu').removeClass('show');
    var submenuWrapper = $('.submenu-wrapper').removeClass('show');

    $('#navigation-menu > li.more a').on('mouseover', openSubMenu);
    $('#navigation-menu > li.more a').on('mouseout', openSubMenu);

    menuToggle.on('mouseover', openSubMenu);
    menuToggle.on('mouseout', openSubMenu);

    function openSubMenu() {
        //$(this).next().toggleClass('show');
        $(this).find('ul').toggleClass('show');
    }

/*    menuToggle.on('mouseover', function (event) {
        event.preventDefault();
        navigationMenu.toggleClass('show');
    });

    $('li.more a').on('mouseover', function (event) {
        event.preventDefault();
        $(this).next().toggleClass('show');
    });
    */

/*    menuToggle.hover(
        function (event) {
        event.preventDefault();
        navigationMenu.toggleClass('show');
    }, function (event) {
        event.preventDefault();
        navigationMenu.toggleClass('show');
    });

    $('li.more a').hover(function (event) {
        event.preventDefault();
        $(this).next().toggleClass('show');
    }, function (event) {
        event.preventDefault();
        $(this).next().toggleClass('show');
    });
*/
});
