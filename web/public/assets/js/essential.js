const pass = () => {}

function OnStart() {
    //var dropdownButtons = document.querySelector(".menu .button");
    var menus = document.querySelectorAll(".menu");
    let dropdownButtons = Array();
    if (!menus) {
        pass();
    } else {
        for (const menu of menus) {
            dropdownButtons.push(menu.getElementsByClassName('button'));
        }
        console.log('Buttons Lenght: ' + dropdownButtons.lenght + ' , Menus Lenght: ' + menus.lenght);
        AddOnClick(dropdownButtons, 'OpenDropdown(event)');
    }
}

OnStart();

window.onclick = function (event) {
    CloseDropdownOnClick(event);
}

function AddOnClick(object, task) {
    if (object instanceof Array) {
        for (const node of object) {
            node.setAttribute("onclick", task);
        }
    } else {
        object.setAttribute("onclick", task);
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
    var activeMenus = menus.querySelectorAll(".show");
    if (!activeMenus) {
        return;
    }
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
