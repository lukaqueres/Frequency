<?php

class Guild
{
    public $id;
    public $name;
    protected $icon;
    public $icon_url;
    public $is_owner;
    public $tags;
    public $is_bot;
    public $role;
    protected $permissions_num;
    protected $permissions;
    public $num_users;
    public $num_members;
    public $features;


    function __construct($id) {
        $this->id = $id;
    }

    function assign_discord($guild) {
        $this->id = $guild->id;
        $this->name = $guild->name;
        $this->permissions_num = $guild->permissions;
        $this->is_owner = $guild->owner;
        $this->icon = $guild->icon;
        $this->features = $guild->features;
    }

    protected function assign_DB($guild) {
        $this->is_bot = True;
        $this->num_members = $guild->number_of_members;
        $this->num_users = $guild->number_of_users;
    }

    public function gen_iconurl() {
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

    public function gen_permissions() {
        $usr_permissions = get_permissions($this->permissions_num);
        $this->permissions = $usr_permissions;
    }

    public function gen_tags() {
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
        
	    if ($this->is_owner) {
		    $tags[] = 'owner';
	    } elseif ($this->role == 'administrator') {
		    $tags[] = 'administrator';
	    } elseif ($this->role == 'moderator') {
		    $tags[] = 'moderator';
	    } elseif ($this->role == 'member') {
		    $tags[] = 'member';
	    };
        $this->tag = $tags;
    }
}
