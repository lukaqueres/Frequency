<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;
use App\Http\Controllers\Controller;

class DiscordController extends Controller
{

	public function authorizeMe(Request $request)
	{
        if ($request->isMethod('post')) {
            $value = $request->header("access_token");
            echo $valuel;
            Session::put('name', 'John Doe');
		    Session::put('username', 'lukaqueres');
		    Session::save();
        }

        //var_dump($request);
		return view('guild'); 
	}
}
