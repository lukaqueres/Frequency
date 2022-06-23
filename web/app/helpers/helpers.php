<?php

function get_user_permissions_tag($usr_permissions_list)
{
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

function get_permissions($usr_permissions_dec): array
{
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

function get_guild_tags($guild) {
    $tags = [];
    $guild_data = $guild;
	if (in_array("COMMUNITY", $guild_data->features)) {
        $tags[] = 'community'; };
	if (in_array("PARTNERED", $guild_data->features)) {
		$tags[] = 'partnered'; };
	if (in_array("DISCOVERABLE", $guild_data->features)) {
		$tags[] = 'discoverable'; };
	if (in_array("NEWS", $guild_data->features)) {
		$tags[] = 'news'; };
	if (in_array("VERIFIED", $guild_data->features)) {
		$tags[] = 'verified'; };
    if (in_array("ROLE_ICONS", $guild_data->features)) {
        $tags[] = 'role_icons'; };
    if (in_array("AUTO_MODERATION", $guild_data->features)) {
        $tags[] = 'auto_moderation'; };
	if ($guild_data->icon == null) {
		$tags[] = 'no_icon'; };
	if ($guild_data->owner) {
		$tags[] = 'owner';
	} elseif ($guild->p_tag == 'administrator') {
		$tags[] = 'administrator';
	} elseif ($guild->p_tag == 'moderator') {
		$tags[] = 'moderator';
	} elseif ($guild->p_tag == 'member') {
		$tags[] = 'member';
	};
    return $tags;
}

# Check user's avatar type
function is_animated($img)
{
	if ($img == null) {
		return ".png";
	}
	$ext = substr($img, 0, 2);
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
    if(is_object($guild)) {
        $icon = $guild->icon;
        $id = $guild->id;
    }
    else {
        $icon = $guild['icon'];
        $id = $guild['id'];
    }

	if ($icon == null) {
		return "/images/blank-icon.png";
	} else {
		$extension = is_animated($icon);
		$icon_url = 'https://cdn.discordapp.com/icons/' . $id . '/' . $icon . $extension;
		return $icon_url;
	}
}

function get_avatar($user)
{
    if(is_object($user)) {
        $avatar = $user->avatar;
        $id = $user->id;
    }
    else {
        $avatar = $user['avatar'];
        $id = $user['icon'];
    }

	if ($avatar == null) {
		return "/images/blank-icon.png";
	} else {
		$extension = is_animated($avatar);
		$icon_url = 'https://cdn.discordapp.com/avatars/' . $id . '/' . $avatar . $extension;
		return $icon_url;
	}
}

function gen_authorization_link($state = Null) {
    $params = [
        'client_id' => '875271995644842004',
        'redirect_uri' => 'https://web-plan-it.herokuapp.com/discord/authorize',
        'scope' => 'identify guilds guilds.members.read email',
        'state' => $state,
        'response_type' => 'code'
    ];

    $url = 'https://discord.com/api/oauth2/authorize?';
    // array_filter will remove any empty value
    $url .= http_build_query($params);

    return $url;
}
