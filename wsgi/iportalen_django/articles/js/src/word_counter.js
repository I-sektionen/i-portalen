

$(document).ready(function()
{
    $("#id_lead").attr('maxlength','160');
});

$("#id_lead").on("change paste keyup keydown keypress", function(){
    console.log("funktion");
    var cs = $("#id_lead").val().length;
    document.getElementById("word_counter_form").value = cs+"/160";
});

//Get coordinate of the lead form by using jquery



