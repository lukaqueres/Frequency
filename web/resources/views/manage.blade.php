<!DOCTYPE html>
<html>
    <head>
        <title> Wild West Post Office | Manage</title>

	    <link rel="stylesheet" type="text/css" href="/assets/css/app.css" />
        <?php //<link rel="stylesheet" type="text/css" href="/assets/css/foundation.css" />?>

	    <script type="text/javascript" src="/assets/js/app.js"></script>
	    <meta name="description" content="Main site featuring Discord multi-task bot Wild West Post Office!" />
	    <meta name="keywords" content="discord, bot" />
	    <meta name="author" content="Lukas" />
	    <meta charset="UTF-8" />
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <?php
        // Get variables from Session data
        //$data = Session::get('data');
        $user = Session::get('user');
        //$guilds = $data['guilds'];
        //$snippets = $data['snippets'];
        $guilds = Session::get('guilds');
    ?>
    <body>
    <div id="notification-container" class="flex vertical">
        <?php
            if (Session::exists('notification')) {
                $notification = Session::get('notification');
                $notifynode = $notification->node;
                echo $notifynode;
            }
        ?>
    </div>
        <div class="container">
            <ul class="margin">
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
        </div>
    </body>
</html>
