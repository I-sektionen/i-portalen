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
            $('.expander-trigger').addClass("expander-hidden");
            container.html(result);
        }
    });
}