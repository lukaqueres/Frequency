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
</head>

<body>
	<div id="header"> <span class="logo">Wild West Post Office</span>
		<span class="menu">
			<a class="log-in" href="https://web-plan-it.herokuapp.com/">Main</a>
			<?php
			$auth_url = url($client_id, $redirect_url, $scopes);
			if (isset($_SESSION['user'])) {
				echo '<a href="includes/logout.php"><button class="log-in">LOGOUT</button></a>';
			} else {
				echo "<a href='$auth_url'><button class='log-in'>LOGIN</button></a>";
			}
			?>
		</span>
	</div>
	<div id="aside_menu">
		Menu
	</div>
	<div id="main_content">
	<h1 style="text-align: center;">A Simple Working Demo of the Script </h2>
		<?php
		if (!isset($_SESSION['user'])) {
			echo "<h2 style='color:red; font-weight:900; text-align: center;'> LOGIN WITH THE LINK ABOVE TO SEE IT WORK! </h2><br/>";
			echo "<h4 style='color:red; font-weight:500; text-align: center;'> IGNORE THE ERRORS IF YOU HAVEN'T LOGGED IN! </h4>";
		}
		?>
		<h2> User Details :</h2>
		<p> Name : <?php echo $_SESSION['username'] . '#' . $_SESSION['discrim']; ?></p>
		<p> ID : <?php echo $_SESSION['user_id']; ?></p>
		<?php
		if (isset($_SESSION['email'])) {
			echo '<p> Email: ' . $_SESSION['email'] . '</p>';
		}
		?>

		<p> Profile Picture : <img src="https://cdn.discordapp.com/avatars/<?php $extention = is_animated($_SESSION['user_avatar']);
																			echo $_SESSION['user_id'] . "/" . $_SESSION['user_avatar'] . $extention; ?>" /></p>
		<br>
		<h2>User Response :</h2>
		<div class="response-block">
			<p><?php echo json_encode($_SESSION['user']); ?></p>
		</div>
		<br>
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
		<h2> User Connections :</h2>
		<table border="1">
			<tr>
				<th>NAME</th>
				<th>TYPE</th>
			</tr>
			<?php
			for ($i = 0; $i < sizeof($_SESSION['connections']); $i++) {
				echo "<tr><td>";
				echo $_SESSION['connections'][$i]['name'];
				echo "<td>";
				echo $_SESSION['connections'][$i]['type'];
				echo "</td>";
				echo "</tr></td>";
			}
			?>
		</table>
		<br>
		<h2> User Connections Response :</h2>
		<div class="response-block">
			<p> <?php echo json_encode($_SESSION['connections']); ?></p>
		</div>
	</div>
</body>

</html>
