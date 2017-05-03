// client-side js
// run by the browser each time your view template is loaded

// protip: you can rename this to use .coffee if you prefer

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {

  var prime1
  var prime2
  
  function clearPrime(clicked, prime){
    clicked.removeClass(prime);
    $( "input#" + prime ).val("");
    return null;
  }
  
  $( "#primes-under-50 li" ).click(function() {
    var num = parseInt($( this ).html());
    // If there is no prime1 set number chosen to prime1:
    if (!prime1) {
      if (prime2 != num) {
        prime1 = num;
        $( this ).addClass("prime1");
        $( "input#prime1" ).val(num);
      } else {
        prime2 = clearPrime($( this ), "prime2");
      }
    } else {
      // If there is a prime1, but not prime2, set number chosen to prime2:
      if (!prime2) {
        if (prime1 != num) {
          prime2 = num;
          $( this ).addClass("prime2");
          $( "input#prime2" ).val(num);
        } else {
          prime1 = clearPrime($( this ), "prime1");
        }
      // If prime1 and prime2 are already selected:
      } else {
        // If either is chosen again, reset that prime to null:
        if (prime1 === num) {
          prime1 = clearPrime($( this ), "prime1");
        } else if (prime2 === num) {
          prime2 = clearPrime($( this ), "prime2");
        } else {
          // Do nothing
        }
      }
    }
    if (prime1 && prime2){
      $( "form#pick-primes" ).show();
    } else {
      $( "form#pick-primes" ).hide();
    }
    console.log("Prime1: " + prime1 + ", Prime2: " + prime2);
  });

});
