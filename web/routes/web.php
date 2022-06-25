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

Route::get( '/manage/', 'DiscordController@showManage' )->name('manage');

Route::get('/', 'MainController@index');

Route::get('/manage/{view?}', 'DiscordController@showManage');
Route::get('/manage/guild/{id}/{view?}', 'DiscordController@Guildview');
Route::get('/manage/user/{view?}', 'DiscordController@showUser');

Route::match(['get', 'post'], '/discord/authorize', 'DiscordController@authorizeMe');
Route::get('/discord/logout', 'DiscordController@unAuthorizeMe');

Route::get('/app/debug', 'MainController@debug');
