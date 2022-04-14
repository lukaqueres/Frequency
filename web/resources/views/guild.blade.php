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
        <div class="app-grid-container">
            <div class="app-left">
                Back to manage
                <div class="app-flex-container">
                    <div class="app-align-right"><img class="app-icon" src= <?php echo '"' . get_avatar($user) . ' " >' ?></div>
                    <div class="app-align-right"> <?php echo $user->username; ?> </div>
                </div>
                <div class="app-dropdown">
                    <button onclick="search_dropdown()"> <?php echo $thisGuild->name; ?> </button>
                    <div id="app-search-dropdown" class="app-dropdown-content">
                        <input type="text" id="app-servers-search" onkeyup="search_guilds();" placeholder= <?php echo '"' . $thisGuild->name . '" '; ?> title="Filter by name or id">
                        <table style="border-collapse: collapse; border-spacing: 0; width: 100%;" id="ap-servers">
                            <?php
                                foreach($snippets as $guild) {
									echo '<tr id="search_dropdown_' . $guild['id'] .'_" class="app-flex_container" >
										<td class="app-flex_container" style="padding: 5px; margin-inline: 30px;" >
											<img class="icon no_margin" src="' . get_icon($guild) . '"/>
											<h1 class="no_margin w_padding max_font">' . $guild['name'] . '</h1>
										</td>
								     	<td class="no-display">' . $guild['id'] . '</td></tr>';
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
        document.getElementById("app-search-dropdown").classList.add("app-show");
        IdOfElement = document.getElementById( <?php echo '"search_dropdown_'.$thisGuild->id . '_"'; ?>);
        var topPos = IdOfElement.offsetTop;
        document.getElementById('app-search-dropdown').scrollTop = topPos;
    }

    window.onclick = function(event) {
	    if (!event.target.matches('#app-search-dropdown')) {
		    var dropdown = document.getElementById("app-search-dropdown");
		    if (dropdown.classList.contains('app-show')) {
			    dropdown.classList.remove('app-show');
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
