var windowIndex = 1;
currentWindow(1);

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
  if (windowIndex === null) { windows[1].style.display = "block";  }
  else { windows[windowIndex-1].style.display = "block";  }
  btns[windowIndex-1].className += " active";
}

function search_guilds() {
    var input, filter, tabel, tr, a, i, txtValue;
    input = document.getElementById("servers_search");
    filter = input.value.toUpperCase();
    tabel = document.getElementById("servers");
    tr = tabel.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        //a = tr[i].getElementsByTagName("a")[0];
        a = tr[i];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}
