<?php

namespace App\Helpers;

class Guild
{
    public $id;
    public $name;
    protected $icon;
    public $icon_url;
    public $owner;
    public $tags;
    public $has_bot;
    public $role;
    protected $permissions_num;
    protected $permissions; // protected
    public $num_users;
    public $num_members;
    public $features;

    // For DEBUGGING ->
    //public $permissions_names;
    // <-

    function __construct($id) {
        $this->id = $id;
    }

    function assign($discord, $DB) {
        $this->assign_discord($discord);
        $this->assign_DB($DB);
        $this->gen_iconurl();
        $this->gen_permissions();
        $this->gen_tags();
        $this->gen_role();
    }

    protected function assign_discord($guild) {
        $this->id = $guild->id;
        $this->name = $guild->name;
        $this->permissions_num = $guild->permissions;
        $this->owner = $guild->owner;
        $this->icon = $guild->icon;
        $this->features = $guild->features;
    }

    protected function assign_DB($guild) {
        if ($guild) {
            $this->has_bot = True;
            $this->num_members = $guild->number_of_members;
            $this->num_users = $guild->number_of_users;
        } else {
            $this->has_bot = False;
        }
    }

    protected function gen_iconurl() {
        $icon = $this->icon;
        $id = $this->id;

	    if ($icon == null) {
		    $url = "/images/blank-icon.png";
	    } else {
		    $extension = is_animated($icon);
		    $url = 'https://cdn.discordapp.com/icons/' . $id . '/' . $icon . $extension;
	    }
        $this->icon_url = $url;
    }

    protected function gen_permissions() {
        $usr_permissions = get_permissions($this->permissions_num);
        $this->permissions = $usr_permissions;
    }

    protected function gen_tags() {
        $tags = [];
	    if (in_array("COMMUNITY", $this->features)) {
            $tags[] = 'community'; };
	    if (in_array("PARTNERED", $this->features)) {
		    $tags[] = 'partnered'; };
	    if (in_array("DISCOVERABLE", $this->features)) {
		    $tags[] = 'discoverable'; };
	    if (in_array("NEWS", $this->features)) {
		    $tags[] = 'news'; };
	    if (in_array("VERIFIED", $this->features)) {
		    $tags[] = 'verified'; };
        if (in_array("ROLE_ICONS", $this->features)) {
            $tags[] = 'role_icons'; };
        if (in_array("AUTO_MODERATION", $this->features)) {
            $tags[] = 'auto_moderation'; };
	    if ($this->icon == null) {
		    $tags[] = 'no_icon';
        };
        
	    if ($this->owner) {
		    $tags[] = 'owner';
	    } elseif ($this->role == 'administrator') {
		    $tags[] = 'administrator';
	    } elseif ($this->role == 'moderator') {
		    $tags[] = 'moderator';
	    } elseif ($this->role == 'member') {
		    $tags[] = 'member';
	    };
        $this->tags = $tags;
    }

    protected function gen_role() {
    $usr_permissions_list = $this->permissions;
        // /administrator/ permissions provide administrator tag, while /moderator/ will tag as moderator, ( all these permissions require 2FA )
        // Please add permissions from top ( from highest )
        if ($this->owner) {
            $role = 'owner';
            $this->role = $role;
            return;
        }
        $tag = 'member';
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
        foreach($gen_permissions_tags as $permission => $role) {
            if (in_array($permission, $usr_permissions_list)) {
                $tag = $role;
                break;
            };
        }
        $this->role = $tag;
    }
}
