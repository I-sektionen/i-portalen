$(function() {
   $("#vote").click(function(){
      if (confirm("Du är på väg att lämna din röst. Tryck ok för att bekräfta.")){
         $('form#voting-form').submit();
      } else {
          event.preventDefault();
      }
   });
});