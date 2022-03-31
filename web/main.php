<!DOCTYPE html>
<html>
  <head>
    <title> Wild West Post Office | Main</title>
    <link rel="stylesheet" type="text/css" href="essential_styles.css" />
    <script type="text/javascript" src="assets/js/scripts.js"></script>
    <?php include("manageDB.php"); ?>
    <meta name="description" content="Main site featuring Discord multi-task bot Wild West Post Office!" />
    <meta name="keywords" content="discord, bot" />
    <meta name="author" content="Lukas" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <?php
    // Here we establish the connection. Yes, that is all.
    $pg_conn = pg_connect(pg_connection_string_from_database_url());
    $dbm = new DatabaseManager();

    require __DIR__ . "/config.php";
    require __DIR__ . "/includes/functions.php";
    require __DIR__ . "/includes/discord.php";
    
  ?>
    <body>
        <div id="header_panel" class="vertical_center flex_container">
            <h1 class="no_margin" > <?php echo $bot_name; ?> </h1>
            <a class="clearlink" href=<?php echo $bot_invite_link; ?> >Main</a>
            <a class="clearlink" href=<?php echo $bot_invite_link; ?> >Commands &amp; Modules</a>
            <a class="clearlink" href=<?php echo $bot_invite_link; ?> >Updates &amp; Changelog</a>
            <div class="no_margin">
                <?php
                if (isset($_SESSION['user']))
                {
                echo "<a id='headerbtn' href='./dc_mng'>
                    Manage
                </a>";
                }
                else
                {
                $auth_url = url($client_id, $redirect_url, $scopes);
                echo "<a id='headerbtn' href='$auth_url'>
                    Authorize
                </a>";
                }
                ?>
            </div>
        </div> <?php #END OF HEADER PANEL ?>

        <div class="grid_container">
            <div class="header">
                <h1 class="no_margin"> <?php echo $bot_name; ?> </h1>
                <a class="clearlink" href=<?php echo $bot_invite_link; ?> >Main</a>
                <a class="clearlink" href=<?php echo $bot_invite_link; ?> >Commands &amp; Modules</a>
                <a class="clearlink" href=<?php echo $bot_invite_link; ?> >Updates &amp; Changelog</a>
                <div class="no_margin">
                    <?php
                    if (isset($_SESSION['user']))
                    {
                    echo "<a id='headerbtn' href='./dc_mng'>
                        Manage
                    </a>";
                    }
                    else
                    {
                    $auth_url = url($client_id, $redirect_url, $scopes);
                    echo "<a id='headerbtn' href='$auth_url'>
                        Authorize
                    </a>";
                    }
                    ?>
                </div>
                <div class="left">
                    Left
                </div>
                <div class="main">
                    Main
                </div>
                <div class="right">
                    Right
                </div>
                <div class="footer">
                    Foooooooooter
                </div>
            </div>
        </div>
    </body>
</html> 
    
<script>
  function callshowtopmorePanel()
  {
    panel = document.getElementById("topPanel");
    showtopmorePanel(panel)
  }
  panel = document.getElementById("panel");
  // When the user scrolls down 20px from the top of the document, show the button
  window.onscroll = function() {scrollFunction(panel)};
</script>
