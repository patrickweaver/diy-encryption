// client-side js
// run by the browser each time your view template is loaded

// protip: you can rename this to use .coffee if you prefer

// by default, you've got jQuery,
// add other scripts at the bottom of index.html
function getMessages() {
  $.get('/messages', function(data) {
    data.messages.forEach(function(message) {
      $('<li>' + message + '</li>').appendTo('ul#messages');
    });
  });
  console.log("GOT THE MESSAGES");
}


$(function() {
  console.log('hello world :o');
  
  $.get('/dreams', function(data) {
    data.dreams.forEach(function(dream) {
      $('<li>' + dream + '</li>').appendTo('ul#dreams');
    });
  });
  
  //getMessages();

  $('form#dream').submit(function(event) {
    event.preventDefault();
    var dream = $('#dream-input').val();
    console.log("DREAM: " + dream);
    if (dream.length === 0) {
      return;
    }
    $.post('/dreams?' + $.param({dream: dream}), function() {
      $('<li>' + dream + '</li>').appendTo('ul#dreams');
      $('input').val('');
      $('input').focus();
    });
  });
    
  $('form#message').submit(function(event) {
    event.preventDefault();
    var message = $('#message-input').val();
    console.log(message);
    if (message.length === 0) {
      return;
    }
    $.post('/offset?' + $.param({message: message}), function() {
      $('<li>' + message + '</li>').appendTo('ul#messages');
      $('input').val('');
      $('input').focus();
    });
    setTimeout(getMessages(), 2000);
    console.log("Times up!2");
  });

});
