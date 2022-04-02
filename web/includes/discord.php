<?php
/* Discord Oauth v.4.1
 * This file contains the core functions of the oauth2 script.
 * @author : MarkisDev
 * @copyright : https://markis.dev
 */

# Starting session so we can store all the variables
session_start();

# Setting the base url for API requests
$GLOBALS['base_url'] = "https://discord.com";

# Setting bot token for related requests
$GLOBALS['bot_token'] = null;

# A function to generate a random string to be used as state | (protection against CSRF)
function gen_state()
{
    $_SESSION['state'] = bin2hex(openssl_random_pseudo_bytes(12));
    return $_SESSION['state'];
}

# A function to generate oAuth2 URL for logging in
function url($clientid, $redirect, $scope)
{
    $state = gen_state();
    return 'https://discordapp.com/oauth2/authorize?response_type=code&client_id=' . $clientid . '&redirect_uri=' . $redirect . '&scope=' . $scope . "&state=" . $state;
}

# A function to initialize and store access token in SESSION to be used for other requests
function init($redirect_url, $client_id, $client_secret, $bot_token = null)
{
    if ($bot_token != null)
        $GLOBALS['bot_token'] = $bot_token;
    $code = $_GET['code'];
    $state = $_GET['state'];
    # Check if $state == $_SESSION['state'] to verify if the login is legit | CHECK THE FUNCTION get_state($state) FOR MORE INFORMATION.
    $url = $GLOBALS['base_url'] . "/api/oauth2/token";
    $data = array(
        "client_id" => $client_id,
        "client_secret" => $client_secret,
        "grant_type" => "authorization_code",
        "code" => $code,
        "redirect_uri" => $redirect_url
    );
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($curl);
    curl_close($curl);
    $results = json_decode($response, true);
    $_SESSION['access_token'] = $results['access_token'];
}

# A function to get user information | (identify scope)
function get_user($email = null)
{
    $url = $GLOBALS['base_url'] . "/api/users/@me";
    $headers = array('Content-Type: application/x-www-form-urlencoded', 'Authorization: Bearer ' . $_SESSION['access_token']);
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
    $response = curl_exec($curl);
    curl_close($curl);
    $results = json_decode($response, true);
    $_SESSION['user'] = $results;
    $_SESSION['username'] = $results['username'];
    $_SESSION['discrim'] = $results['discriminator'];
    $_SESSION['user_id'] = $results['id'];
    $_SESSION['user_avatar'] = $results['avatar'];
    # Fetching email 
    if ($email == True) {
        $_SESSION['email'] = $results['email'];
    }
}

# A function to get user guilds | (guilds scope)
function get_guilds()
{
    $url = $GLOBALS['base_url'] . "/api/users/@me/guilds";
    $headers = array('Content-Type: application/x-www-form-urlencoded', 'Authorization: Bearer ' . $_SESSION['access_token']);
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
    $response = curl_exec($curl);
    curl_close($curl);
    $results = json_decode($response, true);
    return $results;
}

function get_guild_details($id)
{
    $url = $GLOBALS['base_url'] . "/api/users/@me/guilds/$id/member";
    $headers = array('Content-Type: application/x-www-form-urlencoded', 'Authorization: Bearer ' . $_SESSION['access_token']);
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
    $response = curl_exec($curl);
    curl_close($curl);
    $results = json_decode($response, true);
    return $results;
}

# A function to fetch information on a single guild | (requires bot token)
function get_guild($id)
{
    $url = $GLOBALS['base_url'] . "/api/guilds/$id";
    $headers = array('Content-Type: application/x-www-form-urlencoded', 'Authorization: Bot ' . $GLOBALS['bot_token']);
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
    $response = curl_exec($curl);
    curl_close($curl);
    $results = json_decode($response, true);
    return $results;
}

# A function to get user connections | (connections scope)
function get_connections()
{
    $url = $GLOBALS['base_url'] . "/api/users/@me/connections";
    $headers = array ('Content-Type: application/x-www-form-urlencoded', 'Authorization: Bearer ' . $_SESSION['access_token']);
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
    $response = curl_exec($curl);
    curl_close($curl);
    $results = json_decode($response, true);
    return $results;
}

