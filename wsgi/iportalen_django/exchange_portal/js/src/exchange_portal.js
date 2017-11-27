function expander_trigger_exchange_portal(url) {
    $('.expander-trigger').click(function(){
        $('.expander-content').slideToggle( "fast" );
        $(this).toggleClass("expander-hidden");
    });
}