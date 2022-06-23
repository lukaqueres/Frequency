$(document).foundation()


function closeParent(e) {
    let deleteNode = e.target.parentNode;
    deleteNode.parentNode.removeChild(deleteNode);
}

function togglePopUp(popUp) {
    var blur = document.getElementById('blur');
    blur.classList.toggle('active');
    var popUp = document.getElementById(popUp);
    popUp.classList.toggle('active');
}

function arrRemove(arr, value) {

    return arr.filter(function (ele) {
        return ele != value;
    });
}

function random(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
}

/*function search_guilds() {
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
}*/
