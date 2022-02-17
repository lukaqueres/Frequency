<?php
// This function reads your DATABASE_URL config var and returns a connection[
// string suitable for pg_connect. Put this in your app.
function pg_connection_string_from_database_url() 
{
  extract(parse_url($_ENV["DATABASE_URL"]));
  
  return "user=$user password=$pass sslmode=require host=$host dbname=" . substr($path, 1); # <- you may want to add sslmode=require there too
}

class DatabaseManager {

  private $result=0;

  function get_dbmembers($pg_conn)
    {   
      $members = pg_query($pg_conn, "SELECT SUM(number_of_members) as members FROM servers_properties");
      $result = pg_fetch_assoc($members);
      
      $result = add_zeros($result['members'], 5);
      return $result;
    }
  
  function get_dbguilds($pg_conn)
    {
      $guilds = pg_query($pg_conn, "SELECT COUNT(*) as guilds FROM servers_properties");
      $result = pg_fetch_assoc($guilds);
      
      $result = add_zeros($result['guilds'], 5);
      return $result;
    }
 
}

function append_string ($str1, $str2) {
      
    // Using Concatenation assignment
    // operator (.=)
    $str1 .=$str2;
      
    // Returning the result 
    return $str1;
}

function add_zeros($string, $number)
{
  for ($i = 0; $i < $number; $i++) 
  {
    $string = '0' . $string;
  }
  $length = strlen($string): int;
  $length -= $number;
  $string = substr($string, $lenght, $number);
  
  return $string;
  }
?>
