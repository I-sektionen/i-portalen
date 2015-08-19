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

    $('li.more a').on('click', function (event) {
        event.preventDefault();
        $(this).next().toggleClass('show');
    });
});
