/*global $*/
$(document).ready(function () {
    'use strict';
    var menuToggle = $('#menu-toggle').unbind();
    var navigationMenu = $('#navigation-menu').removeClass('show');
    var submenuWrapper = $('#submenu-wrapper').removeClass('show');
    var userPanelCheckbox = $('#user-panel-checkbox');

    if ($(window).width() < 900) {  //TODO: Breakout global vars.
        $('li.more>a').click(function (e) {
            e.preventDefault();
        });
        $('li.more').click(function (e) {
            console.log("li.more");
            $(this).children('.submenu-wrapper').slideToggle('fast');
        })
    }
    menuToggle.on('click', function (event) {
        event.preventDefault();
        navigationMenu.slideToggle('fast');
    });

    /**
    $('#user-panel-toggle').click(function () {
        console.log("hello")
        userPanelCheckbox.prop("checked", !checkBoxes.prop("checked"));
    })**/

});
