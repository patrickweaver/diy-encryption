// * * * * * * * * * *
// Helpers:
// * * * * * * * * * *

function addClickListener(element, func) {
  element.addEventListener('click', func);
}


// * * * * * * * * * *
// Reveal best guesses
// on brute force decrypt
// * * * * * * * * * *

var bestGuessButton = document.getElementById('best-guess-button');
var bestGuesses = document.getElementById('best-guess');

if (bestGuessButton){
  bestGuessButton.addEventListener('click', function() {
    bestGuessButton.style.display = 'none';
    bestGuesses.style.display = 'block';
  });
}


// * * * * * * * * * *
// Remove Invalid Messages
// on brute force decrypt
// * * * * * * * * * *

var removeInvalidButton = document.getElementById('remove-error-button');
var invalidMessages = document.getElementsByClassName('invalid-message');

if (removeInvalidButton) {
  removeInvalidButton.addEventListener('click', function() {
    removeInvalidButton.style.display = 'none';
    for (var i = 0; i < invalidMessages.length; i++) {
      var message = invalidMessages[i];
      message.style.display = 'none';
    }
  })
}



// * * * * * * * * * *
// Generate Keys:
// * * * * * * * * * *

var generateKeys = document.getElementById('generate-keys');
if (generateKeys) {

  var submitPrimesButton = document.getElementById('submit-primes');

  // 1. Choose two primes

  var prime1
  var prime2
  var coprime;

  function clearPrime(clicked, primeClass) {
    clicked.classList.remove(primeClass);
    clicked.classList.remove('selected');
    return undefined;
  }

  function selectPrime(clicked, primeClass) {
    clicked.classList.add(primeClass);
    clicked.classList.add('selected');
  }

  var primesUnder30 = document.getElementsByClassName('prime-under-30');
  for (var i = 0; i < primesUnder30.length; i++) {
    addClickListener(primesUnder30[i], function(event) {
      var el = event.target;
      var num = parseInt(el.innerHTML);


      // If either prime is already this number
      // clear that prime
      if (prime1 === num) {
        prime1 = clearPrime(el, 'prime1');
      }
      else if (prime2 === num) {
        prime2 = clearPrime(el, 'prime2');
      }
      // If there is no prime1 set number chosen to prime1:
      else if (!prime1) {
        prime1 = num;
        selectPrime(el, 'prime1');
      }
      // If there is a prime1, but not prime2, set number chosen to prime2:
      else if (!prime2) {
        prime2 = num;
        selectPrime(el, 'prime2');
      }
      // If number is not prime1 or prime2 and
      // prime1 and prime2 are already selected:
      else {
        // Do nothing
      }

      
      if (prime1 && prime2){
        submitPrimesButton.style.display = 'block';
      } else {
        submitPrimesButton.style.display = 'none';
      }
      console.log('Prime1: ' + prime1 + ', Prime2: ' + prime2);
    });
  }

  addClickListener(submitPrimesButton , function(event) {
    var prime1Span = document.getElementsByClassName('prime1-span');
    for (var i = 0; i < prime1Span.length; i++) {
      prime1Span[i].innerHTML = prime1;
    }
    var prime2Span = document.getElementsByClassName('prime2-span');
    for (var i = 0; i < prime2Span.length; i++) {
      prime2Span[i].innerHTML = prime2;
    }

    var request = new XMLHttpRequest();
    var formData = new FormData();
    formData.append('prime1', prime1);
    formData.append('prime2', prime2);
    request.onload = primeRequestCallback;
    request.onerror = primeRequestCallbackError;
    request.open('POST', '/public-key/primes');
    request.send(formData);

    function primeRequestCallback() {
      var data = JSON.parse(this.responseText);
      chooseCoprime(data);
    }

    function primeRequestCallbackError(error) {
      console.log(error);
    }

    // 2. Find coprimes of the two primes
    

    function chooseCoprime(coprimes) {
      var choosePrimesArea = document.getElementById('choose-primes');
      choosePrimesArea.style.display = 'none';
      var chooseCoprimeArea = document.getElementById('choose-coprime');
      chooseCoprimeArea.style.display = 'block';

      var coprimeList = document.getElementById('coprime-list');

      for (var c in coprimes) {
        var node = document.createElement('li');
        node.id = 'coprime-' + coprimes[c];
        var textnode = document.createTextNode(coprimes[c]);
        node.appendChild(textnode);
        coprimeList.appendChild(node);
      }

      // 3. Choose a coprime

      var submitCoprime = document.getElementById('submit-coprime');

      addClickListener(coprimeList, function(event) {
        var el = event.target;
        var num = parseInt(el.innerHTML);

        if (!coprime) {
          coprime = num;
          selectPrime(el, 'coprime');
        } else {
          var beforeCoprime = coprime;
          var beforeCoprimeElement = document.getElementById('coprime-' + beforeCoprime);
          coprime = clearPrime(beforeCoprimeElement, 'coprime');
          if (beforeCoprime != num){
            coprime = num;
            selectPrime(el, 'coprime');
          }
        }

        if (coprime) {
          submitCoprime.style.display = 'block';
        } else {
          submitCoprime.style.display = 'none';
        }
      })

    }


    var submitCoprime = document.getElementById('submit-coprime');
    addClickListener(submitCoprime, function(event) {
      var coprimeSpan = document.getElementsByClassName('coprime-span');
      for (var i = 0; i < coprimeSpan.length; i++) {
        coprimeSpan[i].innerHTML = coprime;
      }

      var request = new XMLHttpRequest();
      var formData = new FormData();
      formData.append('prime1', prime1);
      formData.append('prime2', prime2);
      formData.append('coprime', coprime);
      request.onload = coprimeRequestCallback;
      request.onerror = coprimeRequestCallbackError;
      request.open('POST', '/public-key/keys');
      request.send(formData);

      function coprimeRequestCallback() {
        var data = JSON.parse(this.responseText);
        displayKeys(data);
      }
  
      function coprimeRequestCallbackError(error) {
        console.log(error);
      }

      // 4. Display keys generated by primes and coprime
      
      function displayKeys(keys) {
        var chooseCoprime = document.getElementById('choose-coprime');
        chooseCoprime.style.display = 'none';

        var publicKeysSpan = document.getElementsByClassName('public-keys-span');
        for (var i = 0; i < publicKeysSpan.length; i++) {
          publicKeysSpan[i].innerHTML = keys.publicKeys[0] + ", " + keys.publicKeys[1];
        }
        var privateKeysSpan = document.getElementsByClassName('private-keys-span');
        for (var i = 0; i < privateKeysSpan.length; i++) {
          privateKeysSpan[i].innerHTML = keys.privateKeys[0] + ", " + keys.privateKeys[1];
        }

        var keysArea = document.getElementById('keys');
        keysArea.style.display = 'block';
      }

    })
 
  });
}


/* Simple Offset Generator */

var offsetSlider = document.getElementById("offset-range");
var output = document.getElementById("simple-offset-label");
var decoderInside = document.getElementById("decoder-inside");


if (offsetSlider && output) {
  output.innerHTML = offsetSlider .value; // Display the default slider value
  
  // Update the current slider value (each time you drag the slider handle)
  offsetSlider.oninput = function() {
    output.innerHTML = this.value;
    var rotation = "rotate(" + (-360 / 26) * parseInt(this.value) + "deg)";
    console.log("rotation:", rotation);
    decoderInside.style.transform = rotation;
  }
}
