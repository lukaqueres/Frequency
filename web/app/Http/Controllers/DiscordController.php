<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Http;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Arr;

use Guild;
use app\helpers\NotificationGenerator;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class DiscordController extends Controller
{
    protected string $tokenURL = "https://discord.com/api/oauth2/token";
    protected string $apiURLBase = "https://discord.com/api/users/@me";

    protected array $tokenData = [
        "client_id" => NULL,
        "client_secret" => NULL,
        "grant_type" => "authorization_code",
        "code" => NULL,
        "redirect_uri" => NULL,
        "scope" => null
    ];

    private function getAccessToken(string $code): object // Retrives Discord acces token by http request
    {
        $this->tokenData['code'] = $code;

        $response = Http::asForm()->post($this->tokenURL, $this->tokenData);

        $response->throw();

        return json_decode($response->body());
    }

    private function getUser(string $access_token): object // Return Discord's user array. It contain data such as nick, avatar, if verified or e-mail
    {
        $response = Http::withToken($access_token)->get($this->apiURLBase);

        $response->throw();

        return json_decode($response->body());
    }

    private function getGuilds(string $access_token): array // Return array containing User's guilds. Every guild array contain their permissions, are they owner, guild's icon, name etc.
    {
        $response = Http::withToken($access_token)->get($this->apiURLBase . "/guilds");

        $response->throw();

        return json_decode($response->body());
    }

    private function getDBdata(array $guildsIds) // Append to guild object data from DB
    {
        // Add code hir
        $guildsDB = DB::connection('alt')->table('servers_properties')
                    ->join('servers_msg_process', 'servers_properties.guild_id', '=', 'servers_msg_process.guild_id')
                    ->whereIn('servers_properties.guild_id', $guildsIds)
                    ->get();

        return $guildsDB;
    }

    private function getguildsDB($guilds) // Iterate on guilds to work on DB data
    {
        $guildsIds = [];
        foreach($guilds as $id=>$guild)
        {
            //$ids = $guild->$id;

            $guildsIds[] = $id;
            
            /*
            if (DB::table('servers_properties')->where('guild_id', $id)->exists()) {
                $guild->isbot = True;
                
            } else {
                $guild->isbot = False;
            }*/
        }
        //return response()->json(['error_message' => $guildsIds]);
        $DBguilds = [];
        foreach($guildsIds as $id)
        {
            $DBguilds[$id] = False;
        }

        $DBdata = $this->getDBdata($guildsIds);
        foreach($DBdata as $guild)
        {
            $guild->invited = True;
            $id = $guild->guild_id;
            $DBguilds[$id] = $guild;
        }

        return $DBguilds;
    }

    public function __construct() // Construct data for http requests
    {
        $this->tokenData['client_id'] = "875271995644842004";
        $this->tokenData['client_secret'] = "mPz7t6RNjmwerfLXN7LlB6-awue-6nUN";
        $this->tokenData['grant_type'] = "authorization_code";
        $this->tokenData['redirect_uri'] = "https://web-plan-it.herokuapp.com/discord/authorize";
        $this->tokenData['scope'] = "identify guilds guilds.members.read email";
        $this->tokenData['status'] = "/manage/guild/640181649463705650";
    }

    public function unAuthorizeMe(Request $request)
    {
        $request->session()->flush();
        return redirect('/');
    }

	public function authorizeMe(Request $request) // Handle autorization requests from path. Used for fetching user's data from Discord
	{
        if($request->error == 'access_denied') { // Check if user failed to authorize trough discord page
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'User did not completed authorization.',
                    'code' => 400
                ]);
            } else {
                Session::flash('status', 'Failed authorization');
                return redirect('/');
            }
        }

        if ($request->missing('code')) { // Checking if the authorization code is present in the request
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'The authorization code is missing.',
                    'code' => 400
                ]);
            } else {
                Session::flash('status', 'Missing authorization');
                return redirect('/');
            }
        }

        try { // Getting the access token from the Discord API
            $accessToken = $this->getAccessToken($request->get('code'));
        } catch (\Exception $e) {
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'The authorization code is invalid. Error getting acces token',
                    'message' => $e->getMessage(),
                    'code' => $e->getCode()
                ]);
            } else {
                Session::flash('status', 'Invalid authorization');
                return redirect('/');
            }
        }

        try { // Using the access_token to get the user
            $user = $this->getUser($accessToken->access_token);
        } catch (\Exception $e) {
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'The authorization failed while getting user.',
                    'message' => $e->getMessage(),
                    'code' => $e->getCode()
                ]);
            } else {
                Session::flash('status', 'Invalid authorization');
                return redirect('/');
            }
        }

        try { // Using the access_token to get guilds
            $guilds = $this->getGuilds($accessToken->access_token);
        } catch (\Exception $e) {
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'The authorization failed during guilds fetching.',
                    'message' => $e->getMessage(),
                    'code' => $e->getCode()
                ]);
            } else {
                Session::flash('status', 'Invalid authorization');
                return redirect('/');
            }
        }
        /*
        // Making nice arrays for guilds
        $data = array();
        $guilds_snippets = [];
        //$data['user'] = $user;

        foreach($guilds as $guild) {
            //var_dump($guild->permissions);
            //$guild['permissions_names'] = get_permissions($guild->permissions);
            $guild->p_tag = get_user_permissions_tag(get_permissions($guild->permissions));
            $guild->tags = get_guild_tags($guild);
            $this_guild = [];
            $this_guild['id'] = $guild->id;
            $this_guild['name'] = $guild->name;
            $this_guild['icon'] = $guild->icon;
            $this_guild['tags'] = $guild->tags;
            //$guilds_preview[] = $this_guild;
            $guilds_snippets[] = [ "id" => $guild->id, "name" => $guild->name, "icon" => $guild->icon, "tags" => $guild->tags];
            $data['guilds'][$guild->id] = $guild;
            $data['snippets'] = $guilds_snippets;
        }
        */
        $data = array();
        foreach($guilds as $guild) {
            $data['guilds'][$guild->id] = $guild;
        }
        $DBdata = $this->getguildsDB($data['guilds']);

        $guildsObj = array();
        foreach($guilds as $guild) {
            $guildsObj[$guild->id] = new Guild($guild->id);
            $guildsObj[$guild->id]->assign($guild, $DBdata[$guild->id]);
        }

        //$data['guilds']['snippets'] = $guilds_snippets;
        //return var_dump($data['guilds']);
        //return response()->json(['guilds' => $data['guilds'] ]); 
        
        //Session::put('access_token', $accessToken);
		//Session::put('user_data', $user);
        //Session::put('data', $data);
        /*Session::put('DBdata', $DBdata);*/
        Session::put('guilds', $guildsObj);

        Session::put('user', $user);
        Session::put('authorized', true);
        Session::save();

        if ($request->missing('state')) {
            return redirect('manage');
        }
        else {
            $redirUrl= $request->state;
            return redirect($redirUrl);
        }
	}

    public function showManage(Request $request)
    {
        if ( !(Session::has('authorized') && Session::get('authorized') == True )) { // Check if user is authorized before returning proper view
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'User is not authorized.',
                ]);
            } else {
                Session::flash('notification', 'Not authorized');
                return redirect('/');
            }
        }
        $data = array();
        return view('manage', $data); 
    }

    public function showUser(Request $request)
    {
        if ( !(Session::has('authorized') && Session::get('authorized') == True )) { // Check if user is authorized before returning proper view
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'User is not authorized.',
                ]);
            } else {
                Session::flash('notification', 'Not authorized');
                return redirect('/');
            }
        }
        $data = array();
        $data['view']=$request->view;
        return view('user', $data);
    }

    public function Guildview(Request $request)
    {
        if ( !(Session::has('authorized') && Session::get('authorized') == True )) { // Check if user is authorized before returning proper view
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'User is not authorized.',
                ]);
            } else {
                $notification = new NotificationGenerator('Not authorized', 'User not found, authorize through discord in order to continue. Link below after authorization will redirect to wanted destination.');
                $notification->addUrl('Authorize', gen_authorization_link(url()->current()));
                $notification->generate();
                Session::flash('notification', $notification);
                return redirect('/');
            }
        }
        $guilds = Session::get('guilds');
        if (! (Arr::exists($guilds, $request->id)))  { // Check if user is in guild with given id
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'Guild not found.',
                ]);
            } else {
                $notification = new NotificationGenerator('Guild not found', 'Guild not found, check if provided guild id is correct and authorized user is member in it.');
                $notification->generate();
                Session::flash('notification', $notification);
                //return var_dump($notification);
                return redirect('/manage');
            }
        }

        if (!$guilds[$request->id]->has_bot)  { // Check if bot is in guild
            $notification = new NotificationGenerator('Bot is not present', 'Bot has not still been invited to this guild. Invite it to unlock multiple configuration options.');

            if ($guilds[$request->id]->role == 'administrator' || $guilds[$request->id]->role == 'owner') {
                $notification->addUrl('Invite', 'https://discord.com/api/oauth2/authorize?client_id=875271995644842004&permissions=8&scope=bot%20applications.commands', 'target="_blank"');
            }
            $notification->generate();
            Session::flash('notification', $notification);
            //return var_dump($notification);
        }

        $data = array();
        $data['id']=$request->id;
        $data['view']=$request->view;
        return view('guild', $data);
    }
}
