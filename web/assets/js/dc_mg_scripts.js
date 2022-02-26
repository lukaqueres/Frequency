function changewindowcontent($target, $button, $targetbutton, $classobjects) {
  //if $target.classList.contains("show") {
    //$x = 1
  //} else {
    $button.classList.remove("active");
    $targetbutton.classList.add("active");
    $classobjects.classList.remove("show");
    $target.classList.toggle("show");
    //$button.classList.toggle("active");
    //$targetbutton.classList.toggle("active");
  //}
}
