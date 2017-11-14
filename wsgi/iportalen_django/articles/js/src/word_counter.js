
// function updateCount()  {

//$('#characters').text(cs);
// }

$(document).ready(function()
{
    $("#id_lead").attr('maxlength','160');
});

$("#id_lead").on("change paste keyup keydown keypress", function(){
    console.log("funktion");
    var cs = $("#id_lead").val().length;
    document.getElementById("characters").value = cs+"/160";
});



//$('#id_lead').on('input', updateCount());

