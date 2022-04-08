<?php  namespace Jakyeru\Larascord\Http\Controllers;  use Illuminate\Http\Request; use Illuminate\Support\Facades\Auth; use Illuminate\Support\Facades\Http; use App\Models\User; use App\Providers\RouteServiceProvider;  class AuthorizeController extends Controller { 
    public function discord_auth(Request $request)
    {
        Session::put('name', 'John Doe');
        return view('guild');
    }

}
