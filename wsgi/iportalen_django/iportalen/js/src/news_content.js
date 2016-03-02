/**
 * Created by jonathan on 2016-02-26.
 */
function get_news_content(url) {
    init_csrf();
    var container = $("#news-content");
    var tags = [];
    $('input[name="tags"]:checked').each(function(){
        tags.push(this.value);
    });
    var articles = $('#article-filter:checked').length;
    var events = $('#event-filter:checked').length;
    var sponsored = $('#sponsor-filter:checked').length;

    $.ajax({
        "type": "POST",
        "url": url,
        "data": {'tags[]': tags, articles: articles, events: events, sponsored: sponsored },
        "success": function (result) {
            container.html(result);
        }
    });
}

function expander_trigger_news_page(url) {
    $('.expander-trigger').click(function(){
        $('.expander-content').slideToggle( "fast" );
        $(this).toggleClass("expander-hidden");
    });
    get_news_content(url);
    $('#sponsored_feed_container').show();
    $(function() {
        $('#sponsored_feed_content').vTicker();
    });
}