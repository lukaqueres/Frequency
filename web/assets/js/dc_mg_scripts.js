function changewindowcontent($target, $button, $targetbutton) {
  //$test = 1;
  //if $target.classList.contains("show") {
    //$test = 1;
  //} else {
    $button.classList.remove("active");
    $targetbutton.classList.add("active");
    $target.classList.toggle("show");
    //$button.classList.toggle("active");
    //$targetbutton.classList.toggle("active");
  }
}
