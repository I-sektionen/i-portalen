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
    console.log(tags);
    $.ajax({
        "type": "POST",
        "url": url,
        "data": {'tags[]': tags},
        "success": function (result) {
            container.html(result);
        }
    });
}