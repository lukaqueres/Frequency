<?php
        $user = Session::get('user');
        $guilds = Session::get('guilds');
        $guild = $guilds[$id];
        $view = $view;
    ?>

<div class="card-container">
    <button onclick="setPreferredColorScheme()">COLOR TEST DARK</button>
    <button onclick="setPreferredColorScheme('light')">COLOR TEST LIGHT</button>
    <button onclick="changeColorScheme('dark')">COLOR TEST DARK</button>
    <button onclick="changeColorScheme('light')">COLOR TEST LIGHT</button>
    <button onclick="changeColorScheme()">COLOR TEST SYSTEM</button>
    <button id="colors-mode-toggler">TOGGLE COLOR</button>
    <div class="testcolor"></div>
                        <div class="card huge-title full transparent">
                            <div class="flex">
                                <p class="x-title">Debug data</p>
                                <button onclick="AJAXtest()">AJAXTEST</button>
                                <div id="test_xyz">TEST</div>
                            </div>
                        </div>
                    </div>

                    <h5>
                    <?php
                    if (Arr::exists($guilds, $id))  {
                        //echo json_encode($thisGuild);
                        //echo 'guildDB: ' . json_encode($guildDB);
                        echo'<br> GUILDS: ' . json_encode($guild);
                    } else {
                        echo 'No guild found';
                    }
                    ?></br></h5>