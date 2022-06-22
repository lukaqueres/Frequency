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


    function __construct($title, $content, $link = Null, $linkTitle = Null) {
        $this->title = $title;
        $this->content = $content;
        $this->link = $link;
        $this->linkTitle = $linkTitle;
    }

    function generate() {
        $notifiClasses = 'notification';
        $node = '<div class="' . $notifiClasses . '">
                    <p>' . $this->title . '</p>
                    <h4>' . $this->content . '</h4>';
        if ($this->link) {
            $node .= '<a href="' . $this->link . '">' . $this->linkTitle; . '</a>';
        }
        $node .= '<button class="close-btn">Close notification</button></div>';
        $this->node = $node;
    }

}
