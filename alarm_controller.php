<?php

    $action = $_POST["send"];
    echo("action: ".$action."<br>");

    // TODO check input from form

    // if action is cancel alarm, make cancel flag file
    if ($action == "Cancel alarm") {
        touch("cancel_alarm");

        // sleep until cancel file is set and alarm file removed
        while(file_exists("alarm_set")) {
            sleep(1);
        }

        $info = "Alarm cancelled!";
        header("Location: index.php?info=" . $info);
    }
    elseif ($action == "Set alarm") {
        $alarmtime = $_POST["alarmtime"];
        $cmd = "python3 /var/www/html/Python-Alarm-Clock/main.py " . $alarmtime;

        // run script, redirect output and error output to log file and run in background(&)
        echo exec($cmd . " > /var/www/html/Python-Alarm-Clock/script.log 2>&1 &");

        // sleep until alarm file is set
        while(!file_exists("alarm_set")) {
            sleep(1);
        }
        header("Location: index.php");
    }

?>
