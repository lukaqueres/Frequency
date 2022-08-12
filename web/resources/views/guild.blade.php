<!DOCTYPE html>
<html>
    <head>
        <title> Plan It | Manage</title>
        <link rel="stylesheet" type="text/css" href="/assets/css/rooties.css" />
	    <link rel="stylesheet" type="text/css" href="/assets/css/app.css" />
        <link rel="stylesheet" type="text/css" href="/assets/css/essential.css" />
	    <script type="text/javascript" src="/assets/js/app.js"></script>
        <script type="text/javascript" src="/assets/js/essential.js"></script>
        <script type="text/javascript" src="/assets/js/guild_view.js"></script>
        <meta name="color-scheme" content="dark light";
	    <meta name="description" content="Main site featuring Discord multi-task bot Wild West Post Office!" />
	    <meta name="keywords" content="discord, bot" />
	    <meta name="author" content="Lukas" />
	    <meta charset="UTF-8" />
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>

    <?php
        $user = Session::get('user');
        $guilds = Session::get('guilds');
        $guild = $guilds[$id];
        $gid = $id;
        global $id; 
        $id = $gid; 
        $view = $view;
    ?>

    <body class= "dark">
        <div id="blur" class="container">
            <div id="notification-container" class="flex vertical">
                <?php
                    if (Session::exists('notification')) {
                        $notification = Session::get('notification');
                        $notifynode = $notification->node;
                        echo $notifynode;
                        Session::forget('notification');
                    }
                ?>
            </div>
            <?php if (Session::exists('status')) {
                echo '<div id="statusPop-up" class="pop-up active">status: ' . json_encode(Session::get('status')) . '<button onclick="togglePopUp("statusPop-up")">Close</button></div>';
            }?>
            <div id="guildPop-up" class="pop-up">
                <div>
                    <button class="close-btn" onclick="togglePopUp('guildPop-up')">X</button>
                    <input type="text" id="filter-guilds" onkeyup="filter_guilds();" placeholder= <?php echo '"' . $guild->name . '" '; ?> title="Filter by name or id">
                </div>
                <div id="guild-search">
                    <table id="guilds-table" class="pop-upContent" style="border-collapse: collapse; border-spacing: 0; width: 100%;">
                        <?php
                        foreach($guilds as $g) {
                            $display_tags = ['community', 'news', 'member', 'partnered', 'auto_moderation', 'owner', 'administrator', 'moderator', 'member'];
                            $tags = '';
                            foreach($g->tags as $tag) {
                                if (!(in_array( $tag, $display_tags))) {
                                    continue;
                                }
						        $tags = $tags . '<div class="tag">' . $tag . '</div>';
						    }
						    echo '<tr id="search_guild_' . $g->id .'" class="guild-row">
							    <td style="width: 100%; padding: 5px; border-block: solid 1px;" >
                                    <a href="/manage/guild/' . $g->id . '">
                                        <div class="flex">
									        <img class="icon" src="' . $g->icon_url . '"/>
									        <h3 class="guild-name app-no-margin">' . $g->name . '</h3>
                                            <h5 class="right">' . $g->id .'</h5>
                                        </div>
                                        <div class="tags">' . $tags . '</div>
                                    </a>
								</td>
                                </tr>';
						}
                        ?>
                    </table>
                </div>
            </div>
            <div class="page-header flex">
                <button type="text" class="center" id="head-button" onclick="togglePopUp('guildPop-up')" title="Search for guilds by name or id"><?php echo 'Search for guilds | ' . $guild->name; ?></button>
                <!--<button class="top-btn top center" onclick="togglePopUp('guildPop-up')">Choose guild</button>-->
                <div class="right menu dropdown flex">
                    <button class="button none flex">
                        <img class="icon" src= <?php echo '"' . get_avatar($user) . ' " >'; ?>
                    </button>
                    <div class="content">
                        <div class="flex vertical">
                            <h3><?php echo $user->username; ?></h3>
                            <a class="full-btn" href="/discord/logout">LogOut</a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="page-aside">
                <button class="expand-aside" onclick="shrinkAside()"><ion-icon name="chevron-back-outline"></ion-icon></button>
                <ul>
                    <?php echo '<li class="title tbutton"><a href="#"><span class="aside-icon"><img class="icon" src="' . $guild->icon_url . '"/></span><span class="title">' . $guild->name . '</span></a></li>'; ?>
                    <li class="space"></li>
                    <li <?php if($view == 'overview' || $view == '') { echo 'class="selected"';} ?> ><button onclick="changeView(event, 'main-window', 'overview')" ><span class="aside-icon" ><ion-icon name="apps-outline"></ion-icon></span><span class="title" >Overview</span></a></li>
                    <li <?php if($view == 'settings') { echo 'class="selected"';} ?><?php if(!$guild->has_bot) { echo 'class="disabled"';} ?> ><button onclick="changeView(event, 'main-window', 'settings')" ><span class="aside-icon" ><ion-icon name="build-outline"></ion-icon></span><span class="title" >Main settings</span></a></li>
                    <li <?php if($view == 'text-settings') { echo 'class="selected"';} ?><?php if(!$guild->has_bot) { echo 'class="disabled"';} ?> ><button onclick="changeView(event, 'main-window', 'textSettings')" ><span class="aside-icon" ><ion-icon name="create-outline"></ion-icon></span><span class="title" >Text settings</span></button></li>
                    <li <?php if($view == 'debug') { echo 'class="selected"';} ?> ><button onclick="changeView(event, 'main-window', 'debug')" ><span class="aside-icon" ><ion-icon name="terminal-outline"></ion-icon></span><span class="title" >Debug</span></button></li>
                    <li class="space"></li>
                    <li title="Main" ><a href="#" ><span class="aside-icon" ><ion-icon name="grid"></ion-icon></span><span class="title" >Main</span></a></li>
                    <li><a href="#" ><span class="aside-icon" ><ion-icon name="person-circle"></ion-icon></span><span class="title" >User</span></a></li>
                    <li><a href="#" ><span class="aside-icon" ><ion-icon name="help-circle"></ion-icon></span><span class="title" >Help</span></a></li>
                    <li><a href="#" ><span class="aside-icon" ><ion-icon name="information-circle"></ion-icon></span><span class="title" >About</span></a></li>
                </ul>
                <?php /*
                <div>
                    <button onclick="scrollDown()"><ion-icon name="chevron-up-outline"></ion-icon></button>
                    <ul class="scroll margin">
                        <?php
                        foreach($guilds as $g) {
                            echo '
                            <li>
                                <a href="/manage/guild/' . $g->id . '">
					                <span class="aside-icon"><img class="icon" src="' . $g->icon_url . '"/></span>
					                <span class="title">' . $g->name . '</span>
                                </a>
                            </li>';
                        }
                        ?>
                    </ul>
                    <button onclick="scrollUp()"><ion-icon name="chevron-down-outline"></ion-icon></button>
                </div>
                */ ?>
            </div>
            <?php // MAIN CONTANT - CAN CHANGE BETWEEN VIEWS ?>
            <div id="main-window" class="page-main">
                <?php if ($view == 'overview') {  // OVERVIEW VIEW ------------------------------------------------------------- ?>
                    <?php include('pages/guildView_overview_page.php'); ?>
                <?php } else if ($view == 'settings') { // SETTINGS VIEW --------------------------------------------------------------------?>
                    <?php include('pages/guildView_settings_page.php'); ?>
                <?php } else if ($view == 'text-settings') { // TEXT SETTINGS VIEW ---------------------------------------------------------- ?>
                    <?php include('pages/guildView_textSettings_page.php'); ?>
                <?php } else if ($view == 'debug') { // DEBUG VIEW -------------------------------------------------------------------------- -7760928402638897752 ?>
                    <?php include('pages/guildView_debug_page.php'); ?>
                <?php } ?>
            </div>
        </div>
        <?php // Because of shitty way I would have to deal with images in aside, I am using this as test/probably will stay, using https://ionic.io/ionicons ?>
        <script type="module" src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.esm.js"></script>
        <script nomodule src="https://unpkg.com/ionicons@5.5.2/dist/ionicons/ionicons.js"></script>
    </body>
