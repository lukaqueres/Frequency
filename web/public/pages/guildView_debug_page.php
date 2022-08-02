<?php
        $user = Session::get('user');
        $guilds = Session::get('guilds');
        $guild = $guilds[$id];
        $view = $view;
    ?>

<div class="card-container">
                        <div class="card huge-title full transparent">
                            <div class="flex">
                                <p class="x-title">Debug data</p>
                                <button onclick="AJAXtest()">TEST</button>
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