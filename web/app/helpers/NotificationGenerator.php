<?php

namespace App\Helpers;

class Notification
{
    public $code;
    protected $title;
    protected $icon;
    protected $content;
    protected $link;
    protected $linkTitle;
    public $node;


    function __construct($title, $content) {
        $this->title = $title;
        $this->content = $content;
    }

    function addUrl($linkTitle, $link) {
        $this->link = $link;
        $this->linkTitle = $linkTitle;
    }

    function generate() {
        $notifiClasses = 'notification';
        $node = '<div class="' . $notifiClasses . '">
                    <p>' . $this->title . '</p>
                    <h5>' . $this->content . '</h5>';
        if ($this->link) {
            $node .= '<a href="' . $this->link . '">' . $this->linkTitle; . '</a>';
        }
        $node .= '<button class="close" onclick="closeParent(event)">Close notification</button></div>';
        $this->node = $node;
    }

}
