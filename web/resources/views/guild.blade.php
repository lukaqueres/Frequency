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
        Guild</br>
        NAME:{{Session::get('name')}}</br>
        GUILD_DATA: <?php
        $data = Session::get('data')['guilds'];
        if (Arr::exists($data, $id))  {
            echo json_encode($data[$id]);
        } else {
            echo 'No guild found';
        }
        ?></br>
    </body>
</html>
