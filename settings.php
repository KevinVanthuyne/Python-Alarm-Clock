<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Alarm Clock</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
    <link rel="icon" href="images/alarm_clock128.png">
    <link rel="stylesheet" type="text/css" href="style.css">

    <?php
        // get settings from setting file
        $volume = 1;

        if (isset($_GET['volume'])) {
            $volume = $_GET['volume'];
        }
    ?>

</head>
<body>

    <div id="background">
        <div id="wrapper">
            <a href="index.php"><h1>Raspi Alarm Clock</h1></a>
            <h2>Settings</h2>
            <?php
                // if there's an info message, print it
                if (isset($_GET['info'])) {
                    echo("<p>" . $_GET['info'] . "<p>");
                }
             ?>

            <form action="alarm_controller.php?action=save_settings" method="post">
                <label for="alarmtime">Volume: </label><input name="volume" id="volume" value="<?= $volume ?>" type="number"  step="0.1" required>
                <p>
                    <input type="submit" value="Save settings">
                </p>
            </form>

            <a href="index.php"><img src="images/icon-refresh-50.png" alt="back button"></a>

        </div>
    </div>
</body>
</html>
