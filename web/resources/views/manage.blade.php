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
        $data = Session::get('data');
        $user = Session::get('user');
        $guilds = $data['guilds'];
        $snippets = $data['snippets'];
    ?>
    <body>
        <div class="app-grid-container">
            <div class="app-left">
                <div class="row align-spaced align-middle">
                        <div class="column small-4"><img class="app-icon" src= <?php echo '"' . get_avatar($user) . ' " >' ?></div>
                        <div class="column small-4"> <?php echo $user->username; ?> </div>
                </div>
                <?php
                    $flow = '<div class="grid-container"><div class="grid-x grid-margin-x small-up-2 medium-up-3">';
                    $count = 0;
                        foreach($snippets as $guild) {
                            $flow .= '<div class="cell"><div class="card">
                              <div class="card-divider"><img class="columns align-self-middle shrink app-icon app-inline-margin" src="' . get_icon($guild) .'"/><h4>' . $guild['name'] . '</h4></div>
                                        <div class="card-section">
                                        <p> TAGS </p>
                                        </div></div></div>';
                            $count = $count + 1;
                        }
                    echo $flow . '</div></div>';
                ?>
            </div>
            <div class="app-main">
                <h5>DATA: <?php echo json_encode(Session::get('data'), JSON_PRETTY_PRINT); ?></br></h5>
            </div>
        </div>
    </body>
</html>
