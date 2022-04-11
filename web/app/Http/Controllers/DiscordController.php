<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;
use App\Http\Controllers\Controller;

class DiscordController extends Controller
{

	public function authorizeMe(Request $request)
	{
		//$session = SessionModel::all();
		
		Session::put('name', 'John Doe');
		Session::put('username', 'lukaqueres');
		Session::save();
		return view('guild'); 
	}
}
