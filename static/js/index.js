url = window.location.href
let params = (new URL(url)).searchParams
var hexDigits = new Array
        ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"); 

function hex(x) {
  return isNaN(x) ? "00" : hexDigits[(x - x % 16) / 16] + hexDigits[x % 16];
}

function rgb2hex(rgb) {
  rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
  try {
    return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
  }
  catch(err) {
    console.log(err);
  }
}

var $ = jQuery;
$("#export").on("click", function() {
  alert("exporting csv")
  var data = {
    username: params.get("user"),
  };
  $.ajax({
    type: 'POST',
    url: '/export_csv',
    data: JSON.stringify(data),
    dataType: 'json',
    contentType: 'application/json; charset=utf-8'
  }).done(function(msg) {
    alert("Data Saved: " + msg);
  });
})

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
    divId = range.startContainer.parentNode.id;
    tagName = range.startContainer.parentNode.tagName; // if font and not div
    if (divId == "P" || divId == "H" || tagName == "FONT") {
      document.execCommand("ForeColor", false, "white");
      document.execCommand("HiliteColor", false, "#7bfc03");
      // console.log("start=",range.startOffset,"end=",range.endOffset);
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
      document.execCommand("HiliteColor", false, "#30d5c8");
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

  document.getElementById("m").onclick = function() {
    var selected_text = window.getSelection().toString();
    selected_text;
  }

  document.getElementById("XP").onclick = function() {
    var P = document.getElementById("P")
    P.innerHTML = P.textContent
  }

  document.getElementById("XH").onclick = function() {
    var H = document.getElementById("H")
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
      document.execCommand("HiliteColor", false, "#fff");
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
$("#S").on("click", function() {
  // sentence1: document.getElementById("P").innerHTML,
  // sentence2: document.getElementById("H").innerHTML
  var P = document.getElementById("P");
  var H = document.getElementById("H");
  var FP = P.getElementsByTagName('font');
  var FH = H.getElementsByTagName('font');
  var EP = ""; var CP = ""; var NP = ""; var UP = "";
  var EH = ""; var CH = ""; var NH = ""; var UH = "";
  for (phrase of FP) {
    if (rgb2hex(phrase.style.backgroundColor) == "#7bfc03") {
      // deal with entailment cases.
      EP += phrase.innerText+"• ";
    }
    else if (rgb2hex(phrase.style.backgroundColor) == "#fc3003") {
      // deal with contradiction cases.
      CP += phrase.innerText+"• ";
    }
    else if (rgb2hex(phrase.style.backgroundColor) == "#fce303") {
      // deal with neutral cases.
      NP += phrase.innerText+"• ";
    }
    else if (rgb2hex(phrase.style.backgroundColor) == "#30d5c8") {
      // deal with unaligned premise.
      UP += phrase.innerText+"• ";
    }
  }
  for (phrase of FH) {
    if (rgb2hex(phrase.style.backgroundColor) == "#7bfc03") {
      // deal with entailment cases.
      EH += phrase.innerText+"• ";
    }
    else if (rgb2hex(phrase.style.backgroundColor) == "#fc3003") {
      // deal with contradiction cases.
      CH += phrase.innerText+"• ";
    }
    else if (rgb2hex(phrase.style.backgroundColor) == "#fce303") {
      // deal with neutral cases.
      NH += phrase.innerText+"• ";
    }
    else if (rgb2hex(phrase.style.backgroundColor) == "#30d5c8") {
      // deal with unaligned premise.
      UH += phrase.innerText+"• ";
    }
  }
  document.getElementById("EP").innerText = EP;
  document.getElementById("CP").innerText = CP;
  document.getElementById("NP").innerText = NP;
  document.getElementById("UP").innerText = UP;
  document.getElementById("EH").innerText = EH;
  document.getElementById("CH").innerText = CH;
  document.getElementById("NH").innerText = NH;
  document.getElementById("UH").innerText = UH;

  var data = {
    id: params.get("id"),
    username: params.get("user"),
    EP: document.getElementById("EP").innerText,
    CP: document.getElementById("CP").innerText,
    NP: document.getElementById("NP").innerText,
    UP: document.getElementById("UP").innerText,
    EH: document.getElementById("EH").innerText,
    CH: document.getElementById("CH").innerText,
    NH: document.getElementById("NH").innerText,
    UH: document.getElementById("UH").innerText
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

