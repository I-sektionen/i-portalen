/**
 * Created by isac on 2015-11-22.
 */
function generate_booking_form(pk, weeks_forward){
    console.log(weeks_forward);
    jQuery.get('booking/book/'+pk+"/api/"+weeks_forward+"/" , function( data ){
        var $element = jQuery(".booking");
        $element.data("max_number_of_slots_in_booking", data.bookable.max_number_of_slots_in_booking);
        var bookings = data.bookings;
        var bookable = data.bookable;
        var user = data.user;
        var $days = jQuery("#days");
        //Each day
        var year = null;
        var year_str = null;
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
            if (year == null){
                year = d.year;
                year_str = d.year;
            }
            if (year != d.year){
                year = d.year;
                year_str = year_str + " - " + d.year;
            }
            s = s + "<p>" + d.day + "/" + d.month;
            //Each slot:
            jQuery.each( value.slots, function( index, value2 ){
                s = s + "<div data-start=\""+d.year + "" + month + "" + day+"_"+value2.start_time + "\" " +
                     "data-end=\""+d.year + "" + month + "" + day+"_"+value2.end_time + "\" class=\"slot";
                if(value2.available){
                    if(value2.blocked){
                        s = s + " blocked\">";
                    } else {
                        s = s + " available\" ";
                        if (user.nr_of_active_bookings<bookable.max_number_of_bookings){
                            s = s + "onclick=\"select_booking_slot(this)\"";
                        }
                            s = s + ">";
                    }
                } else {
                    s = s + " unavailable\">";
                }
                var start_time = value2.start_time.split(':');
                var end_time = value2.end_time.split(':');
                s = s + "<p>" + start_time[0] + ":" + start_time[1] + "</p>";
                s = s + "<p>" + end_time[0] + ":" + end_time[1] + "</p>";
                s = s + "</div>";
            });
             // Write values to child!

            $days.append(s);
        });
        $('#year').append("<h2>"+year_str+"</h2>");
    });
    $("#id_end").attr("hidden","");
    $("#id_start").attr("hidden","");
}

function select_booking_slot(element){
    var max_number_of_slots_in_booking = jQuery(".booking").data("max_number_of_slots_in_booking");
    var $el = $(element);
    var $container = jQuery("#days");
    var first_click = null;
    var last_click = null;
    var it = 0;
    $container.find(".slot").each(function(i) {
        var $tmp = $($container.find(".slot")[i]);
        if ($tmp.data('clicked') == true){
            if (first_click == null){
                first_click = i;
                it++;
            } else {
                last_click = i;
                it++;
            }
        }
    });

    var j = $container.find(".slot").index($el);
    if (first_click==null && last_click==null){
        $el.data('clicked', true);
        $el.addClass("choosen");
    }
    else if (first_click!=null && last_click==null){
        if (max_number_of_slots_in_booking!=1 && (j==first_click+1 || j==first_click-1)){
            $el.data('clicked', true);
            $el.addClass("choosen");
        } else if (j==first_click) {
            $el.data('clicked', false);
            $el.removeClass("choosen");
        } else if(max_number_of_slots_in_booking!=1){
            console.log("max nr of slots");
        } else {
            console.log("måste sitta ihop.");
        }
    }
    else {
        if (j==first_click-1 && it<max_number_of_slots_in_booking){
            $el.data('clicked', true);
            $el.addClass("choosen");
        } else if (j==last_click+1 && it<max_number_of_slots_in_booking){
            $el.data('clicked', true);
            $el.addClass("choosen");
        } else if (j==first_click || j==last_click) {
            $el.data('clicked', false);
            $el.removeClass("choosen");
        } else if(it>=max_number_of_slots_in_booking){
             console.log("max nr of slots");
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