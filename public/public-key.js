$(function() {
  
  /*
    Choose 2 Primes
  */

  var prime1
  var prime2
  var coprime;
  
  function clearPrime(clicked, prime){
    clicked.removeClass(prime);
    clicked.removeClass("selected");
    return null;
  }
  
  $( "#primes-under-50-list li" ).click(function() {
    var num = parseInt($( this ).html());
    // If there is no prime1 set number chosen to prime1:
    if (!prime1) {
      if (prime2 != num) {
        prime1 = num;
        $( this ).addClass("prime1");
        $( this ).addClass("selected");
      } else {
        prime2 = clearPrime($( this ), "prime2");
      }
    } else {
      // If there is a prime1, but not prime2, set number chosen to prime2:
      if (!prime2) {
        if (prime1 != num) {
          prime2 = num;
          $( this ).addClass("prime2");
          $( this ).addClass("selected");
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
      $( "button#submit-primes" ).show();
    } else {
      $( "button#submit-primes" ).hide();
    }
    console.log("Prime1: " + prime1 + ", Prime2: " + prime2);
  });
  
  $( "button#submit-primes").click(function() {
      $( ".prime1-span" ).each(function() {
        $( this ).html(prime1);
      });
      $( ".prime2-span" ).each(function() {
        $( this ).html(prime2);
      });
      $.ajax({
        url: "/public-key/primes",
        data: {
          prime1: prime1,
          prime2: prime2
        },
        success: function(data) {
          console.log("Coprimes: " + data);
          chooseCoprime(data);
          
        },
        error: function(xhr, status, err) {
          console.error(err);
        }
      });
  });
  
  /*
  Receive Coprimes:
  */
  
  function chooseCoprime(coprimes) {
    
    $( "#choose-primes").hide();
    $( "#choose-coprime" ).show();
    
    for (var c in coprimes) {
      $( "#choose-coprime ul#coprime-list" ).append(
        "<li>" + coprimes[c] + "</li>"
      );
    }  
    
    $( "ul#coprime-list li" ).click(function() {
      var num = parseInt($( this ).html());
      if (!coprime) {
        coprime = num;
        $( this ).addClass("coprime");
        $( this ).addClass("selected");
      } else {
        if (coprime === num){
          coprime = null;
          $( this ).removeClass("coprime");
          $( this ).removeClass("selected");
        } else {
          coprime = num;
          $( "ul#coprime-list li" ).removeClass("coprime");
          $( "ul#coprime-list li" ).removeClass("selected");
          $( this ).addClass("coprime");
          $( this ).addClass("selected");
        }
      }
      if (coprime) {
        $( "button#submit-coprime" ).show();
      } else {
        $( "button#submit-coprime" ).hide();
      }
    });

    $( "button#submit-coprime").click(function() {
      $( ".coprime-span" ).each(function() {
        $( this ).html(coprime);
      });
      $.ajax({
        url: "/public-key/keys",
        data: {
          prime1: prime1,
          prime2: prime2,
          coprime: coprime
        },
        success: function(data) {
          console.log("Keys: " + data);
          var keyError = false;
          for (var d in data){
            console.log(d + ": " + data[d]);
            if (d === "error"){
              keyError = keyErrorDisplay(data[d]);
              break;
            }
          }
          if (!keyError){
            displayKeys(data);
          }    
        },
        error: function(xhr, status, err) {
          console.error(err);
        }
      });
    });
  }
  
  function keyErrorDisplay(message){
    $( "#error" ).html("Error: " + message + " Refresh page to generate new keys.");
    $( "#choose-coprime" ).hide();
    $( "#error" ).show();
    return true;
  }
  
  function displayKeys(keys) {
    $( "#choose-coprime" ).hide();
    $( ".public-keys-span" ).each(function() {
      $( this ).html(keys.publicKeys[0] + ", " + keys.publicKeys[1]);
    });
    $( ".private-keys-span" ).each(function() {
      $( this ).html(keys.privateKeys[0] + ", " + keys.privateKeys[1]);
    });
    $( "#keys" ).show();
    for (var i in keys) {
      console.log(i + ": " + keys[i]);
    }
    
  }
  
  
  
  
  
  
});
