
// function updateCount()  {

//$('#characters').text(cs);
// }
$("#id_lead").on("change paste keyup keypress", function(){
    console.log("funktion");
    var cs = $("#id_lead").val().length;
    document.getElementById("characters").value = cs+"/160";
});


//$('#id_lead').on('input', updateCount());

