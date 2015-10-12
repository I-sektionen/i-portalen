/**
 * Created by jonathan on 2015-09-08.
 */
(function () {
        //var converter1 = Markdown.getConverter();
        var converter1 = Markdown.getSanitizingConverter();


        converter1.hooks.chain("preConversion", function (text) {
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

        converter1.hooks.chain("plainLinkText", function (url) {
            return url.replace(/^https?:\/\//, "");
        });
        var editor1 = new Markdown.Editor(converter1, "-body");
        editor1.run();

    })();

    var headline = $("#id_headline");
    var txt=headline.val();
    $("#headline_collapsed").text(txt);
    $("#headline_expanded").text(txt);

    headline.keyup(function(event) {
        var txt=$(this).val();
        $("#headline_collapsed").text(txt);
        $("#headline_expanded").text(txt);
    });

    var lead = $("#id_lead");
    var lead_collapsed = $("#lead_collapsed");
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
function displayVals() {
    var multipleValues = $("#id_tags option:selected").map(function() {
        return $(this).text();
    }).get();
    $( "#tags_collapsed" ).html( multipleValues.join( ", " ) );
    $( "#tags_expanded" ).html( multipleValues.join( ", " ) );
}
$( "select" ).change( displayVals );
displayVals();
