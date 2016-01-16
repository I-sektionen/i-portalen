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
    markdown_event_preview();

    //These are the elements that is being listened to.
    var listened_to = [];
    var headline = $("#id_headline");
    var lead = $("#id_lead");
    var place = $("#id_location");
    var start = $("#id_start");
    var end = $("#id_end");
    var enable_registration = $("#id_enable_registration");
    var free_places = $("#id_registration_limit");
    var organisation = $("#id_organisations");
    var tags = $("#id_tags");
    var sponsor = $("#id_sponsored");
    var extra_registration = $("#id_extra_deadline_text");
    var extra_registration_date = $("#id_extra_deadline");

    //This is the elements where the results are printed to.
    var lead_preview = $(".lead_preview");
    var headline_preview = $(".headline_preview");
    var place_preview = $(".place_preview");
    var start_preview_date = $(".start_preview_date");
    var start_preview_time = $(".start_preview_time");
    var end_preview = $("#id_end_preview");
    var enable_registration_preview = $(".enable_registration_preview");
    var free_places_preview = $(".registration_limit_preview");
    var author_preview = $(".author_preview");
    var tags_preview = $(".tags_preview");
    var sponsor_preview = $(".sponsor_preview");
    var extra_registration_preview = $(".extra_registration_preview");


    listened_to.push([headline, headline_preview],
                    [lead, lead_preview],
                    [place, place_preview],
                    [start, [start_preview_time, start_preview_date]],
                    [end, end_preview],
                    [enable_registration, enable_registration_preview],
                    [free_places, free_places_preview],
                    [organisation, author_preview],
                    [tags, tags_preview],
                    [sponsor, sponsor_preview],
                    [extra_registration, extra_registration_preview]
    );
    enable_registration_preview.hide();
    var render = function (){
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
            } else if(element[0].is(enable_registration)) {
                if (element[0].is(":checked")) {
                    element[1].show();
                } else {
                    element[1].hide();
                }
            } else if(element[0].is(organisation)) {
                var selected_org = organisation.children().filter(":selected");
                var org_string = "";
                jQuery.each(selected_org, function (index, ele) {
                    org_string = ele.innerHTML;
                });
                if (org_string == "") {
                    author_preview.text("Ditt namn");
                } else {
                    author_preview.text(org_string);
                }
            } else if(element[0].is(tags)) {
                var selected_tags = tags.children().filter(":selected");
                var tag_string = "";
                jQuery.each(selected_tags, function (index, ele) {
                    tag_string = tag_string + ele.innerHTML + ", ";
                });
                if (tag_string != "") {
                    tag_string = tag_string.substring(0, tag_string.length - 2)
                }
                element[1].text(tag_string);
            } else if(element[0].is(sponsor)) {
                if(sponsor.prop('checked')){
                    sponsor_preview.text("Sponsrat innehåll");
                } else {
                    sponsor_preview.text("");
                }
            } else if(element[0].is(extra_registration)) {
                txt = element[0].val();
                var tmp = "";

                if (txt == ""){
                    element[1].text("");
                } else {
                    txt = "Anmälningsstop för att " + txt;
                    if (extra_registration_date.val() != ""){
                       txt = txt + " " + extra_registration_date.val();
                    } else {
                        txt = txt + "(Datum ej angivet)"
                    }
                    element[1].text(txt);
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
};



