document.getElementById("E").onclick = function() {
    // Get Selection
    sel = window.getSelection();
    if (sel.rangeCount && sel.getRangeAt) {
      range = sel.getRangeAt(0);
    }
    // Set design mode to on
    document.designMode = "on";
    if (range) {
      sel.removeAllRanges();
      sel.addRange(range);
    }
    // Colorize text
    document.execCommand("ForeColor", false, "white");
    document.execCommand("HiliteColor", false, "green");
    document.execCommand();
    // Set design mode to off
    document.designMode = "off";
  }

document.getElementById("C").onclick = function() {
    // Get Selection
    sel = window.getSelection();
    if (sel.rangeCount && sel.getRangeAt) {
      range = sel.getRangeAt(0);
    }
    // Set design mode to on
    document.designMode = "on";
    if (range) {
      sel.removeAllRanges();
      sel.addRange(range);
    }
    // Colorize text
    document.execCommand("ForeColor", false, "white");
    document.execCommand("HiliteColor", false, "red");
    // Set design mode to off
    document.designMode = "off";
  }

document.getElementById("N").onclick = function() {
    // Get Selection
    sel = window.getSelection();
    if (sel.rangeCount && sel.getRangeAt) {
      range = sel.getRangeAt(0);
    }
    // Set design mode to on
    document.designMode = "on";
    if (range) {
      sel.removeAllRanges();
      sel.addRange(range);
    }
    // Colorize text
    document.execCommand("ForeColor", false, "white");
    document.execCommand("HiliteColor", false, "yellow");
    // Set design mode to off
    document.designMode = "off";
  }

document.getElementById("U").onclick = function() {
    // Get Selection
    sel = window.getSelection();
    if (sel.rangeCount && sel.getRangeAt) {
      range = sel.getRangeAt(0);
    }
    // Set design mode to on
    document.designMode = "on";
    if (range) {
      sel.removeAllRanges();
      sel.addRange(range);
    }
    // Colorize text
    document.execCommand("ForeColor", false, "white");
    document.execCommand("HiliteColor", false, "blue");
    // Set design mode to off
    document.designMode = "off";
  }

document.getElementById("X").onclick = function() {
    var P = document.getElementById("P")
    var H = document.getElementById("H")
    P.innerHTML = P.textContent
    H.innerHTML = H.textContent
}
// document.getElementById("S").onclick = function() {
//     var P = document.getElementById("P")
//     var H = document.getElementById("H")
//     P.innerHTML = P.textContent
//     H.innerHTML = H.textContent
//     alert("annotation saved!")
// }
function pushToServer() {
  // var data = {
  //   screening: '1',
  //   assistance: 'wheelchair access',
  //   guests: [
  //       {
  //           first: 'John',
  //           last: 'Smith'
  //       },
  //       {
  //           first: 'Dave',
  //           last: 'Smith'
  //       }
  //   ]
  // };
  // $.ajax({
  //   type: 'POST',
  //   url: window.location.href,
  //   data: JSON.stringify(response),
  //   dataType: 'json',
  //   contentType: 'application/json; charset=utf-8'
  // }).done(function(msg) {
  //   alert("Data Saved: " + msg);
  // });
  alert("annotation saved")
}

function confirmSubmission() {
  var response = confirm("Do you want to confirm your submission? You wont't be able to edit your annotations any more, after you submit.")
  if (response == true) {
    window.location.href='/thankyou'
  } else {
    // do nothing
  }
}