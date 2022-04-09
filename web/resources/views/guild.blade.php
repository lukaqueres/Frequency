<?php

    if (isset($id)) {
        echo '<b>Passed: ' . $id . ' </b>';
        //echo get_guild_tags(['guild','user']);
    } else {
        echo 'no $id';
    }
    if (isset($view)) {
        echo '<b>Passed: ' . $view . ' </b>';
    } else {
        echo 'Pusta zmienna';
    }
    if (isset($id) and($id == 0)) {
        return redirect()->route('manage');
    }
?>
Guild {{ Session::get('name')}}{{ Session::get('username')}}

Yay
