function get_delivery_cost(){
     $.ajax({
         type: 'GET',
         async: true,
         url: 'http://127.0.0.1:8000/obp/delivery-cost/',
         dataType: 'json',
         success: function(data) {
              $("#delivery-cost-field").html('');
              $("#delivery-cost-field").append(data["cost"] + " грн.")
              $("#total-price-field").html('');
              $("#total-price-field").append(data["total_price"] + " грн.")
         }
     });
}

function get_pickup_cost(){
     $.ajax({
         type: 'GET',
         async: true,
         url: 'http://127.0.0.1:8000/obp/pickup-cost/',
         dataType: 'json',
         success: function(data) {
              $("#delivery-cost-field").html('');
              $("#delivery-cost-field").append(data["cost"] + " грн.")
              $("#total-price-field").html('');
              $("#total-price-field").append(data["total_price"] + " грн.")
         }
     });
}




$('document').ready(function() {
     onlyLetters("[name = 'name']");
     onlyLetters('[name = "city"]');
     onlyLetters('[name = "street"]');
     emailValidator('[name = "email"]');

     onlyNumbers('[name = "house"]');
     max_length('[name = "house"]', 4);
     onlyNumbers('[name = "entrance"]');
     max_length('[name = "entrance"]', 2);
     onlyNumbers('[name = "apartament_number"]');
     max_length('[name = "apartament_number"]', 3);


     get_pickup_cost();

     $("#delivery_courier").click(function() {
          $("#pickup").removeClass("btn-active");
          $(this).addClass("btn-active");
          $('.delivery-form-container').removeClass('d-none');
          get_delivery_cost();
     });
     $("#pickup").click(function() {
          $("#delivery_courier").removeClass("btn-active");
          $(this).addClass("btn-active");
          $('.delivery-form-container').addClass('d-none');
          get_pickup_cost();
     });
     // $("#submit_checkout").click(function(){
     //      var url = $(".btn-active").data("url");
     //      $.ajax({
     //          type: 'POST',
     //          async: true,
     //          url: url,
     //          dataType: 'json',
     //          data: $('.form-checkout').serialize(),
     //          success: function(data) {
     //               alert($("#submit_checkout").data("url"));
     //               window.location.replace( $("#submit_checkout").data("url") );
     //          },
     //          error: function(){
     //               alert("При оформлении заказа произошла ошибка");
     //          }
     //      });
     // });
});
