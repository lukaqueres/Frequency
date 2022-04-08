<?php
    if (isset($id)) {
        echo '<b>Passed: ' . $id . ' </b>';
    } else {
        echo 'Pusta zmienna';
    }
    if (isset($id) and($id == 0)) {
        return redirect()->route('manage');
    }
?>
Manage 

Yay
{{ Session::get('name')}}
{{ Session::get('username')}}
