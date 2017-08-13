/**
 * Created by jers on 11/04/16.
 */

function next_button(tab_no) {
    var next_tab_no = parseInt(tab_no, 10)+1;
    var next ='#tab'+next_tab_no+' a';
    $(next).click();
    scroll(0,0)
}

function prev_button(tab_no) {
    var prev_tab_no = parseInt(tab_no, 10)-1;
    var prev ='#tab'+prev_tab_no+' a';
    $(prev).click();
    scroll(0,0)
}