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
        <div id="container" class="grid-container">
            <div class="header">
                <h1 class="inline-margin">HEADER</h1>
            </div>
            <div class="left">
                <?php
                    $guilds = Session::get('data')['guilds'];
                    foreach($guilds as $guild) {
                        break;
                        //echo '<img class="icon no_margin" src="' . get_icon($guild) .'"/>';
                    }
                ?>
            </div>
            <div class="main">
                <h5>DATA: <?php echo json_encode(Session::get('data'), JSON_PRETTY_PRINT); ?></br></h5>
            </div>
            <div class="footer">
                FOOTA
            </div>
        </div>
    </body>
</html>
