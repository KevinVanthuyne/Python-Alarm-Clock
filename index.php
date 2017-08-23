<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Alarm Clock</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
    <link rel="icon" href="images/alarm_clock128.png">
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>

    <div id="background">
        <div id="wrapper">
            <a href="index.php"><h1>Raspi Alarm Clock</h1></a>
            <?php
                # if alarm file exists (an alarm is set)
                # display the alarm time
                if (file_exists("alarm_set")) {
                    $alarm_file = fopen("alarm_set", "r");
                    $alarm_time = fgets($alarm_file);
                    echo("<p>Alarm is set at " . $alarm_time . "</p>");
                    fclose($alarm_file);
                }
                // if there's an info message, print it
                if (isset($_GET['info'])) {
                    echo("<p>" . $_GET['info'] . "<p>");
                }
            ?>
            <form action="alarm_controller.php?action=set_alarm" method="post">
                <label for="alarmtime">Alarm time: </label><input name="alarmtime" id="alarmtime" type="time" required>
                <p>
                    <input type="submit" value="Set alarm">
                </p>
            </form>
            <form action="alarm_controller.php?action=cancel_alarm" method="post">
                <p>
                    <input type="submit" value="Cancel alarm">
                </p>
            </form>

            <a href="index.php"><img src="images/icon-refresh-50.png" alt="refresh button"></a>
            <a href="alarm_controller.php?action=settings"><img src="images/gear-50.png" alt="settings button"></a>

        </div>
    </div>
</body>
</html>