# Function to make user join a guild | (guilds.join scope)
# Note : The bot has to be a member of the server with CREATE_INSTANT_INVITE permission.
#        The bot DOES NOT have to be online, just has to be a bot application and has to be a member of the server.
#        This is the basic function with no parameters, you can build on this to give the user a nickname, mute, deafen or assign a role.      
function join_guild($guildid)
{
    $data = json_encode(array("access_token" => $_SESSION['access_token']));
    $url = $GLOBALS['base_url'] . "/api/guilds/$guildid/members/" . $_SESSION['user_id'];
    $headers = array('Content-Type: application/json', 'Authorization: Bot ' . $GLOBALS['bot_token']);
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "PUT");
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
    $response = curl_exec($curl);
    curl_close($curl);
    $results = json_decode($response, true);
    return $results;
}

# A function to verify if login is legit
function check_state($state)
{
    if ($state == $_SESSION['state']) {
        return true;
    } else {
        # The login is not valid, so you should probably redirect them back to home page
        return false;
    }
}

function get_permissions($usr_permissions_dec) {
    $gen_permissions_codes = [
        // Codes are updated to date /02.04.2022/, please change date if there were updated changes to codes and/or permissions  
        // General x15
        'generalAdministrator' => 0x000000000000008,
        'generalViewAuditLog' => 0x000000000000080,
        'generalManageServer' => 0x000000000000020,
        'generalManageRoles' => 0x000000010000000,
        'generalManageChannels' => 0x000000000000010,
        'generalKickMembers' => 0x000000000000002,
        'generalBanMembers' => 0x000000000000004,
        'generalCreateInstantInvite' => 0x000000000000001,
        'generalChangeNickname' => 0x00000004000000,
        'generalManageNicknames' => 0x00000008000000,
        'generalManageEmoisAndStickers' => 0x000000040000000,
        'generalManageWebhooks' => 0x000000020000000,
        'generalReadMessagesViewChannels' => 0x000000000000400,
        'generalManageEvents' => 0x0000000200000000,
        'generalModerateMembers' => 0x000000010000000000,
        // Text x15
        'textSendMessages' => 0x000000000000800,
        'textCreatePublicThreads' => 0x0000000800000000,
        'textCreatePrivateThreads' => 0x00000001000000000,
        'textSendMessagesInThreads' => 0x00000004000000000,
        'textSendTTSMessages' => 0x000000000001000,
        'textManageMessages' => 0x000000002000,
        'textManageThreads' => 0x00000000400000000,
        'textEmbedLinks' => 0x0000000000004000,
        'textAttachFiles' => 0x0000000000008000,
        'textReadMessageHistory' => 0x000000000010000,
        'textMentionEveryone' => 0x000000000020000,
        'textUseExternalEmojis' => 0x000000000040000,
        'textUseExternalStickers' => 0x000000002000000000,
        'textAddReactions' => 0x000000000000040,
        'textUseSlashCommands' => 0x0000000080000000,
        // Voice x7
        'voiceConnect' => 0x00000000100000,
        'voiceSpeak' => 0x00000000200000,
        'voiceMuteMembers' => 0x00000000400000,
        'voiceDeafenMembers' => 0x00000000800000,
        'voiceMoveMembers' => 0x000000001000000,
        'voiceUseVActivity' => 0x000000002000000,
        'voicePrioritySpeaker' => 0x000000000000100
    ];
    $usr_permissions_binary = decbin($usr_permissions_dec);
    $usr_permissions = array();
    foreach($gen_permissions_codes as $key => $value) {
        $gen_binary_permission = hex2bin($value);
        $has_permission = ($usr_permissions_binary & $gen_binary_permission) != 0;
        if ($has_permission) {
            $usr_permissions[] = $key;
        };
    };
    return $usr_permissions;
}
?>