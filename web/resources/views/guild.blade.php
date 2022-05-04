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
        <div id="blur" class="app-grid-container container">
            <?php if (Session::exists('status')) {
                echo '<div id="statusPop-up" class="pop-up active">status: ' . json_encode(Session::get('status')) . '<button onclick="togglePopUp("statusPop-up")">Close</button></div>';
            }?>
            <div id="guildPop-up" class="pop-up">
                guilds
                <button class="pop-upContent" onclick="togglePopUp('guildPop-up')">Close</button>
            </div>
            <div class="app-left">
                Back to manage
                <div class="app-flex-container">
                    <div class="app-align-right"><img class="app-icon" src= <?php echo '"' . get_avatar($user) . ' " >' ?></div>
                    <div class="app-align-right"> <?php echo $user->username; ?> </div>
                    <button onclick="togglePopUp('guildPop-up')">Guilds</button>
                </div>
                <div class="app-dropdown">
                    <div id="app-dropdown-button" class="app-flex-container" onclick="search_dropdown()"> <?php echo '<img class="app-icon" onclick="search_dropdown()" src="' . get_icon($thisGuild) . '"/><h4 class="app-no-margin" onclick="search_dropdown()">' . $thisGuild->name . '</h4>'; ?> </div>
                    <div id="app-search-dropdown" class="app-dropdown-content">
                    <div style="background-color: black; width: 100%; position: sticky; top: 0; z-index: 99;"><input type="text" id="app-servers-search" onkeyup="search_guilds();" placeholder= <?php echo '"' . $thisGuild->name . '" '; ?> title="Filter by name or id"></div>
                        <table style="border-collapse: collapse; border-spacing: 0; width: 100%;" id="app-servers">
                        <tr class="app-flex-container" style="padding-block: 10px;">
                        	<?php echo '<td class="app-flex-container" style="width: 100%; border-bottom: 1px #18181E solid;; padding: 5px;" ><a class="app-flex-container app-no-margin app-link-tag app-zoom" href="/manage/user">
								<img class="app-icon" src="' . get_avatar($user) . '"/> 
								<h3 class="app-no-margin">' . $user->username . '</h3></a>
								</td>
								<td class="app-no-display">' . $user->id . '</td>'; ?>
                        </tr>
                            <?php
                                foreach($snippets as $guild) {
									echo '<tr id="search_dropdown_' . $guild['id'] .'_" class="app-flex-container" >
										<td class="app-flex-container" style="width: 100%; padding: 5px;" ><a class="app-flex-container app-no-margin app-link-tag app-zoom" href="/manage/guild/' . $guild['id'] . '">
											<img class="app-icon" src="' . get_icon($guild) . '"/>
											<h3 class="app-no-margin">' . $guild['name'] . '</h3></a>
										</td>
								     	<td class="app-no-display">' . $guild['id'] . '</td></tr>';
								}
                            ?>
                        </table>
                    </div>
                </div>
            </div>
            <div class="app-main">
                GUILD_DATA:
                <?php
                if (Arr::exists($guilds, $id))  {
                    echo json_encode($thisGuild);
                } else {
                    echo 'No guild found';
                }
                ?></br>
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

    window.onclick = function(e) {
        if ((!e.target.matches('#app-dropdown-button')) && (!e.target.matches('#app-search-dropdown')) && (!e.target.matches('#app-servers-search'))) {
            var myDropdown = document.getElementById("app-search-dropdown");
            if (myDropdown.classList.contains('app-show')) {
                myDropdown.classList.remove('app-show');
            }
        }
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
</script>
