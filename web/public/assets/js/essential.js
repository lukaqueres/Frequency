const pass = () => {} // create function to let write some nice 'pass()' on if or something

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

    var slideshows = Array(); // Assigning onclick event to slideshow menus buttons
    slideshows = document.querySelectorAll('.menu.slider');
    let slideshowsButtons = Array();
    if (slideshows.length == 0) {
        pass();
    } else {
        for (const slideshow of slideshows) {
            slideshowsButtons.push(slideshow.querySelectorAll('.button'));
            console.log('Slideshowsbuttonsadd: ' + slideshowsButtons);
        }
        AddOnClick(slideshowsButtons, 'ChangeSlide(event)');
    } // End of assigning onclick event to slideshow menus buttons
    console.log('Slideshows: ' + slideshows + ' ,Buttons: ' + slideshowsButtons);
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
            console.log('DBUG: ' + node);
            node.setAttribute("onclick", task);
        }
    } else {
        collection.setAttribute("onclick", task);
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
// <>------------------------------------------<> SLIDESHOW FUNCTIONS <>----------------------------------------------------------------------------------------<>
//
// These functions are used to mentain divs slideshows with only css configuration on html file.
// All what is needed while creating div slideshow, is to correctly assign css classes to divs.
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
// <>----------------------------------------<> SLIDESHOW FUNCTIONS CODE <>--------------------------------------------------------------------------------------<>
//

function ChangeSlide(e) { // This function will open dropdown depending on button clicked
    var buttoncontainer = e.target.parentNode;
    if (!buttoncontainer.classList.contains('buttons')) {
        buttoncontainer = buttoncontainer.parentNode;
    }

    var nOfButton = 0;
    var buttons = buttoncontainer.childNodes;
    for (var i = 0; i < buttons.length; i++) {
        if (buttons[i] == e.target) {
            nOfButton = i;
            break;
        }
    }

    var container = e.target.parentNode;
    if (!container.classList.contains('slider')) {
        container = container.parentNode;
    }

    var slides = container.querySelector('.slides');
    var slides = slides.childNodes;
    for (const slide of slides) {
        if (slide.classList.contains('show')) {
            slide.classList.remove('show');
        }
    }
    slides[nOfButton].classList.add('show');
}
