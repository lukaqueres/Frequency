const pass = () => {}

function OnStart() {
    //var dropdownButtons = document.querySelector(".menu .button");
    var menus = Array();
    menus = document.querySelectorAll(".menu");
    let dropdownButtons = Array();
    if (menus.length == 0) {
        pass();
    } else {
        for (const menu of menus) {
            dropdownButtons.push(menu.getElementsByClassName('button'));
        }
        AddOnClick(dropdownButtons, 'OpenDropdown(event)');
    }
}

window.onclick = function (event) {
    CloseDropdownOnClick(event);
}

function CollectionToArray(collection) {
    let array = Array();
    for (let i = 0; i < collection.length; i++) {
        array.push(collection[i]);
    }
    return array;
}


function AddOnClick(collection, task) {
    collection = CollectionToArray(collection);
    if (collection instanceof Array) {
        for (const node of collection) {
            console.log('Node: ' + node);
            node.setAttribute("onclick", task);
        }
    } else {
        collection.setAttribute("onclick", task);
    }
}

function OpenDropdown(e) {
    var container = e.target.parentNode;
    var content = container.querySelector(".content");
    content.classList.add("show");
}

function CloseDropdownOnClick(e) {
    var target = e.target;
    var menus = document.querySelectorAll(".menu .content");
    if (!activeMenus) {
        return;
    }
    var activeMenus = menus.querySelectorAll(".show");
    for (const menu of activeMenus) {
        if (menu == target || menu.contains(target)) {
            pass();
        } else {
            if (menu.classList.contains('show')) {
                content.classList.remove("show");
            }
        }
    }
}
