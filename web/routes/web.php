<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/
Route::get( '/manage/', 'MainController@manage_view' )->name('manage');
/*
Route::get('/', function () {
    return view('welcome');
});*/

Route::get('/', 'MainController@index');

Route::get('/manage/guild/{id}/{view?}', 'MainController@guild_view');
Route::get('/manage/user/{view?}', 'MainController@user_view');
Route::get('/discord/authorize', 'AuthorizeController@discord_auth');
//Route::get('/manage/', 'MainController@view');


//Error with installinh laravel/ui

//Auth::routes();
//Auth::routes(['register' => false]);
