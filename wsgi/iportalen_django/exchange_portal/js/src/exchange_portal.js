function expander_trigger_exchange_portal(url) {
    $('.expander-trigger').click(function(){
        $('.expander-content').slideToggle( "fast" );
        $(this).toggleClass("expander-hidden");
    });
}

// Click-function for the dropdwon. When someone clicks on the dropdown-btn, the content for that dropdown will show.
$(".dropdown-btn").on('click', function() {
  $(this).parent().children(".dropdown-content").slideToggle('fast');
});

$(document).click(function(){
  $(".dropdown-content").hide();
});

$(".dropdown-btn").click(function(e){
  e.stopPropagation();
});
