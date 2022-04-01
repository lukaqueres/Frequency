<?php

/* Home Page
* The home page of the working demo of oauth2 script.
* @author : MarkisDev
* @copyright : https://markis.dev
*/

# Enabling error display
error_reporting(E_ALL);
ini_set('display_errors', 1);


# Including all the required scripts for demo
require __DIR__ . "/includes/functions.php";
require __DIR__ . "/includes/discord.php";
require __DIR__ . "/config.php";

# ALL VALUES ARE STORED IN SESSION!
# RUN `echo var_export([$_SESSION]);` TO DISPLAY ALL THE VARIABLE NAMES AND VALUES.
# FEEL FREE TO JOIN MY SERVER FOR ANY QUERIES - https://join.markis.dev

?>

<html>

	<head>
		<title>Wild West Post Office | Manage</title>
		<link rel="stylesheet" href="assets/css/manage_styles.css">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<script type="text/javascript" src="assets/js/manage_scripts.js"></script>
		<style> .windowcontent { display: none; } </style>
	</head>

	<?php if (isset($_SESSION['user'])) { ?>
		<style type="text/css">
			#error-info{
				display:none;
			}
		</style>
	<?php } else { ?>
		<style type="text/css">
			#user-info{
				display:none;
			}
		</style>
	<?php } ?>

	<body>
		<div id="container"> 
			<div id="header_panel" class="vertical_center flex_container">
				<h1 class="no_margin" > <?php echo $bot_name; ?> </h1>
				<?php if (isset($_SESSION['user'])) { ?>
					<div class="dropdown">
						<input type="text" id="servers_search" onfocus="myFunction()" onkeyup="search_guilds(); myFunction()" placeholder= 
							<?php 
								if (!(isset($_GET['guild_id']))) { 
									echo '"Select server"'; 
								} else { 
									for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
										if ($_SESSION['guilds'][$i]['id'] == $_GET['guild_id']) {
											echo '"' . $_SESSION['guilds'][$i]['name'] . '"';
										}
									}
								}
							?> 
						title="Type in a name or id">
						<div id="myDropdown" class="dropdown-content vertical_center">
							<table style="border-collapse: collapse; border-spacing: 0; width: 100%;" id="servers">
								<?php
									for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
										//echo '<a href="?' . $_SESSION['guilds'][$i]['id'] .'">' . $_SESSION['guilds'][$i]['name'] . '</a>';
										echo '<tr class="search_row clicable_row" onclick="window.location.href=\'?guild_id=' . $_SESSION['guilds'][$i]['id'] .'\';" ><td style="padding: 5px;" >' . $_SESSION['guilds'][$i]['name'] . '</td>
								     	      <td class="no-display">' . $_SESSION['guilds'][$i]['id'] . '</td></tr>';
									}
								?>
								</table>
								<button id="slideUp" onclick="">Up</button>
								<button id="slideDown" onclick="">Down</button>
						</div>
					</div>
					<div class="full_height flex_container">
						<img id="avatar" src="https://cdn.discordapp.com/avatars/<?php $extention = is_animated($_SESSION['user_avatar']); echo $_SESSION['user_id'] . "/" . $_SESSION['user_avatar'] . $extention; ?>" />
						<span id="avatar_usename"><?php echo $_SESSION['username']?></span>
					</div>
				<?php } else 
					{
						$auth_url = url($client_id, $redirect_url, $scopes);
						echo "<a id='headerbtn' href='$auth_url'>
						Authorize
						</a>";
					}
				?>
			</div> <?php #END OF HEADER PANEL ?>
			<div class="grid_container center">
				<div class="header">
					header
				</div>
				<div class="left">
					left
				</div>
				<div class="main">
					main
				</div>
				<div class="footer">
					footer
				</div>
			</div>
		</div>
	</body>
	<script>
	add_overflow_btns()

		function load() {
			var windowIndex = 1;
			currentWindow(1);
			//showWindow(windowIndex);
		}
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.add("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('#servers_search')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
	</script>
</html>
