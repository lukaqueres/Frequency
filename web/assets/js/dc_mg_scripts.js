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

function changeuserwindowcontent($button) {
  $button_overview = document.getElementById('buttonoverview');
  $button_servers = document.getElementById('buttonservers');
  $
  $button = document.getElementById($button);
  $target = document.getElementById($target);
  $targetbutton = document.getElementById($targetbutton);
  $test = 1;
  if ($target.classList.contains("show")) {
    $test = 1;
  } else {
    $button.classList.remove("active");
    $targetbutton.classList.add("active");
    $target.classList.toggle("show");
    //$button.classList.toggle("active");
    //$targetbutton.classList.toggle("active");
  }
}
