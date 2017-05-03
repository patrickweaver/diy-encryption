// client-side js
// run by the browser each time your view template is loaded

// protip: you can rename this to use .coffee if you prefer

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {
  console.log('hello world :o');
  
  $.get('/dreams', function(data) {
    data.dreams.forEach(function(dream) {
      $('<li>' + dream + '</li>').appendTo('ul#dreams');
    });
  });

  $('form').submit(function(event) {
    event.preventDefault();
    var dream = $('input').val();
    if (dream.length === 0) {
      return;
    }
    $.post('/dreams?' + $.param({dream: dream}), function() {
      $('<li>' + dream + '</li>').appendTo('ul#dreams');
      $('input').val('');
      $('input').focus();
    });
  });

});
