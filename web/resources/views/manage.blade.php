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
    <?php /* 
            <?php if (Session::exists('notification')) { ?>
                <div id="blur" class="app-grid-container active">
                    <div id="guildPop-up" class="pop-up active">
                    <?php echo 'status: ' . json_encode(Session::get('notification')); ?>
                    <button onclick='togglePopUp("statusPop-up")'>Close</button>
                    </div>;
            <?php } else { ?>
                <div id="blur" class="app-grid-container">
            <?php } ?>
            <div class="app-left">
                Back to manage
                <div class="app-flex-container">
                    <div class="app-align-right"><img class="app-icon" src= <?php echo '"' . get_avatar($user) . ' " >' ?></div>
                    <div class="app-align-right"> <?php echo $user->username; ?> </div>
                </div>
                <?php
                    $flow = '<div class="grid-container"><div class="grid-x grid-margin-x small-up-2 medium-up-3">';
                    $count = 0;
                        foreach($guilds as $guild) {
                            $flow .= '<div class="cell"><div class="card">
                              <div class="card-divider"><img class="columns align-self-middle shrink app-icon app-inline-margin" src="' . $guild->icon_url .'"/><h4>' . $guild->name . '</h4></div>
                                        <div class="card-section">
                                        <p> TAGS </p>
                                        </div></div></div>';
                            $count = $count + 1;
                        }
                    echo $flow . '</div></div>';
                ?>
            </div>
            <div class="app-main">
                <h5>DATA: <?php echo json_encode($guilds, JSON_PRETTY_PRINT); ?></br></h5>
            </div>
        </div>
        */?>
    </body>
</html>
