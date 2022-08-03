<?php
        $user = Session::get('user');
        $guilds = Session::get('guilds');
        $guild = $guilds[$id];
        $view = $view;
    ?>

<div class="card-container">
                        <div class="card huge-title full transparent">
                            <div class="flex">
                                <p class="x-title">Text settings</p>
                            </div>
                        </div>
                        <div class="card">
                            <p class="title">General</p>
                            <ul class="no-points">
                                <li><input type="checkbox" id="filter_messages"/><span>Report </span></li>
                                <li><input type="checkbox" id="notify_flagged"/><span>Delete suspicious links</span></li>
                                <li><input type="checkbox" id="delete_flagged"/><span>Delete all links</span></li>
                                <li><input type="checkbox" id="delete_invites"/><span>Delete discord invites</span></li>
                            </ul>
                        </div>
                        <div class="card transparent full card-container">
                            <div class="card transparent">
                                <ul class="no-points">
                                    <li><label class="chck-label"><input type="checkbox" id="filter_messages"/><span class="label">Delete links</span></label></li>
                                    <li><label class="chck-label"><input type="checkbox" id="notify_flagged"/><span class="label">Enable internal links filter</span></label></li>
                                    <li><label class="chck-label"><input type="checkbox" id="delete_flagged"/><span class="label">Delete all links</span></label></li>
                                    <li><label class="chck-label"><input type="checkbox" id="delete_invites"/><span class="label">Delete discord invites</span></label></li>
                                </ul>
                            </div>
                            <div class="card transparent">
                                <ul class="no-points">
                                    <li><label class="chck-label"><input type="checkbox" id="blacklist_domains"/><span class="label">Blacklist domains</span></label><span class="explanation"><span class="explanation-mark"><ion-icon name="information-circle"></ion-icon></span><div class="explanation-content">Input domain name to be marked as blacklisted. Read More</div></span></li>
                                    <li><div class="input-holding" id="blacklisted_domains"><div class="input"><input type="text" id="blacklist_domains_input" placeholder="Add blacklisted domain"/><button>+</button></div></div></li>
                                    <li><label class="chck-label"><input type="checkbox" id="whitelist_domains"/><span class="label">Whitelist domains</span></label></li>
                                    <li><div><input type="text" id="whitelist_domains_input" placeholder="Add whitelisted domain"/></div></li>
                                </ul>
                            </div>
                        </div>
                    </div>