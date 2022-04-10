function scrollFunction(panel) {
  //panel.classList.toggle('hide');
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
     //panel.classList.toggle('hidden');
     panel.style.display = "block";
     //panel.classList.remove("hide");
     //animate(mybutton)
  } else {
     //panel.classList.toggle('hide');
     panel.classList.add("hidden");
     //animate(mybutton)
     //panel.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
} 

function moveFunction(panel) {
  panel.classList.toggle("expand");
} 

function animate(mybutton) {
    var x = mybutton
    //mybutton.classList.toggle('hide')
    //x.MyBtn.toggle('hide')
    if (x.classList.contains("hide")) {
      x.classList.remove("hide");
    } else {
      x.classList.add("hide");
    }
}

function showtopmorePanel(panel) {
  panel.classList.toggle("show");
} 