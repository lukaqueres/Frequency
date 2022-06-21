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
        <a href='https://discord.com/api/oauth2/authorize?client_id=875271995644842004&state=%2Fmanage%2Fguild%2F640181649463705650&redirect_uri=https%3A%2F%2Fweb-plan-it.herokuapp.com%2Fdiscord%2Fauthorize&response_type=code&scope=identify%20email%20guilds%20guilds.members.read'> AUTHORIZE </a>
        <?php if (Session::exists('status')) {
            echo 'status: ' . json_encode(Session::get('status'));
        }?>
    </body>
</html>
