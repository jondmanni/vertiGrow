//http://stackoverflow.com/questions/3773582/jquery-countdown-status-to-show-in-button

$.fn.timedDisable = function(time) {
  if (time == null) {
    time = 5;
  }
  var seconds = Math.ceil(time); // Calculate the number of seconds
  return $(this).each(function() {
    $(this).attr('disabled', 'disabled');
    var disabledElem = $(this);
    var originalText = this.innerHTML; // Remember the original text content

    // append the number of seconds to the text
    disabledElem.text(originalText + ' (' + seconds + ')');

    // do a set interval, using an interval of 1000 milliseconds
    //     and clear it after the number of seconds counts down to 0
    var interval = setInterval(function() {
        seconds = seconds - 1;
      // decrement the seconds and update the text
      disabledElem.text(originalText + ' (' + seconds + ')');
      if (seconds === 0) { // once seconds is 0...
        disabledElem.removeAttr('disabled')
          .text(originalText); //reset to original text
        clearInterval(interval); // clear interval
      }
    }, 1000);
  });
};

$(function() {
    $('#LED0').click(function() {
        $.ajax({
            //url: '/LEDS',
            url: '/LED0',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
        $(this).timedDisable($('#LED0_time').val());
    });
});

$(function() {
    $('#LED1').click(function() {
        $.ajax({
            //url: '/LEDS',
            url: '/LED1',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
        $(this).timedDisable($('#LED1_time').val());
    });
});

$(function() {
    $('#MOTOR0').click(function() {
        $.ajax({
            //url: '/LEDS',
            url: '/MOTOR0',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
        //$(this).timedDisable($('#MOTOR0_steps').val());
    });
});
