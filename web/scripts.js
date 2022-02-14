function scrollFunction(panel) {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
     panel.classList.toggle('hide');
     //panel.style.display = "block";
     //panel.classList.remove("hide");
     //animate(mybutton)
  } else {
     panel.classList.toggle('hide');
     //panel.classList.remove("hide");
     //animate(mybutton)
     //panel.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
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
