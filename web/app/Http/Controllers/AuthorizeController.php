<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;

class AuthorizeController extends Controller
{

    public function discord_auth(Request $request)
    {
        //$session = SessionModel::all();
        
        Session::put('name', 'John Doe');
        $request->session()->put('username', 'John_Doe');
        return view('guild');
    }
}
