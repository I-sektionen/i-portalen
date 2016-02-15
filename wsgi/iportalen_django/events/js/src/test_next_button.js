/**
 * Created by jers on 15/02/16.
 */
function next_button() {
    console.log('hej');
    var $tabs = $('.accordion-tabs li');
    $tabs.filter('.active').next('li').tab('show');
}

function prev_button() {
    var $tabs = $('.accordion-tabs li');

    $tabs.filter('.active').prev('li').tab('show');
}