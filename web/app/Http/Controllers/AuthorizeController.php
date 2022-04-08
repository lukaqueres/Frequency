<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class AuthorizeController extends Controller { 
    public function discord_auth(Request $request)
    {
        Session::put('name', 'John Doe');
        return view('guild'); 
    }

}
