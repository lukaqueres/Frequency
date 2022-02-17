<?php
// This function reads your DATABASE_URL config var and returns a connection[
// string suitable for pg_connect. Put this in your app.
function pg_connection_string_from_database_url() {
  extract(parse_url($_ENV["DATABASE_URL"]));
  return "user=$user password=$pass sslmode=require host=$host dbname=" . substr($path, 1); # <- you may want to add sslmode=require there too
}

// Here we establish the connection. Yes, that is all.
$pg_conn = pg_connect(pg_connection_string_from_database_url());


class DatabaseManager {

  private $result=0;

  public function get_dbmembers()
    {   
      $members = pg_query($pg_conn, "SELECT SUM(number_of_members) as total FROM servers_properties");
      $result = pg_fetch_assoc($members);
      return $result['total'];
    }
  
  public function get_dbguilds()
    {
      $result = pg_query($pg_conn, "SELECT COUNT(*) FROM servers_properties");
      $numberOfGuilds = pg_fetch_row($result);
      return $result[0];
    }
}
?>
