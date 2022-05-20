<!DOCTYPE html>
<html>
    <head>
        <title> Wild West Post Office | Manage</title>
	    <link rel="stylesheet" type="text/css" href="/assets/css/app.css" />
	    <script type="text/javascript" src="/assets/js/app.js"></script>
	    <meta name="description" content="Main site featuring Discord multi-task bot Wild West Post Office!" />
	    <meta name="keywords" content="discord, bot" />
	    <meta name="author" content="Lukas" />
	    <meta charset="UTF-8" />
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <?php
        // Get variables from Session data
        $data = Session::get('data');
        $user = Session::get('user');
        $guilds = $data['guilds'];
        $snippets = $data['snippets'];
        $thisGuild = $guilds[$id];
    ?>
    <body>
        <div id="blur" class="container">
            <?php if (Session::exists('status')) {
                echo '<div id="statusPop-up" class="pop-up active">status: ' . json_encode(Session::get('status')) . '<button onclick="togglePopUp("statusPop-up")">Close</button></div>';
            }?>
            <div id="guildPop-up" class="pop-up">
                <div>
                    <button class="close-btn" onclick="togglePopUp('guildPop-up')">X</button>
                    <input type="text" id="filter-guilds" onkeyup="filter_guilds();" placeholder= <?php echo '"' . $thisGuild->name . '" '; ?> title="Filter by name or id">
                </div>
                <div id="guild-search">
                    <table id="guilds-table" class="pop-upContent" style="border-collapse: collapse; border-spacing: 0; width: 100%;">
                        <?php
                        foreach($snippets as $guild) {
                            $display_tags = ['community', 'news', 'member', 'partnered', 'auto_moderation', 'owner', 'administrator', 'moderator', 'member'];
                            $tags = '';
                            foreach($guild['tags'] as $tag) {
                                if (!(in_array( $tag, $display_tags))) {
                                    continue;
                                }
						        $tags = $tags . '<div class="tag">' . $tag . '</div>';
						    }
						    echo '<tr id="search_guild_' . $guild['id'] .'" class="guild-row">
							    <td style="width: 100%; padding: 5px; border-block: solid 1px;" >
                                    <a href="/manage/guild/' . $guild['id'] . '">
                                        <div class="flex">
									        <img class="app-icon" src="' . get_icon($guild) . '"/>
									        <h3 class="guild-name app-no-margin">' . $guild['name'] . '</h3>
                                            <h5 class="right">' . $guild['id'] .'</h5>
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
                <a class="small text" href="/manage">< Return</a>
                <button type="text" id="head-button" onclick="togglePopUp('guildPop-up')" title="Search for guilds by name or id"><?php echo 'Search for guilds | ' . $thisGuild->name; ?></button>
                <button class="top-btn top center" onclick="togglePopUp('guildPop-up')">Choose guild</button>
                <img class="icon right" src= <?php echo '"' . get_avatar($user) . ' " >'; ?>
            </div>
            <div class="page-aside">
                /
            </div>
            <div class="app-main page-main">
                <h5>GUILD_DATA:
                <?php
                if (Arr::exists($guilds, $id))  {
                    echo json_encode($thisGuild);
                } else {
                    echo 'No guild found';
                }
                ?></br></h5>
            </div>
        </div>
    </body>
</html>

<script>
    function search_dropdown() {
        var Dropdown = document.getElementById("app-search-dropdown");
        if (!Dropdown.classList.contains('app-show')) {
            Dropdown.classList.add("app-show");
            IdOfElement = document.getElementById( <?php echo '"search_dropdown_'.$thisGuild->id . '_"'; ?>);
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
</script>
