<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Http;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Arr;

use App\Http\Controllers\Controller;

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

    private function getDBdata(object $guild): object // Append to guild object data from DB
    {
        // Add code hir
    }

    private function getguildsDB(array $guilds): array // Iterate on guilds to work on DB data
    {
        if (DB::table('servers_properties')->where('guild_id', $id)->exists()) {
            $guild->isbot = True;
            getDBdata($guild);
        } else {
            $guild->isbot = False;
        }
    }

    public function __construct() // Construct data for http requests
    {
        $this->tokenData['client_id'] = "875271995644842004";
        $this->tokenData['client_secret'] = "mPz7t6RNjmwerfLXN7LlB6-awue-6nUN";
        $this->tokenData['grant_type'] = "authorization_code";
        $this->tokenData['redirect_uri'] = "https://web-plan-it.herokuapp.com/discord/authorize";
        $this->tokenData['scope'] = "identify guilds guilds.members.read email";
    }

	public function authorizeMe(Request $request) // Handle autorization requests from path. Used for fetching user's data from Discord
	{
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

        //$data['guilds']['snippets'] = $guilds_snippets;
        //return var_dump($data['guilds']);
        //return response()->json(['guilds' => $data['guilds'] ]); 
        
        //Session::put('access_token', $accessToken);
		//Session::put('user_data', $user);
        Session::put('data', $data);
        Session::put('user', $user);
        Session::put('authorized', true);
        Session::save();

		return redirect('manage');
	}

    public function showManage(Request $request)
    {
        if ( !(Session::has('authorized') && Session::get('authorized') == True )) { // Check if user is authorized before returning proper view
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'User is not authorized.',
                ]);
            } else {
                Session::flash('status', 'Not authorized');
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
                Session::flash('status', 'Not authorized');
                return redirect('/');
            }
        }
        $data = array();
        $data['view']=$request->view;
        return view('user', $data);
    }

    public function showGuild(Request $request)
    {
        if ( !(Session::has('authorized') && Session::get('authorized') == True )) { // Check if user is authorized before returning proper view
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'User is not authorized.',
                ]);
            } else {
                Session::flash('status', 'Not authorized');
                return redirect('/');
            }
        }
        $data = Session::get('data')['guilds'];
        if (! (Arr::exists($data, $request->id)))  { // Check if user is in guild with given id
            if (env('APP_DEBUG')) {
                return response()->json([
                    'error_message' => 'Guild not found.',
                ]);
            } else {
                Session::flash('status', 'Guild not found');
                return redirect('/manage');
            }
        }
        $data = array();
        $data['id']=$request->id;
        $data['view']=$request->view;
        return view('guild', $data);
    }
}
