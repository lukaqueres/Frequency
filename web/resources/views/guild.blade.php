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
                        <input type="text" id="servers_search" onkeyup="search_guilds();" placeholder= <?php echo '"' . $thisGuild->name . '" '; ?> title="Filter by name or id">
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
        //var IdOfElement = document.getElementById( <?php echo '"search_dropdown_'.$thisGuild->id . '_"'; ?>);
        //var topPos = IdOfElement.offsetTop;
        //document.getElementById('app-search-dropdown').scrollTop = topPos;
    }

    window.onclick = function(event) {
	    if (!event.target.matches('#app-user-dropdown') && document.getElementById("app-user-dropdown").classList.contains('app-show')) {
		    var dropdown = document.getElementById("app-user-dropdown");
		    if (dropdown.classList.contains('app-show')) {
			    dropdown.classList.remove('app-show');
		    }
	    }
	    if ((!event.target.matches('#app-servers-search')) && ((!event.target.matches('#app-search-dropdown'))) && document.getElementById("app-search-dropdown").classList.contains('app-show')) {
		    var dropdown = document.getElementById("app-search-dropdown");
		    if (dropdown.classList.contains('app-show')) {
			    dropdown.classList.remove('app-show');
		    }
	    }
    }
</script>
