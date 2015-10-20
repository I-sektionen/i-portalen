/**
 * Created by jonathan on 2015-10-20.
 */
    var shuffle_sponsors = function () {
        var parent = $("#partners");
        var divs = parent.children();
        while (divs.length) {
            parent.append(divs.splice(Math.floor(Math.random() * divs.length), 1)[0]);
        }
    };
