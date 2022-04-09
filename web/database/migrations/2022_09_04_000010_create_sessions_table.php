<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('sessions', function (Blueprint $table) {
            $table->id()->primary();
            $table->string('ip_address')->nullable();
            $table->string('username');
            $table->string('discriminator');
            //$table->string('email')->unique();
            //$table->timestamp('email_verified_at')->nullable();
            //$table->string('password');
            $table->string('avatar')->nullable();
            $table->array('payload')->nullable();
            //$table->rememberToken();
            $table->string('refresh_token')->nullable();
            $table=>integer('last_activity')->index();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('users');  
    }
};
