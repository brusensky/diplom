$('document').ready(function() {
     $("#delivery_courier").click(function() {
          $("#pickup").removeClass("btn-active");
          $(this).addClass("btn-active");
     });
     $("#pickup").click(function() {
          $("#delivery_courier").removeClass("btn-active");
          $(this).addClass("btn-active");
     });
});
