<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Http;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;
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

    public function __construct()
    {
        $this->tokenData['client_id'] = "875271995644842004";
        $this->tokenData['client_secret'] = "mPz7t6RNjmwerfLXN7LlB6-awue-6nUN";
        $this->tokenData['grant_type'] = "authorization_code";
        $this->tokenData['redirect_uri'] = "https://web-plan-it.herokuapp.com/discord/authorize";
        $this->tokenData['scope'] = "identify guilds guilds.members.read";
    }

    private function getAccessToken(string $code): object
    {
        $this->tokenData['code'] = $code;

        $response = Http::asForm()->post($this->tokenURL, $this->tokenData);

        $response->throw();

        return json_decode($response->body());
    }

    private function getUser(string $access_token): object
    {
        $response = Http::withToken($access_token)->get($this->apiURLBase);

        $response->throw();

        return json_decode($response->body());
    }

    private function getGuilds(string $access_token): array
    {
        $response = Http::withToken($access_token)->get($this->apiURLBase . "/guilds");

        $response->throw();

        return json_decode($response->body());
    }

	public function authorizeMe(Request $request)
	{
        // Checking if the authorization code is present in the request.
        if ($request->missing('code')) {
            if (env('APP_DEBUG')) {
                return response()->json([
                    'larascord_message' => 'The authorization code is missing.',
                    'code' => 400
                ]);
            } else {
                Session::flash('status', 'Missing authorization code');
                return redirect('/');
            }
        }

        // Getting the access_token from the Discord API.
        try {
            $accessToken = $this->getAccessToken($request->get('code'));
        } catch (\Exception $e) {
            if (env('APP_DEBUG')) {
                return response()->json([
                    'larascord_message' => 'The authorization code is invalid.',
                    'message' => $e->getMessage(),
                    'code' => $e->getCode()
                ]);
            } else {
                Session::flash('status', 'Invalid authorization code');
                return redirect('/');
            }
        }

        // Using the access_token to get the user.
        try {
            $user = $this->getUser($accessToken->access_token);
        } catch (\Exception $e) {
            if (env('APP_DEBUG')) {
                return response()->json([
                    'larascord_message' => 'The authorization failed.',
                    'message' => $e->getMessage(),
                    'code' => $e->getCode()
                ]);
            } else {
                Session::flash('status', 'Invalid authorization code');
                return redirect('/');
            }
        }

        // Using the access_token to get guilds
        try {
            $guilds = $this->getGuilds($accessToken->access_token);
        } catch (\Exception $e) {
            if (env('APP_DEBUG')) {
                return response()->json([
                    'larascord_message' => 'The authorization failed.',
                    'message' => $e->getMessage(),
                    'code' => $e->getCode()
                ]);
            } else {
                Session::flash('status', 'Invalid authorization code');
                return redirect('/');
            }
        }

        if (! Session::exists('token')) {
            Session::put('access_token', $accessToken);
		    Session::put('user_data', $user);
            Session::put('guilds_data', $guilds);
        }

        Session::save();
		return redirect('manage');
	}
}
