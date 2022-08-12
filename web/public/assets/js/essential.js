const pass = () => {} // create function to let write some nice 'pass()' on if or something


function getParentElement(node, requirement) {
    if (requirement.startsWith('.')) {  // We are looking for parent with class
        pass();
    } else if (requirement.startsWith('#')) { // We are looking for parent with id
        pass();
    } else { // We are looking for parent with tag
        pass(); 
    }
}

function getParentElementByClassName(node, className) {
    let nodeParent = node.parentNode;
    while (nodeParent) {
        if (!nodeParent.classList.contains(className)) {
            break;
        }
        nodeParent = nodeParent.parentNode;
    }
    return nodeParent;
}

function getParentElementByTag(node, tagName) {
    let nodeParent = node.parentNode;
    tagName = tagName.toUpperCase();
    while (nodeParent) {
        if (nodeParent.tagName == tagName) {
            break;
        }
        nodeParent = nodeParent.parentNode;
        if (nodeParent.tagName == 'body') {
            break;
        }
    }
    return nodeParent;
}

function OnStart() { // function to run on page creation

    var dropdownmenus = Array(); // Assigning onclick event to dropdown menus buttons
    dropdownmenus = document.querySelectorAll(".menu.dropdown");
    let dropdownButtons = Array();
    if (dropdownmenus.length == 0) {
        pass();
    } else {
        for (const menu of dropdownmenus) {
            dropdownButtons.push(...menu.querySelectorAll('.button'));
        }
        AddOnClick(dropdownButtons, 'OpenDropdown(event)');
    } // End of assigning onclick event to dropdown menu buttons

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


function AddOnClick(collection, task) { // Add onclick attribute to array of html elements or single ones
    collection = Array.from(collection);
    if (collection instanceof Array) {
        for (const node of collection) {
            //console.log('DBUG: ' + node);
            node.setAttribute("onclick", task);
        }
    } else {
        collection.setAttribute("onclick", task);
    }
}

function goTo(page, title, url) {
    if ("undefined" !== typeof history.pushState) {
        history.pushState({ page: page }, title, url);
    } else {
        window.location.assign(url);
    }
}


//
// <>-------------------------------------------<> DROPDOWN FUNCTIONS <>----------------------------------------------------------------------------------------<>
//
// These functions are used to mentain dropdown menus with only css configuration on html file.
// All what is needed while creating dropdown menu, is to correctly assign css classes to divs.
//
// main container div = 'menu dropdown'; within previous div add button and div with class 'content'.
// like this:
//
// <div class="menu dropdown">
//      <button>OPEN DROPDOWN</button>
//      <div class="content">CONTENT</div>
// </div>
//
// JS will automaticly add onclick attribute to button
//
// <>-----------------------------------------<> DROPDOWN FUNCTIONS CODE <>--------------------------------------------------------------------------------------<>
//
function OpenDropdown(e) { // This function will open dropdown depending on button clicked
    
    var container = e.target.parentNode;
    if (!container.classList.contains('dropdown')) {
        container = container.parentNode;
    }
    var content = container.querySelector('.content');
    if (content.classList.contains('show')) {
        content.classList.remove('show');
    } else {
        content.classList.add("show");
    }
}

function CloseDropdownOnClick(e) { // This will close dropdowns on click in window                  <-!-> NOT DEBUGGED <-!->
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

//
// <>---------------------------------------<> DROPDOWN FUNCTIONS CODE END <>------------------------------------------------------------------------------------<>
//

//
//  <>-------------------------------------<> LIGHT/DARK/SYSTEM COLOR MODES <>-----------------------------------------------------------------------------------<>
//
//  Automate changing color schemes on-site
//

let mode = localStorage.getItem('mode');
const modeToggler = document.querySelector('colors-mode-toggler');
const modes = ['system', 'dark', 'light'];

if (modeToggler) {
    modeToggler.addEventListener('click', toggleColorScheme());
}

function changeColorScheme(color = 'system') {
    let body = document.querySelector('body')
    switch (color) {
        case "light":
            if (body.classList.contains('dark')) {
                body.classList.remove('dark')
            }
            if (!body.classList.contains('light')) {
                body.classList.add('light')
            }
            break;
        case "dark":
            if (body.classList.contains('light')) {
                body.classList.remove('light')
            }
            if (!body.classList.contains('dark')) {
                body.classList.add('dark')
            }
            break;
        default:
            console.log("system")
            if (body.classList.contains('light')) {
                body.classList.remove('light')
            }
            if (body.classList.contains('dark')) {
                body.classList.remove('dark')
            }
            break;
    }
}

function toggleColorScheme() {
    mode = localStorage.getItem('mode');
    let nextmode = modes.indexOf(mode) + 1;
    if (modes.lenght < nextmode) {
        nextmode = 0;
    }
    mode = modes[nextmode];
    localStorage.setItem('mode', mode);
    changeColorScheme(mode);
}



//
// <>-------------------------------------------<> INPUT FUNCTIONS <>----------------------------------------------------------------------------------------<>
//
// With these functions there is ( hopefully ) no need to add any js functions or elements and only css and html to make nice unusual inputs.
// But classes must be assigned correctly - and it is a little more complicated than menus.
//
// main container div = 'menu dropdown'; within previous div add button and div with class 'content'.
// like this:
//
// <div class="menu dropdown">
//      <button>OPEN DROPDOWN</button>
//      <div class="content">CONTENT</div>
// </div>
//
// JS will automaticly add onclick attribute to button
//
// <>-----------------------------------------<> DROPDOWN FUNCTIONS CODE <>--------------------------------------------------------------------------------------<>
//

function shrinkAside() {
    //let toggle = document.querySelector('.expand-aside');
    let aside = document.querySelector('.page-aside');
    let main = document.querySelector('.page-main');
    aside.classList.toggle('shrink');
    main.classList.toggle('expand');
}

function scrollUp() {
    let window = document.querySelector('.scroll');
    window.scrollBy(0, 120);
}

function scrollDown() {
    let window = document.querySelector('.scroll');
    window.scrollBy(0, -120);
}

function notify(title, content) {
    var container = document.getElementById('notification-container');
    var div = document.createElement("div");
    div.className = "notification";

    let p = document.createElement("p");
    p.innerText = title;

    let h = document.createElement("h5");
    h.innerText = content;

    var button = document.createElement("button");
    button.setAttribute("onclick", 'closeParent(event)'); // "key-word-'+(count + 1)+'"
    button.innerText = "Close notification";
    button.className = "close";
    button.type = "button";

    div.appendChild(p);
    div.appendChild(h);
    div.appendChild(button);

    container.appendChild(div);
}
