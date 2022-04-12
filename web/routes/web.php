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

Route::get( '/manage/', 'MainController@showManage' )->name('manage');

Route::get('/', 'MainController@index');

Route::get('/manage/{view?}', 'DiscordController@showManage');
Route::get('/manage/guild/{id}/{view?}', 'DiscordController@showGuild');
Route::get('/manage/user/{view?}', 'DiscordController@showUser');

Route::match(['get', 'post'], '/discord/authorize', 'DiscordController@authorizeMe');
