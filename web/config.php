<?php
# CLIENT ID
# https://i.imgur.com/GHI2ts5.png (screenshot)
$client_id = "875271995644842004";

# CLIENT SECRET
# https://i.imgur.com/r5dYANR.png (screenshot)
$secret_id = "mPz7t6RNjmwerfLXN7LlB6-awue-6nUN";

# SCOPES SEPARATED BY SPACE
# example: identify email guilds connections  
$scopes = "identify guilds guilds.members.read";

# REDIRECT URL
# example: https://mydomain.com/includes/login.php
# example: https://mydomain.com/test/includes/login.php
$redirect_url = "https://web-plan-it.herokuapp.com/includes/login.php";

# IMPORTANT READ THIS:
# - Set the `$bot_token` to your bot token if you want to use guilds.join scope to add a member to your server
# - Check login.php for more detailed info on this.
# - Leave it as it is if you do not want to use 'guilds.join' scope.

# https://i.imgur.com/2tlOI4t.png (screenshot)
$bot_token = $_ENV["TOKEN"];

$bot_name = "Wild West Post Office";
$bot_invite_link = "https://discord.com/api/oauth2/authorize?client_id=875271995644842004&permissions=8&scope=bot%20applications.commands";