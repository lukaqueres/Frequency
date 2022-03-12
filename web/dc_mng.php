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
		<link rel="stylesheet" href="assets/css/dc_mg_styles.css">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<script type="text/javascript" src="assets/js/dc_mg_scripts.js"></script>
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
			<div id="aside_menu">
				<div class="side_menu_accountdet">
					<?php if (isset($_SESSION['user_avatar'])) { ?>
						<img id="avatar" src="https://cdn.discordapp.com/avatars/<?php $extention = is_animated($_SESSION['user_avatar']); echo $_SESSION['user_id'] . "/" . $_SESSION['user_avatar'] . $extention; ?>" />
						<span id="avatar_usename"><?php echo $_SESSION['username']?></span>
					<?php } ?>
				</div>
				<div>
					<?php
						$auth_url = url($client_id, $redirect_url, $scopes);
						if (!(isset($_SESSION['user']))) {
							echo "<a href='$auth_url'><button>Authorize</button></a>";
						} else {
							echo '<a href="includes/logout.php"><button>Log-out</button></a>';
						}
					?>
					<a href="?window=user"><button>User</button></a>
					<a href="?window=guilds"><button>Guilds</button></a>
				</div>
				<input type="text" id="servers_search" onkeyup="search_guilds()" placeholder="Filter by id or name.." title="Type in a name or id" style="width: 90%; margin-block: 10px;">
				<div style="max-height: 50%; overflow:auto;">
					<table style="border-collapse: collapse; border-spacing: 0;" id="servers">
						<?php 
							for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
								echo '<tr class="search_row clicable_row" onclick="window.location.href=\'?window=guilds&' . $_SESSION['guilds'][$i]['id'] .'\';" ><td style="padding: 5px;" >' . $_SESSION['guilds'][$i]['name'] . '</td>
								     <td class="no-display">' . $_SESSION['guilds'][$i]['id'] . '</td></tr>';
								/*echo ;
								echo "<td>";
								echo $_SESSION['guilds'][$i]['id'];
								echo "</td>";
								echo "</tr></td>";
								<li><a href="#">Adele</a></li>*/
							}
						?>
					</table>
				</div>
			</div>
			<div id="main_content">
				<?php if (!(isset($_GET['window']))) { redirect("../dc_mng.php?window=main"); } #Redirect if no window specified  ?>
				<?php if (!isset($_SESSION['user'])) { #WINDOW CONTENT ----------------------------------------------------------- ERROR ON NOT LOGIN ?>
					<div class="window" id="error-info">
						<?php if (!isset($_SESSION['user'])) { echo '<h1 style="font-size:100px;">You are not logged in</h1></br>'; } ?>
					</div>
				<?php } elseif ($_GET['window'] == 'main') { #WINDOW CONTENT ----------------------------------------------------------- MAIN ?> 
					<div class="window" id="main">
						<div class="small_window">
							User:
						</div>
						<div class="small_window">
							Guilds:
						</div>
						<div class="small_window">
							Anty-spam:
						</div>
					</div>
				<?php } elseif ($_GET['window'] == 'guilds') { #WINDOW CONTENT ----------------------------------------------------------- GUILDS ?>
					<div class="window" id="guilds">Guilds
					</div>
				<?php } elseif ($_GET['window'] == 'user') { #WINDOW CONTENT ----------------------------------------------------------- USER ?>
					<div class="window" id="user-info">
						<h1> User</h1>
						<div class="linkheader">
							<button class="clearlink windowContentBtn" onclick="currentWindow(1)">Overview</button>
							<button class="clearlink windowContentBtn" onclick="currentWindow(2)">Servers</button>
						</div>
						</br>
						<div class="windowcontent" id="useroverview">
							<?php if (isset($_SESSION['user'])) { ?>
								<p> Name : <?php echo $_SESSION['username'] . '#' . $_SESSION['discrim']; ?></p>
								<p> ID : <?php echo $_SESSION['user_id']; ?></p>

								<p> Profile Picture : <img src="https://cdn.discordapp.com/avatars/<?php $extention = is_animated($_SESSION['user_avatar']);
									echo $_SESSION['user_id'] . "/" . $_SESSION['user_avatar'] . $extention; ?>" />
								</p>
								<h2>User Response :</h2>
								<div class="response-block">
									<p><?php echo json_encode($_SESSION['user']); ?></p> 
									<?php
										echo json_encode($_SESSION['guilds_details']);
		
										// handle a successful response
										//success : function(data) {
										//}
										//});
									?>
								</div>
							<?php } ?>
						</div>
						<?php #}else { echo ''; ?>
						<div class="windowcontent" id="userservers">
							<h2>Guilds :</h2>
							<table border="1">
								<tr>
									<th>NAME</th>
									<th>ID</th>
								</tr>
									<?php
										for ($i = 0; $i < sizeof($_SESSION['guilds']); $i++) {
											echo "<tr><td>";
											echo $_SESSION['guilds'][$i]['name'];
											echo "<td>";
											echo $_SESSION['guilds'][$i]['id'];
											echo "</td>";
											echo "</tr></td>";
										}
									?>
							</table>
							<br>
							<h2> User Guilds Response :</h2>
							<div class="response-block">
								<p> <?php echo json_encode($_SESSION['guilds']); ?></p>
							</div>
						</div>
					</div>
					<script type="text/javascript"> load(); </script>
				<?php } else { redirect("../dc_mng.php?window=main"); } #END OF WINDOW's IF STATEMENT ?>
			</div>
		</div>
	</body>
	<script>
		function load() {
			var windowIndex = 1;
			currentWindow(1);
			//showWindow(windowIndex);
		}
	</script>
</html>
