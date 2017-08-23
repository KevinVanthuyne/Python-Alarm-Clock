<?php
    $alarm_folder = "/var/www/html/Python-Alarm-Clock/";
    $action = $_GET["action"];

    echo("action: ".$action."<br>");

    // TODO check input from form

    if ($action == "cancel_alarm") {
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
    elseif ($action == "set_alarm") {
        // if another alarm is already set, give errors
        if (file_exists("alarm_set")) {
            header("Location: index.php?info=Another alarm is already set.<br>Cancel the current one first.");
        }
        else {
            $alarmtime = $_POST["alarmtime"];
            // if the input is a valid time 00:00 - 23:59
            if (preg_match("/([01]?[0-9]|2[0-3]):[0-5][0-9]/", $alarmtime)) {
                $cmd = "python3 " . $alarm_folder . "main.py " . $alarmtime;

                // run script, redirect output and error output to log file and run in background(&)
                echo exec($cmd . " > " . $alarm_folder . "script.log 2>&1 &");

                // sleep until alarm file is set
                while(!file_exists("alarm_set")) {
                    sleep(1);
                }
                // echo($alarmtime);
                header("Location: index.php");
            }
            // if the input is invalid
            else {
                header("Location: index.php?info=Invalid input.");
            }
        }
    }
    // if there is a settings file, put values into form
    elseif ($action == "settings") {
        if (file_exists("alarm_settings")) {
            // Read file contents into array of lines
            $contents = file($alarm_folder . "alarm_settings");

            // function for searching a substring in array of strings,
            // returning the full string
            function search_array($string, $array) {
                foreach($array as $entry) {
                    // searches substring $string in $entry
                    if (strpos($entry, $string) !== false) {
                        return $entry;
                    }
                }
            }

            // search for every setting in settings file
            $volume = search_array("volume", $contents);

            header("Location: settings.php?" . $volume);
        }
    }
    // write every setting back to the settings file
    elseif ($action == "save_settings") {
        // check input
        $volume = floatval($_POST['volume']);
        if ($volume < 0 || $volume > 1 ) {
            header("Location: settings.php?info=Volume must be between 0 and 1.");
        }
        else {
            // change settings
            $settings_file = fopen("alarm_settings", "w");

            fwrite($settings_file, "volume=" . $_POST['volume'] . "\n");
            fwrite($settings_file, "lijn2=1");

            fclose($settings_file);

            header("Location: index.php?info=Settings saved.");
        }
    }

?>
