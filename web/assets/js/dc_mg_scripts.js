function plusWindow(n) {
  showWindow(windowIndex += n);
}

function currentWindow(n) {
  showWindow(windowIndex = n);
}

function showWindow(n) {
  var i;
  var windows = document.getElementsByClassName("windowcontent");
  var btns = document.getElementsByClassName("windowContentBtn");
  if (n > windows.length) {windowIndex = 1}    
  if (n < 1) {windowIndex = windows.length}
  for (i = 0; i < windows.length; i++) {
      windows[i].style.display = "none";  
  }
  for (i = 0; i < btns.length; i++) {
      btns[i].className = btns[i].className.replace(" active", "");
  }
  windows[windowIndex-1].style.display = "block";  
  btns[windowIndex-1].className += " active";
}
