<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\Session as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class Session extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'id',
        'username',
        'discriminator',
        'avatar',
        'payload',
        'last_activity',
        'user_agent'
    ];

    /**
     * The attributes that should be hidden for serialization.
     *
     * @var array<int, string> 
     */
    protected $hidden = [
        'refresh_token',
        'remember_token',
        'ip_address',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'id' => 'string',
        'username' => 'string',
        'discriminator' => 'string',
        'avatar' => 'string',
        'payload' => 'json',
        'refresh_token' => 'encrypted',
        'ip_address' => 'string',
        'last_activity' => 'integrer',
        'user_agent' => 'string',
    ];
}
