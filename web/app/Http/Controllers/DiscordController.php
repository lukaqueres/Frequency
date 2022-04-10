<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;

class DiscordController extends Controller
{

    public function authorize(Request $request)
    {
        //$session = SessionModel::all();
        
        Session::put('name', 'John Doe');
        session(['username' => 'John_Doe210328']);
        Session::save();
        return view('guild');
    }
