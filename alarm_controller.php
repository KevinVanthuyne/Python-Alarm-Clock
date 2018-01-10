<?php
    $alarm_folder = "/var/www/html/Python-Alarm-Clock/";
    $action = $_GET["action"];

    echo("action: ".$action."<br>");

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
                // calculate time until alarm (HH:MM)
                $now = new DateTime();
                $alarmtime_object = new DateTime($alarmtime);

                // TODO
                // if alarm time is earlier, time difference needs to be until tomorrow
                // h = hours, i = minutes
                if ($alarmtime_object->format("hi") < $now->format("hi")) {
                    echo("alarm is tomorrow, in: ");
                    $next_day = $alarmtime_object->modify("+1 day");
                    $time_until = $now->diff($next_day);
                }
                else {
                    echo("alarm is later today, in: ");
                    $time_until = $now->diff($alarmtime_object);
                }
                $time_until = $time_until->format("%h:%I");

                // run script, redirect output and error output to log file and run in background(&)
                echo exec($cmd . " > " . $alarm_folder . "script.log 2>&1 &");

                // sleep until alarm file is set
                // while(!file_exists("alarm_set")) {
                //     sleep(1);
                // }
                //echo("alarm goes off in " . $time_until);
                header("Location: index.php?info=Alarm goes off in " . $time_until);
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
            $volume = rtrim(search_array("volume", $contents));
            // max_time needs to be converted from seconds (for python) to minutes (for the user)
            $max_time = search_array("max_time", $contents);
            $max_time_seconds = explode("=", $max_time, 2);
            $max_time_minutes = $max_time_seconds[1] / 60;

            header("Location: settings.php?" . $volume . "&max_time=" . $max_time_minutes);
        }
        else {
            header("Location: index.php?info=No settings file found, set an alarm to create one.");
        }
    }
    // write every setting back to the settings file
    elseif ($action == "save_settings") {
        // check input
        $volume = floatval($_POST['volume']);
        $max_time = $_POST['max_time']; // in minutes

        if ($volume < 0 || $volume > 1 ) {
            header("Location: settings.php?info=Volume must be between 0 and 1.");
        }
        elseif ($max_time < 1 || $max_time > 30) {
            header("Location: settings.php?info=Maximum playtime must be between 1 and 30 minutes.");
        }
        else {
            // change settings
            $settings_file = fopen("alarm_settings", "w");

            fwrite($settings_file, "volume=" . $volume . "\n");
            fwrite($settings_file, "max_time=" . $max_time * 60); // convert minutes to seconds for python

            fclose($settings_file);

            header("Location: index.php?info=Settings saved.");
        }
    }

?>
