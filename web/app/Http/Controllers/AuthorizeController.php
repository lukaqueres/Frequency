<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;

class AuthorizeController extends Controller
{

    public function discord_auth(Request $request)
    {
        protected string $tokenURL = "https://discord.com/api/oauth2/token";
        protected string $apiURLBase = "https://discord.com/api/users/@me";
        protected array $tokenData = [
        "client_id" => 875271995644842004,
        "client_secret" => "mPz7t6RNjmwerfLXN7LlB6-awue-6nUN",
        "grant_type" => "authorization_code",
        "code" => NULL,
        "redirect_uri" => "https://web-plan-it.herokuapp.com/discord/authorize",
        "scope" => "identify guilds guilds.members.read"
    ];
        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();
 
            return redirect()->intended('dashboard');
        }

        // Checking if the authorization code is present in the request.
        if ($request->missing('code')) {
            if (env('APP_DEBUG')) {
                return response()->json([
                    'discord_message' => config('discord.error_messages.missing_code', 'The authorization code is missing.'),
                    'code' => 400
                ]);
            } else {
                return redirect('/')->with('error', config('discord.error_messages.missing_code', 'The authorization code is missing.'));
            }
        }

        // Getting the access_token from the Discord API.
        try {
            $accessToken = $this->getDiscordAccessToken($request->get('code'));
        } catch (\Exception $e) {
            if (env('APP_DEBUG')) {
                return response()->json([
                    'discord_message' => config('discord.error_messages.invalid_code', 'The authorization code is invalid.'),
                    'message' => $e->getMessage(),
                    'code' => $e->getCode()
                ]);
            } else {
                return redirect('/')->with('error', config('discord.error_messages.invalid_code', 'The authorization code is invalid.'));
            }
        }
        return view('guild');
    }

    /**
     * Handles the Discord OAuth2 callback.
     *
     * @param string $code
     * @return object
     * @throws \Illuminate\Http\Client\RequestException
     */
    private function getDiscordAccessToken(string $code): object
    {
        $this->tokenData['code'] = $code;

        $response = Http::asForm()->post($this->tokenURL, $this->tokenData);

        $response->throw();

        return json_decode($response->body());
    }

    /**
     * Handles the Discord OAuth2 login.
     *
     * @param string $access_token
     * @return object
     * @throws \Illuminate\Http\Client\RequestException
     */
    private function getDiscordUser(string $access_token): object
    {
        $response = Http::withToken($access_token)->get($this->apiURLBase);

        $response->throw();

        return json_decode($response->body());
    }
}
