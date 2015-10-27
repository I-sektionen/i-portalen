function markdown_event_preview() {
        var converter = Markdown.getSanitizingConverter();
        converter.hooks.chain("preConversion", function (text) {
            return text.replace(/[&<"'\/]/g, function (s) {
                var entityMap = {
                    "&": "&amp;",
                    "<": "&lt;",
                    '"': '&quot;',
                    "'": '&#39;',
                    "/": '&#x2F;'
                };
                return entityMap[s];
            }).replace(/([#]{2,})/g, '#').replace(/([=]{3,})/g, '').replace(/([-]{3,})/g, '').replace(/([`])/g, '');
        });
        converter.hooks.chain("plainLinkText", function (url) {
            return url.replace(/^https?:\/\//, "");
        });
        var editor = new Markdown.Editor(converter, "-body");
        editor.run();
    }
/**
 * This function
 * 1. Starts the markdown engine.
 * 2. Add event listeners on the forms.
 */
var article_preview = function () {
    //Start the engines. Listens to the body and outputs.
    console.log("Call on meeeee");
    markdown_event_preview();
    console.log("Call on me");

    //These are the elements that is being listened to.
    var listened_to = [];
    var headline = $("#id_headline");
    var lead = $("#id_lead");
    var author = $("#id_author");
    var from = $("#id_visible_from");
    var tags = $("#id_tags");

    //This is the elements where the results are printed to.
    var headline_preview = $(".headline_preview");
    var lead_preview = $(".lead_preview");
    var author_preview = $(".author_preview");
    var from_preview_date = $(".date_preview");
    var tags_preview = $(".tags_preview");

    listened_to.push(
                    [headline, headline_preview],
                    [lead, lead_preview],
                    [author, author_preview],
                    [from, from_preview_date],
                    [tags, tags_preview]
    );

    var render = function (){
        console.log("Bamm.");
        jQuery.each(listened_to, function(index, element){
            var txt;

            //Special case of start-time:
            if(element[0].is(from)) {
                if (element[0].val() != "") {
                    var d = element[0].val().split(" ");
                    var date = d[0];
                    element[1].text(date);
                }
            } else if(element[0].is(tags)){
                var selected_tags = tags.children().filter(":selected");
                var tag_string = "";
                jQuery.each(selected_tags, function(index, ele){
                    tag_string = tag_string + ele.innerHTML + ", ";
                });
                if(tag_string != ""){
                    tag_string = tag_string.substring(0, tag_string.length-2)
                }
                element[1].text(tag_string);

            } else {
                txt = element[0].val();
                element[1].text(txt);
            }
        });
    };

    jQuery.each(listened_to, function(index, element){
        var ele = element[0];
        ele.change(function(){render()});
        ele.keypress(function(){render()});
    });
};