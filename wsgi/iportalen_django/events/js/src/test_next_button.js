
function next_button() {
    var $tabs = $('.accordion-tabs li');
    console.log("hej " + $tabs);
    $tabs.filter('.active').next('li').tab('show');
}

function prev_button() {
    var $tabs = $('.accordion-tabs li');

    $tabs.filter('.active').prev('li').tab('show');
}