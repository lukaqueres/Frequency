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

    public function __construct() // Construct data for http requests
    {
        $this->tokenData['client_id'] = "875271995644842004";
        $this->tokenData['client_secret'] = "mPz7t6RNjmwerfLXN7LlB6-awue-6nUN";
        $this->tokenData['grant_type'] = "authorization_code";
        $this->tokenData['redirect_uri'] = "https://web-plan-it.herokuapp.com/discord/authorize";
        $this->tokenData['scope'] = "identify guilds guilds.members.read";
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
        $data = [];
        $guilds_preview = [];
        $data['user'] = $user;

        foreach($guilds as $guild) {
            //var_dump($guild->permissions);
            //$guild['permissions_names'] = get_permissions($guild->permissions);
            $guild->p_tag = get_user_permissions_tag(get_permissions($guild->permissions));
            $guild->tags = get_guild_tags($guild);
            $guilds_preview[] = [ $guild->id, $guild->name, $guild->icon, $guild->tags ];
            $data[$guild->id] = $guild;
        }
        $data['guilds'] = $guilds_preview;
        
        if (! Session::exists('data')) {
            //Session::put('access_token', $accessToken);
		    //Session::put('user_data', $user);
            Session::put('data', $data);
            Session::save();
        }

		return redirect('manage');
	}
}
