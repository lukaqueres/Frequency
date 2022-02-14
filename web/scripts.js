function scrollFunction(mybutton, id) {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    animate(id)
  } else {
    animate(id)
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
} 

function animate(id) {
    x = id
    if (x.classList.contains("hide")) {
      x.classList.remove("hide");
    } else {
      x.classList.add("hide");
    }
}
