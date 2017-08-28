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
        $alarm_folder = "/var/www/html/Python-Alarm-Clock/";

        // get settings from setting file
        $volume = 1;
        $max_time = 600;

        if (isset($_GET['volume'])) {
            $volume = $_GET['volume'];
        }
        if (isset($_GET['max_time'])) {
            $max_time = $_GET['max_time'];
        }

        // get sounds from played_sounds file
        $played_sounds = array();

        if (file_exists("played_sounds")) {
            // reads file into array of lines
            $played_sounds = file($alarm_folder . "played_sounds");
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

                <p><label for="max_time">Max playtime: </label><input name="max_time" id="max_time" value="<?= $max_time ?>" type="number" min="1" max="30" step="1" required> (min)</p>

                <p><input type="submit" value="Save settings"></p>
            </form>


            <h2>Played Sounds</h2>
            <?php
                if (empty($played_sounds)) {
                    echo("<p>No sounds found.</p>");
                }
                else {
                    echo("<ul>");
                    // echo every sound
                    foreach($played_sounds as $sound) {
                        echo("<li>" . $sound . "</li>");
                    }
                    echo("</ul>");
                }
             ?>

            <a href="index.php"><img src="images/icon-refresh-50.png" alt="back button"></a>

        </div>
    </div>
</body>
</html>
