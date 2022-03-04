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
	<script type="text/javascript" src="assets/js/dc_mg_scripts.js"></script>
	<style>
		.windowcontent { display: none; }</style>
</head>
<?php	
if (isset($_SESSION['user'])) {
	?>
	<style type="text/css">
		#error-info{
			display:none;
		}
	</style>
	<?php
 }else {
	?>
	<style type="text/css">
		#user-info{
			display:none;
		}
	</style>
	<?php
}
?>
<body onload="load()">
	<div id="aside_menu">
		<?php	
		if (isset($_SESSION['user'])) {
		?>
		<div class="padding_box">
			<img id="avatar" src="https://cdn.discordapp.com/avatars/<?php $extention = is_animated($_SESSION['user_avatar']); 
				echo $_SESSION['user_id'] . "/" . $_SESSION['user_avatar'] . $extention; ?>" />
			<!--<h1 style="float: left; padding: 25;"><#?php echo $_SESSION['username']?></h1>-->
		<?php
 		}
		?>
		<!--<span class="menu">-->
			<?php
			$auth_url = url($client_id, $redirect_url, $scopes);
			if (isset($_SESSION['user'])) {
				echo '<a href="includes/logout.php"><img class="imagebtn" src="images/log-out-gear-white.png " onmouseover="this.src="log-out-gear-black.png";" onmouseout="this.src="log-out-gear-white.png";"></a>';
			} else {
				echo "<a href='$auth_url'><button class='log-in'>Login</button></a>";
			}
			?>
		<!--</span>-->
			</div>
		<a href="https://web-plan-it.herokuapp.com/"> <button class="log-in">Main</button></a>
	</div>
	<div id="main_content">
		<div class="window" id="error-info">
		<?php
		if (!isset($_SESSION['user'])) {
			echo '<h1 style="font-size:100px;">You are not logged in</h1></br>';
		}
		?>
		</div>
		<div class="window" id="user-info">
			<h1> User</h1>
		<div class="linkheader">
			<button class="clearlink windowContentBtn" onclick="currentWindow(1)">Overview</button>
			<button class="clearlink windowContentBtn" onclick="currentWindow(2)">Servers</button>
		</div>
			</br>
		<div class="windowcontent" id="useroverview">
		<?php
		if (isset($_SESSION['user'])) {
		?>
		<p> Name : <?php echo $_SESSION['username'] . '#' . $_SESSION['discrim']; ?></p>
		<p> ID : <?php echo $_SESSION['user_id']; ?></p>

			<p> Profile Picture : <img src="https://cdn.discordapp.com/avatars/<?php $extention = is_animated($_SESSION['user_avatar']);
			echo $_SESSION['user_id'] . "/" . $_SESSION['user_avatar'] . $extention; ?>" /></p>
		<h2>User Response :</h2>
		<div class="response-block">
			<p><?php echo json_encode($_SESSION['user']); ?></p>
			<?php
	echo json_encode($_SESSION['guilds_details']);
		
            // handle a successful response
            //success : function(data) {
            //},
    //});?>
		</div>
		</div>
		<?php
 		}else {
			echo '';
		?>
	<?php
}
?>
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
		<br>
		</div>
		<br>
		</div>
		<!--<h2> User Connections Response :</h2>-->
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
