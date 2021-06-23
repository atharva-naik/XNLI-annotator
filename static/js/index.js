url = window.location.href
let params = (new URL(url)).searchParams

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
    document.execCommand("HiliteColor", false, "#7bfc03");
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
    document.execCommand("HiliteColor", false, "#fc3003");
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
    document.execCommand("HiliteColor", false, "#fce303");
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
    document.execCommand("HiliteColor", false, "turquoise");
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
var $ = jQuery;
$("#S").on("click", function() {
  var data = {
    id: params.get("id"),
    sentence1: document.getElementById("P").innerHTML,
    sentence2: document.getElementById("H").innerHTML,
    username: params.get("user")
  };
  $.ajax({
    type: 'POST',
    url: '/save',
    data: JSON.stringify(data),
    dataType: 'json',
    contentType: 'application/json; charset=utf-8'
  }).done(function(msg) {
    alert("Data Saved: " + msg);
  });
})

function confirmSubmission() {
  var response = confirm("Do you want to confirm your submission? You wont't be able to edit your annotations any more, after you submit.")
  if (response == true) {
    window.location.href='/thankyou'
  } else {
    // do nothing
  }
}

