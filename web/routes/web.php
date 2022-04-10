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

Route::get('/', 'MainController@index');

Route::get('/manage/{view?}', 'MainController@manage_view');
Route::get('/manage/guild/{id}/{view?}', 'MainController@guild_view');
Route::get('/manage/user/{view?}', 'MainController@user_view');

//Route::get('/discord/authorize', 'DiscordController@authorizeMe');
Route::get('/discord/authorize', '\App\Http\Controller\DiscordController@authorizeMe');