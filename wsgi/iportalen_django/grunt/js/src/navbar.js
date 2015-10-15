/*global $*/
$(document).ready(function () {
    'use strict';
    var menuToggle = $('#menu-toggle').unbind();
    var navigationMenu = $('#navigation-menu').removeClass('show');
    var submenuWrapper = $('.submenu-wrapper').removeClass('show');
    var mainMenuMore =

    menuToggle.on('click', function (event) {
        event.preventDefault();
        navigationMenu.toggleClass('show');
    });
});
