<?php
    if (isset($id)) {
        echo '<b>Passed: ' . $id . ' </b>';
    } else {
        echo 'Pusta zmienna';
    }
    if (isset($view)) {
        echo '<b>Passed: ' . $view . ' </b>';
    } else {
        echo 'Pusta zmienna';
    }
    if (isset($id) and ($id == 0)) {
        return redirect()->route('manage');
    }
?>
User

Yay
