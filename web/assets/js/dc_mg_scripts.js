function changewindowcontent($target, $buttontarget) {
  if !$buttontarget.classList.contains("active") {
    $x = 1
  } else {
    $target.classList.toggle("show");
    $buttontarget.classList.toggle("active");
  }
}
