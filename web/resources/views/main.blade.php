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
    <body>
        Main</br>
        <a href='https://discord.com/api/oauth2/authorize?client_id=875271995644842004&state=%2Fmanage%2Fguild%2F640181649463705650&redirect_uri=https%3A%2F%2Fweb-plan-it.herokuapp.com%2Fdiscord%2Fauthorize&response_type=code&scope=identify%20email%20guilds%20guilds.members.read'> AUTHORIZE FOR GUILD</a>
        <a href='https://discord.com/api/oauth2/authorize?client_id=875271995644842004&redirect_uri=https%3A%2F%2Fweb-plan-it.herokuapp.com%2Fdiscord%2Fauthorize&response_type=code&scope=identify%20email%20guilds%20guilds.members.read'> AUTHORIZE </a>
        <div id="notification-container" class="flex vertical">
            <?php
                if (Session::exists('notification')) {
                    $notification = Session::get('notification');
                    $notifynode = $notification->node;
                    echo $notifynode;
                }
            ?>
            <div class="notification">
                <p>User not authorized</p>
                <h5>Authorize to continue</h5>
                <button class="close" onclick="closeParent(event)">Close notification</button>
            </div>
            <div class="notification">
                <h5>status</h5>
                <button class="close" onclick="closeParent(event)">Close notification</button>
            </div>
            <div class="notification">
                <h5>status</h5>
                <button class="close" onclick="closeParent(event)">Close notification</button>
            </div>
        </div>
    </body>
</html>
