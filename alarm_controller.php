<?php

    $action = $_POST["send"];
    echo("action: ".$action."<br>");

    // TODO check input from form

    if ($action == "Cancel alarm") {
        // if there's no alarm set, don't do cancel code
        if (!file_exists("alarm_set")) {
            $info = "No alarm to cancel.";
        }
        // if there is an alarm, cancel it
        else {
            touch("cancel_alarm");
            // sleep until alarm file removed
            while(file_exists("alarm_set")) {
                sleep(1);
            }
            $info = "Alarm cancelled!";
        }

        header("Location: index.php?info=" . $info);
    }
    elseif ($action == "Set alarm") {
        $alarmtime = $_POST["alarmtime"];
        // if the input is a valid time 00:00 - 23:59
        if (preg_match("([01]?[0-9]|2[0-3]):[0-5][0-9]", $alarmtime)) {
            $cmd = "python3 /var/www/html/Python-Alarm-Clock/main.py " . $alarmtime;

            // run script, redirect output and error output to log file and run in background(&)
            echo exec($cmd . " > /var/www/html/Python-Alarm-Clock/script.log 2>&1 &");

            // sleep until alarm file is set
            while(!file_exists("alarm_set")) {
                sleep(1);
            }
            header("Location: index.php");
        }
        // if the input is invalid
        else {
            header("Location: index.php?info=Invalid input.");
        }
    }

?>
