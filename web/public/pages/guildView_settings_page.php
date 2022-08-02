<?php
        $user = Session::get('user');
        $guilds = Session::get('guilds');
        $guild = $guilds[$id];
        $view = $view;
    ?>

<div class="card-container">
                        <div class="card huge-title full transparent">
                            <div class="flex">
                                <p class="x-title">Settings</p>
                            </div>
                        </div>
                    </div>