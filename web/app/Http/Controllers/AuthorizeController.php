<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;

class AuthorizeController extends Controller
{

    public function discord_auth(Request $request)
    {
        Session::put('name', 'John Doe');
        return view('guild');
    }

}
