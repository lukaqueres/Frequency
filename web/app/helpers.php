<?php

if (! function_exists('get__user_permissions_tag')) {
    function get__user_permissions_tag($usr_permissions_list) {
        // /administrator/ permissions provide administrator tag, while /moderator/ will tag as moderator, ( all these permissions require 2FA )
        // Please add permissions from top ( from highest )
        $gen_permissions_tags = [
            'generalAdministrator' => 'administrator',
            'generalKickMembers' => 'moderator',
            'generalBanMembers' => 'moderator',
            'generalManageChannels' => 'moderator',
            'generalManageServer' => 'moderator',
            'textManageMessages' => 'moderator',
            'generalManageRoles' => 'moderator',
            'generalManageWebhooks' => 'moderator',
            'generalManageEmoisAndStickers' => 'moderator',
            'textManageThreads' => 'moderator',
            'generalModerateMembers' => 'moderator'
        ];
        foreach($gen_permissions_tags as $permission => $tag) {
            if (in_array($permission, $usr_permissions_list)) {
                return $tag;
            };
        }
        return 'member';
    }
}

if (! function_exists('get_permissions')) {
    function get_permissions($usr_permissions_dec) {
        $gen_permissions_codes = [
            // Codes are updated to date /02.04.2022/, please change date if there were updated changes to codes and/or permissions  
            //https://discord.com/developers/docs/topics/permissions <- permissions tab in discord docks
            // General x15
            'generalAdministrator' => 0x000008,
            'generalViewAuditLog' => 0x0080,
            'generalManageServer' => 0x0020,
            'generalManageRoles' => 0x10000000,
            'generalManageChannels' => 0x0010,
            'generalKickMembers' => 0x0002,
            'generalBanMembers' => 0x0004,
            'generalCreateInstantInvite' => 0x0001,
            'generalChangeNickname' => 0x4000000,
            'generalManageNicknames' => 0x8000000,
            'generalManageEmoisAndStickers' => 0x40000000,
            'generalManageWebhooks' => 0x20000000,
            'generalReadMessagesViewChannels' => 0x0400,
            'generalManageEvents' => 0x200000000,
            'generalModerateMembers' => 0x10000000000,
            // Text x15
            'textSendMessages' => 0x0800,
            'textCreatePublicThreads' => 0x800000000,
            'textCreatePrivateThreads' => 0x1000000000,
            'textSendMessagesInThreads' => 0x4000000000,
            'textSendTTSMessages' => 0x1000,
            'textManageMessages' => 0x2000,
            'textManageThreads' => 0x400000000,
            'textEmbedLinks' => 0x4000,
            'textAttachFiles' => 0x8000,
            'textReadMessageHistory' => 0x10000,
            'textMentionEveryone' => 0x20000,
            'textUseExternalEmojis' => 0x40000,
            'textUseExternalStickers' => 0x2000000000,
            'textAddReactions' => 0x040,
            'textUseSlashCommands' => 0x80000000,
            // Voice x7
            'voiceConnect' => 0x100000,
            'voiceSpeak' => 0x200000,
            'voiceMuteMembers' => 0x400000,
            'voiceDeafenMembers' => 0x800000,
            'voiceMoveMembers' => 0x1000000,
            'voiceUseVActivity' => 0x2000000,
            'voicePrioritySpeaker' => 0x100,
        ];
        //$usr_permissions_binary = decbin($usr_permissions_dec);
        $usr_permissions = array();
        foreach($gen_permissions_codes as $key => $value) {
            //$current_permission = base_convert($value, 16, 10);
            //$current_permission = (int)$current_permission;
            $has_permission = ($usr_permissions_dec & $value) != 0;
            //echo '$key: ' . gettype($key) . '( ' . $key  . ' ) $value: ' . gettype($value) . '( ' . $value . ' ) $usr_permissions_dec: ' . gettype($usr_permissions_dec) . '( ' . $usr_permissions_dec . ' ) $has_permission: ' . gettype($has_permission) . '( ' . $has_permission . ' ) </br>';
            if ($has_permission) {
                $usr_permissions[] = $key;
            };
        };
        return $usr_permissions;
    
    }
}

if (! function_exists('get_guild_tags')) {
    function get_guild_tags($guild) {
        $tags_div = '<div class="tags_div">';
        $guild_data = $guild['data'];
	    if (in_array("COMMUNITY", $guild_data['features'])) {
            $tags_div .= '<div class="tag"><h5>Community</h5></div>'; };
	    if (in_array("PARTNERED", $guild_data['features'])) {
		    $tags_div .= '<div class="tag"><h5>Partner</h5></div>'; };
	    if (in_array("DISCOVERABLE", $guild_data['features'])) {
		    $tags_div .= '<div class="tag"><h5>Discoverable</h5></div>'; };
	    if (in_array("NEWS", $guild_data['features'])) {
		    $tags_div .= '<div class="tag"><h5>News</h5></div>'; };
	    if (in_array("VERIFIED", $guild_data['features'])) {
		    $tags_div .= '<div class="tag"><h5>Verified</h5></div>'; };
	    if ($guild_data['icon'] == null) {
		    $tags_div .= '<div class="tag"><h5>No icon</h5></div>'; };
	    if ($guild_data['owner']) {
		    $tags_div .= '<div class="tag"><h5>Owner</h5></div>';
	    } elseif ($guild['p_tag'] == 'administrator') {
		    $tags_div .= '<div class="tag"><h5>Administrator</h5></div>';
	    } elseif ($guild['p_tag'] == 'moderator') {
		    $tags_div .= '<div class="tag"><h5>Moderator</h5></div>';
	    } elseif ($guild['p_tag'] == 'member') {
		    $tags_div .= '<div class="tag"><h5>Member</h5></div>';
	    };
        $tags_div .='</div>';
        return $tags_div;
    }
}

# Check user's avatar type
function is_animated($avatar)
{
	if ($avatar == null) {
		return ".png";
	}
	$ext = substr($avatar, 0, 2);
	if ($ext == "a_")
	{
		return ".gif";
	}
	else
	{
		return ".png";
	}
}

function get_icon($guild)
{
	if ($guild['icon'] == null) {
		return "images/blank-icon.png";
	} else {
		$extension = is_animated($guild['icon']);
		$icon_url = 'https://cdn.discordapp.com/icons/' . $guild['id'] . '/' . $guild['icon'] . $extension;
		return $icon_url;
	}
}

#declare variables
$secret_id = "mPz7t6RNjmwerfLXN7LlB6-awue-6nUN";
$scopes = "identify guilds guilds.members.read";
$redirect_url = "https://web-plan-it.herokuapp.com/includes/login.php";
$bot_token = $_ENV["TOKEN"];
$bot_name = "Wild West Post Office";
$bot_invite_link = "https://discord.com/api/oauth2/authorize?client_id=875271995644842004&permissions=8&scope=bot%20applications.commands";
