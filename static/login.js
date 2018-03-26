var attempt = 5; // Variable to count number of attempts.
// Below function Executes on click of login button.
function validate(){
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  if ( username == "vertiGrow" && password == "intothegarden20*"){
    //alert ("Login successfully");
    // $.ajax({
    //     //url: '/LEDS',
    //     url: '/config',
    //     data: ,
    //     type: 'GET',
    //     success: function(response) {
    //         console.log(response);
    //     },
    //     error: function(error) {
    //         console.log(error);
    //     }
    // });
    window.location = "/config"; // Redirecting to other page.
    return false;
  } else {
    attempt --;// Decrementing by one.
    alert("You have left "+attempt+" attempt(s) left!");
    // Disabling fields after 3 attempts.
    if( attempt == 0){
      document.getElementById("username").disabled = true;
      document.getElementById("password").disabled = true;
      document.getElementById("submit").disabled = true;
      return false;
    }
  }
}
