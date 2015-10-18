/*global $*/
$(document).ready(function () {
    'use strict';
    var menuToggle = $('#menu-toggle').unbind();
    var navigationMenu = $('#navigation-menu').removeClass('show');
    var submenuWrapper = $('#submenu-wrapper').removeClass('show');
    var userPanelCheckbox = $('#user-panel-checkbox')

    if ($(window).width() < 900) {
        $('li.more').click(function (e) {
            e.preventDefault()
            $(this).children('.submenu-wrapper').slideToggle('fast')
        })
    }
    menuToggle.on('click', function (event) {
        event.preventDefault();
        navigationMenu.toggleClass('show');
    });

    /**
    $('#user-panel-toggle').click(function () {
        console.log("hello")
        userPanelCheckbox.prop("checked", !checkBoxes.prop("checked"));
    })**/

});
