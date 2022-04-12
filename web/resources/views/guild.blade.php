Guild</br>
NAME:{{Session::get('name')}}</br>
GUILD_DATA: <?php
$data = Session::get('data');
if (Arr::exists($data[$id]))  {
    echo json_encode($data[$id]);
} else {
    echo 'No guild found';
}
?></br>
