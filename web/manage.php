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
			<div id="header_panel" class="flex_container">
				<h1 class="no_margin" > <?php echo $bot_name; ?> </h1>
				<?php if (isset($_SESSION['user'])) { ?>
					<div class="dropdown">
						<input type="text" id="servers_search" onfocus="search_dropdownFunction()" onkeyup="search_guilds(); search_dropdownFunction()" placeholder= 
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
						<div id="search_dropdown" class="dropdown-content vertical_center">
							<table style="border-collapse: collapse; border-spacing: 0; width: 100%;" id="servers">
								<?php
									for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
										//echo '<a href="?' . $_SESSION['guilds'][$i]['id'] .'">' . $_SESSION['guilds'][$i]['name'] . '</a>';
										$extention = is_animated($_SESSION['guilds'][$i]['icon']);
										echo '<tr class="search_row clicable_row full_height flex_container" onclick="window.location.href=\'?guild_id=' . $_SESSION['guilds'][$i]['id'] .'\';" >
											<td class="flex_container" style="padding: 5px; margin-inline: 30px;" ><img class="icon no_margin" src="' . get_icon($_SESSION['guilds'][$i]) . '"/><h1 class="no_margin w_padding max_font">' . $_SESSION['guilds'][$i]['name'] . '</h1></td>
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
			<div id="main_grid" class="grid_container center">
				<div class="header">
					
				</div>
				<div class="left">
					<div class="div_box" style="min-width:250px;">
						<div class="no_margin flex_container" style="height: 75px;">
							<?php
								if (isset($_GET['guild_id']) and isset($_SESSION['user'])) {
									for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
										if ($_SESSION['guilds'][$i]['id'] == $_GET['guild_id']) {
											$extention = is_animated($_SESSION['guilds'][$i]['icon']);
											echo '<img class="icon no_margin" src="' . get_icon($_SESSION['guilds'][$i]) . '"/>';
											echo '<h2 class="no_margin w_padding" style="font-size: unset;">' . $_SESSION['guilds'][$i]['name'] . '</h2>';
											break;
										}
									}
								} elseif (isset($_SESSION['username'])) {
									echo '<h1 class="no_margin w_padding">' . $_SESSION['username'] . '</h1>';
								} else {
									echo '<h1 class="no_margin w_padding">Please log in</h1>';
								}
							?>
						</div>
						<?php
							if (isset($_GET['guild_id']) and isset($_SESSION['user'])) { ?>						
								<div class="tags_div">
									<?php
										for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
											if ($_SESSION['guilds'][$i]['id'] == $_GET['guild_id']) {
												$guild = $_SESSION['guilds'][$i];
												break;
											}
										}
										if (in_array("COMMUNITY", $guild['features'])) { ?>
											<div class="tag">
												<h5>Community</h5>
											</div>
										<?php };
										if (in_array("PARTNERED", $guild['features'])) { ?>
											<div class="tag">
												<h5>Partner</h5>
											</div>
										<?php };
										if (in_array("DISCOVERABLE", $guild['features'])) { ?>
											<div class="tag">
												<h5>Discoverable</h5>
											</div>
										<?php };
										if ($guild['owner']) { ?>
											<div class="tag">
												<h5>Owner</h5>
											</div>
										<?php };
										if (in_array("NEWS", $guild['features'])) { ?>
											<div class="tag">
												<h5>News</h5>
											</div>
										<?php };
										if (in_array("VERIFIED", $guild['features'])) { ?>
											<div class="tag">
												<h5>Verified</h5>
											</div>
										<?php };
										if ($guild['icon'] == null) { ?>
											<div class="tag">
												<h5>No icon</h5>
											</div>
										<?php };
									?>
							</div>	
						<?php }
					?>
					</div>
				</div>
				<div class="main">
					<?php
						if (isset($_GET['guild_id']) and isset($_SESSION['user'])) {
							for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
								if ($_SESSION['guilds'][$i]['id'] == $_GET['guild_id']) {
									echo json_encode($_SESSION['guilds'][$i]);
									echo '<br> TERAZ UPRAWNIENIA';
									$permissions = get_permissions($_SESSION['guilds'][$i]['permissions']);
									echo json_encode($permissions);
									echo '<br> TERAZ TAG';
									echo json_encode(get__user_permissions_tag($permissions));
									break;
								}
							}
						}
					?>
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
function search_dropdownFunction() {
  document.getElementById("search_dropdown").classList.add("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if ((!event.target.matches('#servers_search')) && ((!event.target.matches('#search_dropdown')))) {
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