<!DOCTYPE html>
<html>
    <head>
        <title> Wild West Post Office | Manage</title>
	    <link rel="stylesheet" type="text/css" href="/assets/css/foundation.css" />
	    <script type="text/javascript" src="/assets/js/vendor/foundation.js"></script>
	    <meta name="description" content="Main site featuring Discord multi-task bot Wild West Post Office!" />
	    <meta name="keywords" content="discord, bot" />
	    <meta name="author" content="Lukas" />
	    <meta charset="UTF-8" />
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        Manage</br>
        USER_DATA: <?php echo json_encode(Session::get('user_data')); ?></br>
        GUILDS_DATA: <?php echo json_encode(Session::get('guilds_data')); ?></br>
    </body>
</html>
