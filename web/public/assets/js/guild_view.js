function txtSettingsView(object) {
    const xhttp = new XMLHttpRequest();
    let obj = document.getElementById(object);
    xhttp.onload = function () {
        obj.innerHTML = this.responseText;
    }
    xhttp.open("GET", "/data/guild/<?php echo $guild->id; ?>?operation=getview&view=textSettings");
    xhttp.send();
    goTo("Text Settings", "Plan It | Txt settings", '/manage/guild/<?php echo $id; ?>/text-settings');
}

function AJAXtest() { //TEST
    const xhttp = new XMLHttpRequest();
    let test = document.getElementById("test_xyz");
    xhttp.onload = function () {
        test.innerHTML = this.responseText;
    }
    xhttp.open("GET", "/data/guild/<?php echo $guild->id; ?>?status='test'");
    xhttp.send();
}
