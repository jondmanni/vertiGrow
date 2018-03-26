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


// Homing Disable for Test: Motor Control
$.fn.homingDisable = function() {
  // Set arbitrary time for now
  var seconds = 5;
  return $(this).each(function() {
    $(this).attr('disabled', 'disabled');
    var disabledElem = $(this);
    var originalText = this.innerHTML; // Remember the original text content

    // append the number of seconds to the text
    //disabledElem.text(originalText + ' (' + seconds + ')');

    // Set text to "Homing..."
    disabledElem.text('Homing...');

    // do a set interval, using an interval of 1000 milliseconds
    //     and clear it after the number of seconds counts down to 0
    var interval = setInterval(function() {
        seconds = seconds - 1;
      if (seconds === 0) { // once seconds is 0...
        //disabledElem.removeAttr('disabled')
          //.text('Homed'); //reset text to "Homed"
        disabledElem.text('Homed');
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


// Test: Water Control
$(function() {
    $(document).on('click', '.water_on', function() {
      $(this).removeClass('turn_on').addClass('turn_off');
      $(this).removeClass('water_on').addClass('water_off');
      $(this).text('Turn Off');
      $.ajax({
          url: '/WATER_ON',
          data: $('form').serialize(),
          type: 'POST',
          success: function(response) {
              console.log(response);
          },
          error: function(error) {
              console.log(error);
          }
      });
    });
    $(document).on('click', '.water_off', function() {
      $(this).removeClass('turn_off').addClass('turn_on');
      $(this).removeClass('water_off').addClass('water_on');
      $(this).text('Turn On');
      $.ajax({
          url: '/WATER_OFF',
          data: $('form').serialize(),
          type: 'POST',
          success: function(response) {
              console.log(response);
          },
          error: function(error) {
              console.log(error);
          }
      });
    });
});

// Schedule: Fertilize checkbox with hidden value
$(function() {
  $('.fertilize').click(function(){
    $('#HIDDEN_fertilize').val( this.checked ? 'True' : 'False');
  });
});

// Schedule: Add Event Repeating checkbox with hidden value
$(function() {
  $('.repeating').click(function(){
    $('#HIDDEN_repeating').val( this.checked ? 'True' : 'False');
  });
});

// Test: Light Control
$(function() {
    $(document).on('click', '.lights_on', function() {
      $(this).removeClass('turn_on').addClass('turn_off');
      $(this).removeClass('lights_on').addClass('lights_off');
      $(this).text('Turn Off');
      $.ajax({
          url: '/LIGHTS_ON',
          data: $('form').serialize(),
          type: 'POST',
          success: function(response) {
              console.log(response);
          },
          error: function(error) {
              console.log(error);
          }
      });
    });
    $(document).on('click', '.lights_off', function() {
      $(this).removeClass('turn_off').addClass('turn_on');
      $(this).removeClass('lights_off').addClass('lights_on');
      $(this).text('Turn On');
      $.ajax({
          url: '/LIGHTS_OFF',
          data: $('form').serialize(),
          type: 'POST',
          success: function(response) {
              console.log(response);
          },
          error: function(error) {
              console.log(error);
          }
      });
    });
});

// Test: Home X-Axis
$(function() {
    $('#HOME_X').click(function() {
      // First, send a post request to start motors moving Home
      // Then, check every second using GET requests to see if
      // the car is at home. Once the car is home, stop sending
      // GET requests and change the text to "Homed" and leave
      // it disabled.
      $.ajax({
        url: '/HOME_X',
        data: $('form').serialize(),
        type: 'POST',
        success: function (response) {
            console.log(response); // do anything you want with your parsed data
        },
        error: function(error) {
            console.log(error);
        }
      });

      $(this).attr('disabled', 'disabled'); // disable the button
      var disabledElem = $(this);
      disabledElem.text('Homing...');

      // do a set interval, using an interval of 1000 milliseconds
      var interval = setInterval(function() {

        $.ajax({
          type: 'GET',
          url: '/HOME_X',
          dataType: 'json',
          success: function (data) {
              console.log(data); // do anything you want with your parsed data
              if (data.status == '1') {
                disabledElem.text('Homed');
                clearInterval(interval);
              }
          }
        });

      }, 1000);

    });
});

// Test: Set X-Axis
$(function() {
    $('#SET_X').click(function() {
        $.ajax({
            url: '/SET_X',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

// Calibrate: Water
var lastClick = 0;
var clicked = 0;
$(function() {
  $("#CALIBRATE").click(function() {
    // Turn the water on
    if (clicked == 0) {
      $.ajax({
          url: '/WATER_ON',
          data: {'fert_box':0},
          type: 'POST',
          success: function(response) {
              console.log(response);
          },
          error: function(error) {
              console.log(error);
          }
      });
      clicked = 1;
    }
    // Change the text and color
    $(this).text('My container is full!');
    $(this).addClass('turn_off');
    // Get time information
    var d = new Date();
    var t = d.getTime();
    var time = t - lastClick;
    if(time < 99999999999) { // If the user clicked the second time
      // Turn the water off
      $.ajax({
          url: '/WATER_OFF',
          data: $('form').serialize(),
          type: 'POST',
          success: function(response) {
              console.log(response);
          },
          error: function(error) {
              console.log(error);
          }
      });

      // Get form info and attached time info
      var form_info = $('form').serializeArray();
      form_info.push({name: 'time', value: time});
      // Send the information over
      $.ajax({
        url: '/calibFlow',
        data: form_info,
        type: 'POST',
        success: function(response) {
          console.log(response);
        },
        error: function(error) {
          console.log(error);
        }
      });

      // Change color back and disable the button
      $(this).removeClass('turn_off');
      $(this).attr('disabled', 'disabled');
      var disabledElem = $(this);

      // Get the flow rate from the process
      $.ajax({
        type: 'GET',
        url: '/calibFlow',
        dataType: 'json',
        success: function (data) {
            console.log(data); // do anything you want with your parsed data
            disabledElem.text('Flow Rate: ' + data.flow.toFixed(2) + ' L/s');
        }
      });
    }
    lastClick = t;
  });
});

// Schedule: Datepicker
// https://jqueryui.com/datepicker/
// Timepicker: http://timepicker.co
$(function() {
    $("#start_datepicker" ).datepicker({minDate: new Date()});
    $("#start_datepicker").datepicker("setDate", new Date());
    $("#end_datepicker" ).datepicker({minDate: new Date()});
    $('input.timepicker').timepicker({
      dropdown: false,
      defaultTime: 'now'
    });
});


// Shedule: Display water quantity dropdown
// getEvents(): updates Upcoming Events side of page
// Delete functionality to events
jQuery(document).ready(function(){

  function getTimeDiff(startTime, endTime) {
    //help: http://stackoverflow.com/questions/12170209/difference-between-two-times-that-are-saved-as-strings-using-javascript
    function to24h(value) {
      value = value.split(' ');
      time_val = value[0].split(':');
      return [(time_val[0] % 12) + (value[1]=="PM" ? 12:0), time_val[1]];
    }
    start = to24h(startTime);
    end = to24h(endTime);

    min = end[1]-start[1];
    hour_carry = 0;
    if (min < 0) {
      min += 60;
      hour_carry += 1;
    }
    hour = (end[0]||24) - start[0] - hour_carry;
    return (hour + min/60);

    //return (to24h(endTime)||24) - to24h(startTime);
  }

  function getEvents() {
    $.ajax({
      type: 'GET',
      url: '/addEvent',
      dataType: 'json',
      success: function (data) {
          console.log(data); // do anything you want with your parsed data
          //var events = jQuery.parseJSON(data.events);
          $("#upcoming_events").empty();
          for (var i = 0; i < data.events.length; i++) {
            // data format: eventID, eventType, quantity, start_date, end_date, repeat, freq, eventTime, endTime
                if (data.events[i][6] == 'daily'){
                  data.events[i][6] = 'Daily';
                } else if (data.events[i][6] == 'every_other'){
                  data.events[i][6] = 'Every Other Day';
                } else if (data.events[i][6] == 'weekly'){
                  data.events[i][6] = 'Weekly';
                }
                if (data.events[i][1] == 'LightingOn'){
                  data.events[i][1] = 'Lighting';
                } else if (data.events[i][1] == 'LightingOff'){
                  data.events[i][1] = 'Lighting';
                }
                if (data.events[i][5] == 0){
                  data.events[i][5] = 'False';
                }
                if (data.events[i][4] != 0){ // Repeating = True
                  if (data.events[i][1] == "Lighting"){
                    $("#upcoming_events").prepend('<div class="event">' + '<table><tr><td class="event_item">' +
                        data.events[i][1] + ':</td><td>' +
                        '<div>' + data.events[i][3] + ' - ' + data.events[i][4] +
                        '</div><div>' + data.events[i][6] + ' from ' + data.events[i][7] + ' to ' +
                        data.events[i][8] + '</div>' +
                        '<div>Repeat: ' + data.events[i][5] + '</div>' +
                        '<div class="delete"><div class="del_child">&#10005;</div></div>' +
                        '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +
                        '</td></tr></table></div>');
                  } else {
                    $("#upcoming_events").prepend('<div class="event">' + '<table><tr><td class="event_item">' +
                        data.events[i][1] + ':</td><td>' +
                        '<div>' + data.events[i][3] + ' - ' + data.events[i][4] +
                        '</div><div>' + data.events[i][6] + ' at ' + data.events[i][7] + '</div>' +
                        '<div>Repeat: ' + data.events[i][5] + '</div>' +
                        '<div class="delete"><div class="del_child">&#10005;</div></div>' +
                        '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +
                        '</td></tr></table></div>');
                  }
            //   if (data.events[i][1] == "Water"){ // Water
            //     $("#upcoming_events").prepend('<div class="event">' +
            //         '<div>' + data.events[i][3] + ' - ' + data.events[i][4] +
            //         '<div class="right">' + data.events[i][7] +
            //         '</div></div><div>' + data.events[i][1] + ' ' +
            //         data.events[i][6] + ' at ' + data.events[i][7] + '</div>' +
            //         '<div>Repeatthis: ' + data.events[i][5] + '</div>' +
            //         '<div class="delete"><div class="del_child">&#10005;</div></div>' +
            //         '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +
            //         '</div>');
            //   } else if (data.events[i][1] == "Fertilize"){ // Fertilize
            //     $("#upcoming_events").prepend('<div class="event">' +
            //         '<div>' + data.events[i][3] + ' - ' + data.events[i][4] +
            //         '<div class="right">' + data.events[i][7] +
            //         '</div></div><div>' + data.events[i][1] + ' ' +
            //         data.events[i][6] + ' at ' + data.events[i][7] + '</div>' +
            //         '<div>Repeat: ' + data.events[i][5] + '</div>' +
            //         '<div class="delete"><div class="del_child">&#10005;</div></div>' +
            //         '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +
            //         '</div>');
            //   } else if (data.events[i][1] == "Lighting"){ // Lighting
            //     $("#upcoming_events").prepend('<div class="event">' +
            //         '<div>' + data.events[i][3] + ' - ' + data.events[i][4] +
            //         '<div class="right">' + data.events[i][7] +
            //         ' - ' + data.events[i][8] +
            //         '</div></div><div>' + data.events[i][1] + ' ' +
            //         data.events[i][6] + '<div class="right">' +
            //         //thisguy(1, 3) +
            //         //to24h(data.events[i]6) +
            //         getTimeDiff(data.events[i][7], data.events[i][8]) +
            //         ' hours</div>' + '</div>' +
            //         '<div class="delete"><div class="del_child">&#10005;</div></div>' +
            //         '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +
            //         '</div>');
            //   }
            //   $("#upcoming_events").prepend('<div class="event">' +
            //       '<div>' + data.events[i][3] + ' - ' + data.events[i][4] +
            //       '<div class="right">' + data.events[i][7] +
            //       '</div></div><div>' + data.events[i][1] + ' ' +
            //       data.events[i][6] + ' at ' + data.events[i][7] + '</div>' +
            //       '<div>Repeatthis: ' + data.events[i][5] + '</div>' +
            //       '<div class="delete"><div class="del_child">&#10005;</div></div>' +
            //       '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +                    '</div>');
            //       '</div>');
                } else { // Repeating = False
                  if (data.events[i][1] == "Lighting"){
                    $("#upcoming_events").prepend('<div class="event">' + '<table><tr><td class="event_item">' +
                        data.events[i][1] + ':</td><td>' +
                        '<div>' + data.events[i][3] +
                        '</div><div>Once from ' + data.events[i][7] + ' to ' + data.events[i][8] + '</div>' +
                        '<div>Repeat: ' + data.events[i][5] + '</div>' +
                        '<div class="delete"><div class="del_child">&#10005;</div></div>' +
                        '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +
                        '</td></tr></table></div>');
                  } else {
                    $("#upcoming_events").prepend('<div class="event">' + '<table><tr><td class="event_item">' +
                        data.events[i][1] + ':</td><td>' +
                        '<div>' + data.events[i][3] +
                        '</div><div>Once at ' + data.events[i][7] + '</div>' +
                        '<div>Repeat: ' + data.events[i][5] + '</div>' +
                        '<div class="delete"><div class="del_child">&#10005;</div></div>' +
                        '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +
                        '</td></tr></table></div>');
                  }

                    // $("#upcoming_events").prepend('<div class="event">' +
                    //     '<div>' + data.events[i][3] +
                    //     '<div class="right">' + data.events[i][7] +
                    //     '</div></div><div>' + data.events[i][1] + ' ' +
                    //     data.events[i][6] + ' at ' + data.events[i][7] + '</div>' +
                    //     '<div>Repeat: ' + data.events[i][5] + '</div>' +
                    //     '<div class="delete"><div class="del_child">&#10005;</div></div>' +
                    //     '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +
                    //     '</div>');
            //   $("#upcoming_events").prepend('<div class="event">' +
            //       '<div>' + data.events[i][3] +
            //       '<div class="right">' + data.events[i][7] +
            //       '</div></div><div>' + data.events[i][1] + '</div>' +
            //       '<div>Repeat: ' + data.events[i][5] + '</div>' +
            //       '<div class="delete"><div class="del_child">&#10005;</div></div>' +
            //       '<input class="eventID" type="hidden" value="' + data.events[i] + '">' +
            //       '</div>');
            //   //$("#upcoming_events").prepend('<div class="event">' +
            //   //    data.events[i][2] + '</div>');
                }
          }
          //$("#upcoming_events").append('List size:' + events.size());
          //$("#upcoming_events").append('<div class="item">' + data.num_events + '</div><br>');
      }
    });
  }



  // Display current planned events
  setInterval(getEvents, 15000);
  //$("#upcoming_events").append('<div>Documented loaded.</div>');

  // Delete events that have been planned
  $('#upcoming_events').on('click', 'div.delete', function() {
    //e.preventDefault();
    //eventID = $(this).closest('.event')[0].id;

    eventID = {'event':$(this).siblings('.eventID').val()};
    // Delete event from scheduler
    $.ajax({
      url: '/deleteEvent',
      data: eventID,
      type: 'POST',
      success: function(response) {
        console.log(response);
      },
      error: function(error) {
        console.log(error);
      }
    });

    $(this).closest('.event').remove();
    //e.preventDefault();
  });


  //Display water quantity dropdown
  $("#add_event_select_type").change(function(){
    $(this).find("option:selected").each(function(){
      if($(this).attr("value")=="water"){
        //$("#add_event_water_quantity_div").show();

        $("#add_event_end_time").removeClass('table');
        $("#add_event_end_time").addClass('lighting_hidden');
      }
      else if($(this).attr("value")=="lighting"){
        //$("#add_event_water_quantity_div").hide();
        $("#add_event_end_time").removeClass('lighting_hidden');
        // Add table for alignment purposes
        $("#add_event_end_time").addClass('table');
      }
      else if($(this).attr("value")=="fertilize"){
        //$("#add_event_water_quantity_div").hide();

        $("#add_event_end_time").removeClass('table');
        $("#add_event_end_time").addClass('lighting_hidden');
      }
    });
  }).change();

  // Repeating Checkbox
  $("#repeating").change(function(){
    if(this.checked) {
      //$("#add_event_end_date_div").show();
      //$("#add_event_repeat_period_div").show();
      $("#add_event_end_date_div").removeClass('hidden');
      $("#add_event_end_date_div").addClass('table');
      $("#add_event_repeat_period_div").removeClass('hidden');
      $("#add_event_repeat_period_div").addClass('table');
    }
    else {
      $("#add_event_end_date_div").addClass('hidden');
      $("#add_event_end_date_div").removeClass('table');
      $("#add_event_repeat_period_div").addClass('hidden');
      $("#add_event_repeat_period_div").removeClass('table');
      //$("#add_event_end_date_div").hide();
      //$("#add_event_repeat_period_div").hide();
    }
  });

  // Display custom repeat frequency
  $("#add_event_repeat_freq").change(function(){
    $(this).find("option:selected").each(function(){
      if($(this).attr("value")=="custom"){
        $("#add_event_repeat_custom_div").removeClass('hidden');
        $("#add_event_repeat_custom_div").addClass('table');
      }
      else {
        $("#add_event_repeat_custom_div").addClass('hidden');
        $("#add_event_repeat_custom_div").removeClass('table');
      }
    });
  }).change();

  // Control hidden checkboxes for custom repeat
  $(function() {
    $('#sunday').click(function(){
      $('#HID_sunday').val( this.checked ? 'True' : 'False');
    });
    $('#monday').click(function(){
      $('#HID_monday').val( this.checked ? 'True' : 'False');
    });
    $('#tuesday').click(function(){
      $('#HID_tuesday').val( this.checked ? 'True' : 'False');
    });
    $('#wednesday').click(function(){
      $('#HID_wednesday').val( this.checked ? 'True' : 'False');
    });
    $('#thursday').click(function(){
      $('#HID_thursday').val( this.checked ? 'True' : 'False');
    });
    $('#friday').click(function(){
      $('#HID_friday').val( this.checked ? 'True' : 'False');
    });
    $('#saturday').click(function(){
      $('#HID_saturday').val( this.checked ? 'True' : 'False');
    });
  });


  // Add Event Button
  $("#add_event_submit").click(function() {
    $.ajax({
        url: '/addEvent',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
    // Wait 2 seconds before getting any other events
    setTimeout(
      function() {
        getEvents();
      }, 2000);
  });


});

// Tab function
// http://inspirationalpixels.com/tutorials/creating-tabs-with-html-css-and-jquery
jQuery(document).ready(function() {

  jQuery('.tabs .tab-links a').on('click', function(e) {
    var currentAttrValue = jQuery(this).attr('href');

    // Show/Hide tabs
    jQuery('.tabs ' + currentAttrValue).show().siblings().hide();

    // Change/remove current tab to active
    jQuery(this).parent('li').addClass('active').siblings().removeClass('active');

    e.preventDefault();
  });
});
