function changeuserwindowcontent($target, $button, $targetbutton) {
  $button = document.getElementById($button)
	$target = document.getElementById($target)
	$targetbutton = document.getElementById($targetbutton)
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
