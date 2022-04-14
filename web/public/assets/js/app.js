$(document).foundation()

function search_guilds() {
    var input, filter, tabel, tr, a, i, txtValue;
    input = document.getElementById("app-servers-search");
    filter = input.value.toUpperCase();
    tabel = document.getElementById("app-servers");
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
