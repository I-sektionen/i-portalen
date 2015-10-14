//This function initiates the markdown engine. It is called on by event_preview below.
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
var event_preview = function () {
    //Start the engines. Listens to the body and outputs.
    console.log("Call on meeeee");
    markdown_event_preview();
    console.log("Call on me");

    //These are the elements that is being listened to.
    var listened_to = [];
    var headline = $("#id_headline");
    var lead = $("#id_lead");
    var place = $("#id_location");
    var start = $("#id_start");
    var end = $("#id_end");
    var enable_registration = $("#id_enable_registration");
    var free_places = $("#id_registration_limit");

    //This is the elements where the results are printed to.
    var lead_preview = $("#lead_preview");
    var headline_preview = $(".headline_preview");
    var place_preview = $(".place_preview");
    var start_preview_date = $(".start_preview_date");
    var start_preview_time = $(".start_preview_time");
    var end_preview = $("#id_end_preview");
    var enable_registration_preview = $(".enable_registration_preview");
    var free_places_preview = $("#id_registration_limit_preview");

    listened_to.push([headline, headline_preview],
                    [lead, lead_preview],
                    [place, place_preview],
                    [start, [start_preview_time, start_preview_date]],
                    [end, end_preview],
                    [enable_registration, enable_registration_preview],
                    [free_places, free_places_preview]
    );
    enable_registration_preview.hide();
    var render = function (){
        console.log("Bamm.");
        jQuery.each(listened_to, function(index, element){
            var txt;

            //Special case of start-time:
            if(element[0].is(start)) {
                if(element[0].val() != ""){
                    var d = element[0].val().split(" ");
                    var date = d[0];
                    var time = "Kl. " + d[1];
                    element[1][0].text(time);
                    element[1][1].text(date);
                }

                //Special case of
            } else if(element[0].is(enable_registration)){
                if(element[0].is(":checked")){
                  element[1].show();
                  console.log("1");
              } else {
                  element[1].hide();
                  console.log("0");
              }
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

    /**
    var txt=headline.val();
    $("#headline_collapsed").text(txt);
    $("#headline_expanded").text(txt);
    headline.keyup(function(event) {
        var txt=$(this).val();
        $("#headline_collapsed").text(txt);
        $("#headline_expanded").text(txt);
    });
    txt=headline.val();
    lead_collapsed.text(txt);
    $("#lead_expanded").text(txt);
    var wordCounts = {};
    lead.keyup(function(event) {
        var number = 0;
        var matches = $(this).val().match(/\b/g);
        if (matches) {
            number = matches.length / 2;
        }
        wordCounts[this] = number;
        var finalCount = 0;
        $.each(wordCounts, function(k, v) {
            finalCount += v;
        });
        var txt=$(this).val();
        if (finalCount<=50){
            lead_collapsed.text(txt);
        }
        $("#lead_expanded").text(txt);
    });

    var fullDate = new Date();
    var twoDigitMonth = fullDate.getMonth()+"";
    if(twoDigitMonth.length==1){
        twoDigitMonth="0" +twoDigitMonth;
    }
    var twoDigitDate = fullDate.getDate()+"";
    if(twoDigitDate.length==1){
        twoDigitDate="0" +twoDigitDate;
    }
    var currentDate = fullDate.getFullYear() + "-" + twoDigitMonth + "-" + twoDigitDate;
    $("#date_collapsed").text(currentDate);
    $("#date_expanded").text(currentDate);

    var author = $("#id_author");
    txt=author.val();
    $("#author_collapsed").text(txt);
    $("#author_expanded").text(txt);

    author.keyup(function(event) {
        var txt=$(this).val();
        $("#author_collapsed").text(txt);
        $("#author_expanded").text(txt);
    });
     */
};



/**
function displayVals() {
    var multipleValues = $("#id_tags option:selected").map(function() {
        return $(this).text();
    }).get();
    $( "#tags_collapsed" ).html( multipleValues.join( ", " ) );
    $( "#tags_expanded" ).html( multipleValues.join( ", " ) );
}
$( "select" ).change( displayVals );
displayVals();

**/