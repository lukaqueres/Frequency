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
                <div class="grid-container">
                    <?php
                        $flow = '<div class="grid-container">';
                        $count = 0;
                        foreach($snippets as $guild) {
                            if ($count == 0) { $flow .= '<div class="grid-x grid-margin-x small-up-2 medium-up-3">'; }
                            $flow .= '<div class="cell"><div class="card">
                                        
                                        <div class="card-section">
                                        <img class="columns align-self-middle shrink icon inline-margin" src="' . get_icon($guild) .'"/>
                                        <h4>' . $guild['name'] . '</h4>
                                        <p> TAGS </p>
                                    </div></div></div>';
                            if ($count == 0) { $flow .= '</div>'; $count = 0; continue;}
                            $count += 1;
                        }
                        echo $flow;
                    ?>
                    </div>
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