</html>

<script>

    OnStart();
    const keywordentryexists = document.getElementById('keyword-entry') || false
    if (keywordentryexists) {
        var keywordEntry = document.getElementById("keyword-entry");
        keywordEntry.addEventListener("keydown", function (e) {
            if (e.code === "Enter") {  //checks whether the pressed key is "Enter"
                addInput();
            }
        });
    }
    function search_dropdown() {
        var Dropdown = document.getElementById("app-search-dropdown");
        if (!Dropdown.classList.contains('app-show')) {
            Dropdown.classList.add("app-show");
            IdOfElement = document.getElementById( <?php echo '"search_dropdown_'.$guild->id . '_"'; ?>);
            var topPos = IdOfElement.offsetTop;
            document.getElementById('app-search-dropdown').scrollTop = topPos;
        } else {
            Dropdown.classList.remove("app-show");
        }
    }

    /*window.onclick = function(e) {
        if ((!e.target.matches('#app-dropdown-button')) && (!e.target.matches('#app-search-dropdown')) && (!e.target.matches('#app-servers-search'))) {
            var myDropdown = document.getElementById("app-search-dropdown");
            if (myDropdown.classList.contains('app-show')) {
                myDropdown.classList.remove('app-show');
            }
        }
    }*/

    function addInput(e) {
        var keywordEntry = document.getElementById("keyword-entry");
        
        var keyword = keywordEntry.value;
        keywordEntry.value = '';
        keywordempty = keyword.replace(/\s/g, '');
        if (!keywordempty) {
            return notify( 'Empty keyword', "Provided keyword is empty, please input word to be selected.");
        };

        let count = document.getElementById("input-container").childElementCount;
        var container = document.getElementById("input-container");
        // Append a node with a random text
        // Create an <input> element, set its type and name attributes
        var div = document.createElement("div");

        div.className = "flex tag";
        //div.appendChild(document.createTextNode(count + 1));

        var input = document.createElement("input");
        var button = document.createElement("button");

        input.type = "text";
        input.name = "word-"+(count + 1);
        input.className = "cover key-word-input";
        input.setAttribute("value",keyword);
        input.setAttribute('maxlength','20');

        button.setAttribute("onclick",'removeInput(event)'); // "key-word-'+(count + 1)+'"
        button.innerText = "x";
        button.className = "key-word-button";
        button.type="button";

        div.id = "key-word-"+(count + 1);
        div.appendChild(input);
        div.appendChild(button);
        //button.addEventListener('click', function(){ removeInput();});
        container.appendChild(div);
        // Append a line break 
        //container.appendChild(document.createElement("br"));
    }

    function removeInput(e) {
        var div = e.target.parentNode; // document.getElementById(input);
        div.parentNode.removeChild(div);
    }

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

    function filter_guilds() {
        var input, filter, tabel, tr, a, i, txtValue;
        input = document.getElementById("filter-guilds");
        filter = input.value.toUpperCase();
        tabel = document.getElementById("guilds-table");
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

    function changeView(e, object, target) {
        const xhttp = new XMLHttpRequest();
        let obj = document.getElementById(object);
        xhttp.onload = function () {
            obj.innerHTML = this.responseText;
        }
        if (target == 'overview') {
            xhttp.open("GET", "/data/guild/<?php echo $guild->id; ?>?operation=getview&guildId=<?php echo $guild->id; ?>&view=overview");
            xhttp.send();
            goTo("Overview", "Plan It | Overview", '/manage/guild/<?php echo $id; ?>/overview');
        } else if (target == 'settings') {
            xhttp.open("GET", "/data/guild/<?php echo $guild->id; ?>?operation=getview&guildId=<?php echo $guild->id; ?>&view=settings");
            xhttp.send();
            goTo("Settings", "Plan It | Settings", '/manage/guild/<?php echo $id; ?>/settings');
        } else if (target == 'textSettings') {
            xhttp.open("GET", "/data/guild/<?php echo $guild->id; ?>?operation=getview&guildId=<?php echo $guild->id; ?>&view=textSettings");
            xhttp.send();
            goTo("Text Settings", "Plan It | Txt settings", '/manage/guild/<?php echo $id; ?>/text-settings');
        } else if (target == 'debug') {
            xhttp.open("GET", "/data/guild/<?php echo $guild->id; ?>?operation=getview&guildId=<?php echo $guild->id; ?>&view=debug");
            xhttp.send();
            goTo("Debug", "Plan It | Debug", '/manage/guild/<?php echo $id; ?>/debug');
        }

        var aside = document.querySelector(".page-aside");
        var links = aside.querySelectorAll("li");
        for (const link of links) {
            if (link.classList.contains('selected')) {
                link.classList.remove('selected');
            }
        }
        if ( e.target.tagName == 'li' ) {
            e.target.classList.add('selected');
        } else {
            let button = getParentElementByTag(e.target, 'li');
            button.classList.add('selected');
        }
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
</script>
