const pass = () => {}

function OpenDropdown(e) {
    var container = e.target.parentNode;
    var content = container.querySelector(".content");
    content.classList.add("show");
}

function CloseDropdownOnClick(e) {
    var target = e.target;
    var menus = document.querySelector(".menu .content");
    var activeMenus = menus.querySelector(".show");
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
