<?php

    $action = $_POST["send"];
    echo("action: ".$action."<br>");
    $info;

    // if action is cancel alarm, make cancel flag file
    if ($action == "Cancel alarm") {
        touch("cancel_alarm");
        echo("Alarm cancelled!");
        $info = "Alarm cancelled!";
    }
    elseif ($action == "Set alarm") {
        $alarmtime = $_POST["alarmtime"];
        $cmd = "python3 /var/www/html/main.py " . $alarmtime;

        echo "Command executed: " . $cmd . "<br>";
        echo "Alarm is set at " . $alarmtime;

        // run script, redirect output and error output to log file and run in background(&)
        echo exec($cmd . " > /var/www/html/script.log 2>&1 &");

        $info = "Alarm set!";
    }

    header("Location: index.php?info=" . $info);

?>
