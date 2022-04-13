<!DOCTYPE html>
<html>
    <head>
        <title> Wild West Post Office | Manage</title>

	    <link rel="stylesheet" type="text/css" href="/assets/css/app.css" />
        <link rel="stylesheet" type="text/css" href="/assets/css/foundation.css" />

	    <script type="text/javascript" src="/assets/js/app.js"></script>
	    <meta name="description" content="Main site featuring Discord multi-task bot Wild West Post Office!" />
	    <meta name="keywords" content="discord, bot" />
	    <meta name="author" content="Lukas" />
	    <meta charset="UTF-8" />
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <?php
        // Get variables from Session data
        $snippets = Session::get('data')['guilds']['snippets'];
    ?>
    <body>
        <div class="grid-y medium-grid-frame">
            <div class="header">
                <h1 class="inline-margin">HEADER</h1>
            </div>
            <div class="left">
                <?php
                    $flow = '<div class="grid-container"><div class="grid-x grid-margin-x small-up-2 medium-up-3">';
                    $count = 0;
                        foreach($snippets as $guild) {
                            $flow .= '<div class="cell"><div class="card">
                              <div class="card-divider"><h4>' . $guild['name'] . '</h4></div>
                                        <div class="card-section">
                                        <img class="columns align-self-middle shrink icon inline-margin" src="' . get_icon($guild) .'"/>
                                        
                                        <p> TAGS </p>
                                        </div></div></div>';
                            $count = $count + 1;
                        }
                    echo $flow . '</div>';
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
