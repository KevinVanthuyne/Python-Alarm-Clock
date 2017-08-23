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
        $max_time = 600;

        if (isset($_GET['volume'])) {
            $volume = $_GET['volume'];
        }
        if (isset($_GET['max_time'])) {
            $max_time = $_GET['max_time'];
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
                <p><label for="volume">Volume: </label><input name="volume" id="volume" value="<?= $volume ?>" type="number" min="0" max="1" step="0.1" required></p>

                <p><label for="max_time">Maximum playtime: </label><input name="max_time" id="max_time" value="<?= $max_time ?>" type="number" min="1" max="30" step="1" required> (min)</p>

                <p><input type="submit" value="Save settings"></p>
            </form>

            <a href="index.php"><img src="images/icon-refresh-50.png" alt="back button"></a>

        </div>
    </div>
</body>
</html>
