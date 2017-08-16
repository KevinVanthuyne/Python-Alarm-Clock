<?php
    $alarmtime = $_POST["alarmtime"];
    $cmd = "python3 /var/www/html/main.py " . $alarmtime;
    // $cmd = "python alarm.py " . $alarmtime;

    echo "Command executed: " . $cmd;
    echo "Alarm is set at " . $alarmtime;

    //echo shell_exec($cmd . " > /var/www/html/log &");
    echo shell_exec($cmd);
    //echo shell_exec("ls")
?>
