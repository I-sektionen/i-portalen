/**
 * Created by isac on 2015-11-22.
 */
function generate_booking_form(pk){
    jQuery.get('booking/book/'+pk+"/api/" , function( data ){
        var $element = jQuery(".booking");
        var bookable = data.bookable;
        var bookings = data.bookings;

        $element.append("<div><p>" + bookable.name +"</p></div>");
        $element.append("<div class=\"days\"></div>");
        var $days = jQuery(".days");
        //Each day
        jQuery.each( bookings, function(index, value){
            var s = "<div class=\"single_day\">";
            var d = value.date;
            s = s + "<p>Datum: " + d.year + "-" + d.month + "-" + d.day;
            //Each slot:
            jQuery.each( value.slots, function( index, value2 ){
                s = s + "<div class=\"slot";
                if(value2.available){
                    s = s + " available\">";
                } else {
                    s = s + " unavailable\">";
                }
                s = s + "<p>" + value2.start_time + "</p>";
                s = s + "<p>" + value2.end_time + "</p>";
                s = s + "</div>";
            });
             // Write values to child!
            console.log(s);
            $days.append(s);
        });
        console.log("hit.");
    });
}