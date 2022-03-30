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
    <div class="header_panel">
        <h1> <?php echo $bot_name; ?> </h1>
        <?php
          if (isset($_SESSION['user'])) 
          {
            echo "<a class='headerbtn' href='https://web-plan-it.herokuapp.com/dc_mng' style='width: 87px;border-radius: 20px;right: 2%;top: 4px;/*! height: calc(100% - 1px); */font-size: 20px;'>
              Manage
            </a>";
          }
          else
          {
            $auth_url = url($client_id, $redirect_url, $scopes);
            echo "<a class='headerbtn' href='$auth_url' style='width: 87px;border-radius: 20px;right: 2%;top: 4px;/*! height: calc(100% - 1px); */font-size: 20px;'>
              Authorize
            </a>";
          }
        ?>
        <div style="top: -109px; right: 10%; /*! width: 100%; */" class="footerlinksdiv">
            <a class="headerlink" href=<?php echo $bot_invite_link; ?>>Main</a>
            <a class="headerlink" href=<?php echo $bot_invite_link; ?>>Commands &amp; Modules</a>
            <a class="headerlink" href=<?php echo $bot_invite_link; ?>>Updates &amp; Changelog</a>
        </div>
    </div>
      <div id="panel">
        <button onclick="topFunction()" id="panel_up_btn" title="Go to top">&#8613;</button> 
        <button onclick="moveFunction(document.getElementById('panel'))" id="panel_more_btn"><h4 id="rotated_text">More</h4></button> 
        <div id="panel_content"> 
          <a class="footerlink" href="https://discord.com/api/oauth2/authorize?client_id=875271995644842004&permissions=8&scope=bot%20applications.commands">Invite me!</a>
        </div>
      </div>
      <div id="top">
        <div style=" height:100%; width: 50%; right: 0px; -ms-transform: rotate(45deg); transform: rotate(45deg); background-color: black;"></div>
      </div>
      <div id="up">
        <div style="display: flex; flex-direction: row;left: auto;right: auto;padding: 50px 0px 50px 0px;">
          <div class="window" style="width: 33%;border-radius: 0px; border-style: none none solid none;">
            <h1 style="background-color: black; color: white;">ADMINISTRATE</h1></br>
            <h4>Bot comes with variety of tools to administrate your guild.</h4>
            <h4>It will shure help you speed up many processes and increase quality of your work.</h4>
          </div>
          <div class="window" style="width: 34%;border-radius: 0px; border-style: none none solid none;">
            <h1 style="background-color: black; color: white; border-left-style: none; border-right-style: none;">MANAGE</h1></br>
            <h4>It was obwious that configuring bot has to be intuitive and easy.</h4>
            <h4>You have many possibilities to set features and other stuff, from commands, to our bot's website.</h4>
          </div>
          <div class="window" style="width: 33%;border-radius: 0px; border-style: none none solid none;">
            <h1 style="background-color: black; color: white;">USE</h1></br>
            <h4>It wasn't designed only for work and administration.</h4>
            <h4>You can check many other features, like music and maybe games.</h4>
          </div>
        </div>
        <div>
        <h1>Wild West Post Office</h1></br>
        <h3>The only bot you ( probably ) will ever need</h3>
      </div>
      <div id="main">
        <div style="text-align: right;" id="main_up_left">
          <?php
           echo '<span style="font-size: 250px;font-weight: 600;"> ' . $dbm->get_dbmembers($pg_conn) . '</span>
                 </br>
                 <span style="font-size: 50px;font-weight: 500;"> Members</span>';
          ?>
        </div>
        <div style="border-left-style: none;" id="main_up_right">
          <?php
            echo '<span style="font-size: 250px;font-weight: 600;"> ' . $dbm->get_dbguilds($pg_conn) . '</span>
                  </br>
                  <span style="font-size: 50px;font-weight: 500;"> Guilds </br></span>';
          ?>
        </div>
      </div
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
