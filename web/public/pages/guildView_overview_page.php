<?php
        $user = Session::get('user');
        $guilds = Session::get('guilds');
        $guild = $guilds[$id];
        $view = $view;
    ?>

<div class="card-container">
                    <?php
                    if ($guild->has_bot)
                    {
                        $s= 'Current';
                    } else {
                        $s= 'Absent';
                    }
                    ?>
                    <div class="card full transparent">
                        <div class="flex x-center">
                            <?php echo '<img class="icon" src="' . $guild->icon_url . '">'; ?>
                            <p class="x-title"><?php echo $guild->name; ?></p>
                        </div>
                    </div>
                    <div class="card">
                        <p class="title">Overwiew</p>
                        <ul class="no-points">
                            <li><span> Name: </span> <?php echo '<span class="bg-text">' . $guild->name . '</span>' ; ?> </li>
                            <li><span> Id: </span> <?php echo '<span class="bg-text">' . $guild->id . '</span>' ; ?> </li>
                            <li><span> Bot: </span> <?php echo '<span class="bg-text">' . $s . '</span>' ; ?> </li>
                            <li><span> Role: </span> <?php echo '<span class="bg-text">' . $guild->role . '</span>' ; ?> </li>
                        </ul>
                    </div>
                    <div class="card wide">
                        <p class="title">Features</p>
                        <div class="tags">
                        <?php
                            if (!$guild->features) {
                                echo '<span class="x-title xy-center"> N/A</span>';
                            } else {
                                foreach($guild->features as $feature) {
                                    echo '<div class="tag"><h4>' . $feature . '</h4></div>';
                                }
                            }
                        ?>
                        </div>
                    </div>
                    <div class="card">
                        <p class="title">Data</p>
                        <ul class="no-points">
                            <li><span> Members: </span> <?php echo '<span class="bg-text">' . $guild->name . '</span>' ; ?> </li>
                            <li><span> Message service: </span> <?php echo '<span class="bg-text">' . $guild->id . '</span>' ; ?> </li>
                            <li><span> Bot: </span> <?php echo '<span class="bg-text">' . $s . '</span>' ; ?> </li>
                            <li><span> Role: </span> <?php echo '<span class="bg-text">' . $guild->role . '</span>' ; ?> </li>
                        </ul>
                    </div>
                    <div class="card wide">
                        <p class="title">Key-words</p>
                        <div id="input-container" class="tags">
                            <div class="tag flex"><input type="text" id="keyword-entry" class="cover" maxlength="20" placeholder="Enter word"/> <button class="text" onclick="addInput()">Add key-word</button></div>
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