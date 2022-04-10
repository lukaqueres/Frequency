<?php

namespace App\Http\Controllers\Discord;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;
use App\Http\Controllers\Controller;

class DiscordController extends Controller
{

	public function authorize(Request $request)
	{
		//$session = SessionModel::all();
		
		Session::put('name', 'John Doe');
		session(['username' => 'John_Doe210328']);
		Session::save();
		return view('guildyjklkksuksyfsfgskgwygfcsgfsfgksfgsgcvcfvkwseyuyfeuyfjdhdvcjdgvd'); 
	}
}
