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
    // Colorize text if it belongs to P or H or "FONT" tag
    divId = sel.getRangeAt(0).startContainer.parentNode.id;
    tagName = sel.getRangeAt(0).startContainer.parentNode.tagName; // if font and not div
    if (divId == "P" || divId == "H" || tagName == "FONT") {
      document.execCommand("ForeColor", false, "white");
      document.execCommand("HiliteColor", false, "#7bfc03");
    }
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
    // Colorize text if it belongs to P or H or "FONT" tag
    divId = sel.getRangeAt(0).startContainer.parentNode.id;
    tagName = sel.getRangeAt(0).startContainer.parentNode.tagName; // if font and not div
    divId = sel.getRangeAt(0).startContainer.parentNode.id;
    if (divId == "P" || divId == "H" || tagName == "FONT") {
      document.execCommand("ForeColor", false, "white");
      document.execCommand("HiliteColor", false, "#fc3003");
    }
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
    // Colorize text if it belongs to P or H or "FONT" tag
    divId = sel.getRangeAt(0).startContainer.parentNode.id;
    tagName = sel.getRangeAt(0).startContainer.parentNode.tagName; // if font and not div
    if (divId == "P" || divId == "H" || tagName == "FONT") {
      document.execCommand("ForeColor", false, "white");
      document.execCommand("HiliteColor", false, "#fce303");
    }
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
    // Colorize text if it belongs to P or H or "FONT" tag
    divId = sel.getRangeAt(0).startContainer.parentNode.id;
    tagName = sel.getRangeAt(0).startContainer.parentNode.tagName; // if font and not div
    if (divId == "P" || divId == "H" || tagName == "FONT") {
      document.execCommand("ForeColor", false, "white");
      document.execCommand("HiliteColor", false, "turquoise");
    }
    // Set design mode to off
    document.designMode = "off";
  }

  document.getElementById("X").onclick = function() {
    var P = document.getElementById("P")
    var H = document.getElementById("H")
    P.innerHTML = P.textContent
    H.innerHTML = H.textContent
  }

  document.getElementById("x").onclick = function() {
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
    // Colorize text if it belongs to P or H or "FONT" tag
    divId = sel.getRangeAt(0).startContainer.parentNode.id;
    tagName = sel.getRangeAt(0).startContainer.parentNode.tagName; // if font and not div
    if (divId == "P" || divId == "H" || tagName == "FONT") {
      document.execCommand("ForeColor", false, "black");
      document.execCommand("HiliteColor", false, "white");
    }
    // Set design mode to off
    document.designMode = "off";
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

  document.getElementById("collapse").onclick = function() {
    var statusbar = document.getElementById("statusbar")
    if (statusbar == null) {
      var statusbar = document.getElementById("statusbar_hide")
      statusbar.id = "statusbar"
      var contentWrapper = document.getElementById("contentwrapper_max")
      contentWrapper.id = "contentwrapper"
      var rightColumn = document.getElementById("rightcolumn_hide")
      rightColumn.id = "rightcolumn"
    }
    else {
      statusbar.id = "statusbar_hide"
      var contentWrapper = document.getElementById("contentwrapper")
      contentWrapper.id = "contentwrapper_max"
      var rightColumn = document.getElementById("rightcolumn")
      rightColumn.id = "rightcolumn_hide"
    }
  }