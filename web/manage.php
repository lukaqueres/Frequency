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
	<?php
		if (isset($_GET['guild_id']) and isset($_SESSION['user'])) {
			for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
				if ($_SESSION['guilds'][$i]['id'] == $_GET['guild_id']) {
					$this_guild['data'] = $_SESSION['guilds'][$i];
					break;
				}
			}
			$this_guild['permissions'] = get_permissions($this_guild['data']['permissions']);
			$this_guild['p_tag'] = get__user_permissions_tag($this_guild['permissions']);
			$this_guild['name'] = $this_guild['data']['name'];
		};
	?>
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
			<div id="header_panel" class="flex_container">
				<h1 class="no_margin" > <?php echo $bot_name; ?> </h1>
				<?php if (isset($_SESSION['user'])) { ?>
					<div class="dropdown">
						<input type="text" id="servers_search" onfocus="search_dropdownFunction()" onkeyup="search_guilds(); search_dropdownFunction()" placeholder= 
							<?php 
								if (!(isset($_GET['guild_id']))) { 
									echo '"Select server"'; 
								} else { 
									echo '"' . $this_guild['name'] . '"';
								}
							?> 
						title="Type in a name or id">
						<div id="search_dropdown" class="dropdown-content vertical_center">
							<table style="border-collapse: collapse; border-spacing: 0; width: 100%;" id="servers">
								<?php
									for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
										//echo '<a href="?' . $_SESSION['guilds'][$i]['id'] .'">' . $_SESSION['guilds'][$i]['name'] . '</a>';
										$extention = is_animated($_SESSION['guilds'][$i]['icon']);
										echo '<tr id="search_dropdown_' . $_SESSION['guilds'][$i]['id'] .'_" class="search_row clicable_row full_height flex_container" onclick="window.location.href=\'?guild_id=' . $_SESSION['guilds'][$i]['id'] .'\';" >
											<td class="flex_container" style="padding: 5px; margin-inline: 30px;" >
												<img class="icon no_margin" src="' . get_icon($_SESSION['guilds'][$i]) . '"/>
												<h1 class="no_margin w_padding max_font">' . $_SESSION['guilds'][$i]['name'] . '</h1>
											</td>
								     		<td class="no-display">' . $_SESSION['guilds'][$i]['id'] . '</td></tr>';
									}
								?>
								</table>
								<button id="slideUp" onclick="">Up</button>
								<button id="slideDown" onclick="">Down</button>
						</div>
					</div>
					<div class="dropdown full_height">
						<div class="full_height flex_container clicable_div" onclick='user_dropdownFunction()'>
							<img id="avatar" src="https://cdn.discordapp.com/avatars/<?php $extention = is_animated($_SESSION['user_avatar']); echo $_SESSION['user_id'] . "/" . $_SESSION['user_avatar'] . $extention; ?>" />
							<span id="avatar_usename"><?php echo $_SESSION['username']?></span>
						</div>
						<div id="user_dropdown" >
							test
						</div>
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
			<div id="main_grid" class="grid_container center">
				<div class="header">
					<div class="div_box" style="min-width:250px;">
						<div class="no_margin flex_container" style="height: 75px;">
							<?php
								if (isset($_GET['guild_id']) and isset($_SESSION['user'])) {
									echo '<img class="icon no_margin" src="' . get_icon($this_guild['data']) . '"/>';
									echo '<h2 class="no_margin w_padding" style="font-size: unset;">' . $this_guild['name'] . '</h2>';
								} elseif (isset($_SESSION['username'])) {
									echo '<h1 class="no_margin w_padding">' . $_SESSION['username'] . '</h1>';
								} else {
									echo '<h1 class="no_margin w_padding">Please log in</h1>';
								}
							?>
						</div>
						<?php
							if (isset($_GET['guild_id']) and isset($_SESSION['user'])) {				
								echo get_guild_tags($this_guild['data']);
							}
						?>
					</div>
				</div>
				<div class="main">
					<?php
						if (isset($_GET['guild_id']) and isset($_SESSION['user'])) {
							echo json_encode($this_guild['data']);
							echo json_encode($this_guild['permissions']);
						}
					?>
				</div>
				<div class="footer">
					footer
				</div>		
				</div>
				<div class="left">

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
function search_dropdownFunction() {
	document.getElementById("search_dropdown").classList.add("show");
	<?php
	if (isset($_GET['guild_id']) and isset($_SESSION['user'])) { ?>
		var IdOfElement = document.getElementById( <?php echo '"search_dropdown_' . $_GET['guild_id'] . '_"'; ?>);
		var topPos = IdOfElement.offsetTop;
		document.getElementById('search_dropdown').scrollTop = topPos;
	<?php }; ?>
}

function user_dropdownFunction() {
	document.getElementById("user_dropdown").classList.add("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
	if (!event.target.matches('#user_dropdown') && document.getElementById("user_dropdown").classList.contains('show')) {
		var dropdown = document.getElementById("user_dropdown");
		if (dropdown.classList.contains('show')) {
			dropdown.classList.remove('show');
		}
	}
	if ((!event.target.matches('#servers_search')) && ((!event.target.matches('#search_dropdown'))) && document.getElementById("search_dropdown").classList.contains('show')) {
		var dropdown = document.getElementById("search_dropdown");
		if (dropdown.classList.contains('show')) {
			dropdown.classList.remove('show');
		}
	}
}
function addListiners() {
	var div = document.getElementById("user_dropdown");

	div.addEventListener('click', function (event) { document.getElementById("user_dropdown").classList.add("show"); });
 }

 addListiners()
	</script>
</html>