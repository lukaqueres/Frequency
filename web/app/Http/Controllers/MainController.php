<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class MainController extends Controller
{
    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Contracts\Support\Renderable
     */
    public function index()
    {
        return view('main');
    }

    public function view(Request $request)
    {
        $data = array();
        $data['id']=$request->id;
        if ($data['id'] == 0) {
            return redirect()->route('manage');
        }
        return view('main', $data);
    }

    public function manage_view(Request $request)
    {
        $data = array();
        $data['id']=$request->id;
        return view('manage', $data); 
    }

    public function user_view(Request $request)
    {
        $data = array();
        $data['view']=$request->view;
        return view('user', $data);
    }

    public function guild_view(Request $request)
    {
        $data = array();
        $data['id']=$request->id;
        $data['view']=$request->view;
        return view('guild', $data);
    }
}
