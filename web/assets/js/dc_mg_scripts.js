function changewindowcontent($target, $button, $targetbutton) {
  //if $target.classList.contains("show") {
    //$x = 1
  //} else {
    $button.classList.remove("active");
    $targetbutton.classList.add("active");
    $target.classList.toggle("show");
    //$button.classList.toggle("active");
    //$targetbutton.classList.toggle("active");
  //}
}
