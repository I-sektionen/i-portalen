/**
 * Created by isac on 2015-11-22.
 */
function generate_booking_form(pk){
    jQuery.get('booking/book/'+pk+"/api/" , function( data ){
        var $element = jQuery(".booking");
        var bookable = data.bookable;
        var bookings = data.bookings;

        $element.append("<div><p>" + bookable.name +"</p></div>");
        $element.append("<div id=\"days\"></div>");
        var $days = jQuery("#days");
        //Each day
        jQuery.each( bookings, function(index, value){
            var s = "<div class=\"single_day\">";
            var d = value.date;
            var month = d.month;
            if (month <10){
                month = "0"+month;
            }
            var day = d.day;
            if (day <10){
                day = "0"+day;
            }
            s = s + "<p>" + d.year + "-" + month + "-" + day;
            //Each slot:
            jQuery.each( value.slots, function( index, value2 ){
                s = s + "<div data-start=\""+d.year + "" + month + "" + day+"_"+value2.start_time + "\" " +
                     "data-end=\""+d.year + "" + month + "" + day+"_"+value2.end_time + "\" class=\"slot";
                if(value2.available){
                    s = s + " available\" onclick=\"select_booking_slot(this)\">";
                } else {
                    s = s + " unavailable\">";
                }
                s = s + "<p>" + value2.start_time + "</p>";
                s = s + "<p>" + value2.end_time + "</p>";
                s = s + "</div>";
            });
             // Write values to child!

            $days.append(s);
        });
    });
    $("#id_end").attr("hidden","");
    $("#id_start").attr("hidden","");
}

function select_booking_slot(element){
    var $el = $(element);
    var $container = jQuery("#days");
    var first_click = null;
    var last_click = null;
    $container.find(".slot").each(function(i) {
        var $tmp = $($container.find(".slot")[i]);
        if ($tmp.data('clicked') == true){
            if (first_click == null){
                first_click = i;
            } else {
                last_click = i;
            }
        }
    });
    var j = $container.find(".slot").index($el);
    if (first_click==null && last_click==null){
        $el.data('clicked', true);
        $el.addClass("choosen");
    }
    else if (first_click!=null && last_click==null){
        if (j==first_click+1 || j==first_click-1){
            $el.data('clicked', true);
            $el.addClass("choosen");
        } else if (j==first_click) {
            $el.data('clicked', false);
            $el.removeClass("choosen");
        } else {
            console.log("måste sitta ihop.");
        }
    }
    else {
        if (j==first_click-1){
            $el.data('clicked', true);
            $el.addClass("choosen");
        } else if (j==last_click+1){
            $el.data('clicked', true);
            $el.addClass("choosen");
        } else if (j==first_click || j==last_click) {
            $el.data('clicked', false);
            $el.removeClass("choosen");
        } else {
            console.log("måste sitta ihop.");
        }
    }
    first_click = null;
    $container.find(".slot").each(function(i) {
        var $tmp = $($container.find(".slot")[i]);
        if ($tmp.data('clicked') == true){
            if (first_click == null){
                first_click = i;
            } else {
                last_click = i;
            }
        }
    });
    $("#id_start").val($($container.find(".slot")[first_click]).data('start'));
    if (last_click==null){
        $("#id_end").val($($container.find(".slot")[first_click]).data('end'));
    } else {
        $("#id_end").val($($container.find(".slot")[last_click]).data('end'));
    }

}