function max_length( element, max ){
     $(element).attr("autocomplete", "off");
     $(element).keypress(function(){
          if($(this).val().length > max-1 ){
               return false;
          }
     });
     $(element).change(function(){
          var str = $(this).val();
          if ( str.length > max){
               str = str.substr(0, max);
               $(this).val(str);
          }
     });
}

function onlyLetters( element ){
     var $reg = /[a-zA-Z-а-яА-Я\s]/;
     $(element).attr("autocomplete", "off");
     $(element).attr("pattern", "[a-zA-Z-а-яА-Я\s]");
     $(element).keypress(function(e){
          var letter = String.fromCharCode(e.which);
          if( $reg.test(letter) == false ){
               return false;
          }
     });
     $(element).change(function(){
          var str = $(this).val();
          str = str.replace(/[^a-zA-Z-а-яА-Я\s]/g, "");
          $(this).val(str);
     });
}

function onlyNumbers( element ){
     var $reg = /[0-9]/;
     $(element).attr("autocomplete", "off");
     //$(element).attr("-moz-appearance", "textfield");
     $(element).keypress(function(e){
          var letter = String.fromCharCode(e.which);
          if( $reg.test(letter) == false ){
               return false;
          }
     });

}

function emailValidator( element ){

     var pattern = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
     var mail = $( element );
      
      mail.blur(function(){
           if(mail.val() != ''){
                if(mail.val().search(pattern) == 0){
                      mail.removeClass("invalidField");
                      $('input[type="submit"]').removeClass("disabled");
                }
                else{
                     mail.addClass("invalidField");
                      $('input[type="submit"]').addClass("disabled");

                }
           }
           else{
                mail.removeClass("invalidField");
                $('input[type="submit"]').removeClass("disabled");
           }
      });
}
