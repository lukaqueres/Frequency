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
<body onload="changecontent('buttonservers', 'useroverview', 'buttonoverview');">
	<div id="aside_menu">
		<span class="logo">Wild West Post Office</span>
		<span class="menu">
			<a href="https://web-plan-it.herokuapp.com/"> <button class="log-in">Main</button></a>
			<?php
			$auth_url = url($client_id, $redirect_url, $scopes);
			if (isset($_SESSION['user'])) {
				echo '<a href="includes/logout.php"><button class="log-in">Logout</button></a>';
			} else {
				echo "<a href='$auth_url'><button class='log-in'>Login</button></a>";
			}
			?>
		</span>
	</div>
	<div id="main_content">
		<div class="window" id="error-info">
		<?php
		if (!isset($_SESSION['user'])) {
			echo 'You are not logged in</br>';
		}
		?>
		</div>
		<div class="window" id="user-info">
			</br>
		<div class="linkheader">
			<button class="clearlink" id="buttonoverview" onclick="changecontent('buttonoverview', 'userservers', 'buttonservers')">Overview</button>
			<button class="clearlink" id="buttonservers" onclick="changecontent('buttonservers', 'useroverview', 'buttonoverview')">Servers</button>
		</div>
			</br>
		<div class="windowcontent" id="useroverview">
		<h2> User Details :</h2>
		<p> Name : <?php echo $_SESSION['username'] . '#' . $_SESSION['discrim']; ?></p>
		<p> ID : <?php echo $_SESSION['user_id']; ?></p>

			<p> Profile Picture : <img src="https://cdn.discordapp.com/avatars/<?php $extention = is_animated($_SESSION['user_avatar']);
			echo $_SESSION['user_id'] . "/" . $_SESSION['user_avatar'] . $extention; ?>" /></p>
		</div>
			<br>
		<!--<h2>User Response :</h2>
		<div class="response-block">
			<p><#?php echo json_encode($_SESSION['user']); ?></p>
		</div>-->
		<br>
		<div class="windowcontent" id="userservers">
		<h2> User Guilds :</h2>
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
	function changecontent($button, $target, $targetbutton) {
		$button = document.getElementById($button)
		$target = document.getElementById($target)
		$targetbutton = document.getElementById($targetbutton)
		//changewindowcontent($target, $button, $targetbutton)
		$button.classList.remove("active");
   	 	$targetbutton.classList.add("active");
    		$target.classList.toggle("show");
	}
</script>
</html>
