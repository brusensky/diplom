//Рисовка блока для одного элемента в корзину
function shadowAllOff(){
     $(".shadow-block").css({
          "opacity": "0",
          "left": "-100%"
     });
}

function shadowAllOn(){
     $(".shadow-block").css({
          "opacity": "1",
          "left": "0"
     });
}

function openBasket(){
     $(".basket-block").css({
          "right": "0px",
          "transition": "right 0.65s",
          "display": "block",
     });
     shadowAllOn();
}

function closeBasket(){
     var width = parseInt( $('.basket-block').css('width'), 10 );
     $(".basket-block").css({
          "right": "-" + String(width+10) + "px",
          "transition": "right 0.65s",
     });
     $(".basket-block").css({
          "display": "none",
     });
     shadowAllOff();
}

function ifCartIsEmpty(quantity){
     if (quantity == 0){
          closeBasket();
     }
}

function plusQuantity(id){
     $.getJSON('http://127.0.0.1:8000/cart/plus_quantity/', {"id": id}, function(data, jqXHR){
          $("#quantityField"+id).html('');
          $("#quantityField"+id).append(data["quantity"]);
          $("#total-price").html('');
          $("#total-price").append(data["totalPrice"] + " грн.");
     });
}

function minusQuantity(id){
     $.getJSON('http://127.0.0.1:8000/cart/minus_quantity/', {"id": id}, function(data, jqXHR){
          $("#quantityField"+id).html('');
          $("#quantityField"+id).append(data["quantity"]);
          $("#total-price").html('');
          $("#total-price").append(data["totalPrice"] + " грн.");
     });
     ifCartIsEmpty();
}

function deleteProduct(id){
     $.getJSON('http://127.0.0.1:8000/cart/remove/', {"id": id}, function(data, jqXHR){
          $("#productItem"+id).remove();
          //$("#"+id).append(data["quantity"]);
          $("#total-price").html('');
          $("#total-price").append(data["totalPrice"] + " грн.");
          ifCartIsEmpty(data["quantity"]);

     });
}

function createItemInBasket(id, img_url,  quantity, price, title){

     var product_item =
          '<div class = "product-item d-flex flex-row" id = "productItem'+id+'">'+
               '<div class = "d-flex flex-row product-link flex-grow-1">'+
                    '<div class = "flex-fill image-container">'+
                         '<img src = "' + img_url + '">'+
                    '</div>'+
                    '<div class = "flex-fill d-flex flex-column info-container flex-fill">'+
                         '<div class = "flex-fill title">' + String(title) + '</div>'+
                         '<div class = "flex-fill price">' + String(price) + '</div>'+
                    '</div>'+
               '</div>'+

               '<div class = "d-flex flex-row product-buttons flex-grow-1">'+
                    '<div class="btn-toolbar" role="toolbar" aria-label="Toolbar with button groups">'+
                         '<div class="btn-group mr-2" role="group" aria-label="First group">'+
                              '<button type="button" class="basket-btn btnPlusQuantity" onClick = "plusQuantity('+id+')">+</button>'+
                              '<div class="quantity align-middle"><span id = "quantityField'+id+'">'+ quantity +'</span></div>'+
                              '<button type="button" class="basket-btn" onClick = "minusQuantity('+id+')">-</button>'+
                         '</div>'+
                    '</div>'+
                    '<div class = "btn-delete">'+
                         '<button type="button"  onClick = "deleteProduct('+id+')">&times;</button>'+
                    '</div>'+
               '</div>'+
          '<div>';
     return product_item;
}


function createList(list){
     var div = $('<div class = "products w-100 p-0"></div>');
     for( var i = 0; i <list.length; i++){
          div.append(createItemInBasket(list[i]['id'], list[i]['img_url'], list[i]['quantity'], list[i]['price'], list[i]['title']) )
     }
     return div;
}



$(document).ready(function () {
     $('#btn-open-basket').click(function(){
          $('.basket-group').children().remove();
          $flag = false;
          $.ajax({
              type: 'GET',
              async: false,
              url: 'http://127.0.0.1:8000/cart/CartList/',
              success: function(data, jqXHR){
                  $('.basket-group').append( createList( data['cartList']) );
                  if (data['cartList']){
                       $flag = true;
                  }
                  $("#total-price").html('');
                  $("#total-price").append(data["totalPrice"] + " грн.");
             },
              dataType: 'json',
          });

           // $.getJSON('http://127.0.0.1:8000/cart/CartList/', {id: 2}, function(data, jqXHR){
           //      $('.basket-group').append( createList( data['cartList']) );
           //      if (data['cartList']){
           //           alert(1);
           //      }
           //      $("#total-price").html('');
           //      $("#total-price").append(data["totalPrice"] + " грн.");
           // });
           if($flag){
                var right = parseInt( $(".basket-block").css("right"), 10 );
                if( Number( right ) < 0 ){
                    openBasket();
                }
                else{
                     closeBasket();
                }
           }

      });

});
