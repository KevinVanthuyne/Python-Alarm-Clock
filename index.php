<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Alarm Clock</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">
    <style>
        body {
            margin: 0;
            font-family: 'Raleway', sans-serif;
        }

        #background {
            height: 100vh;
            width: auto;
            overflow: hidden;
            background-image: url(background-optimized-1920x1080.jpeg);
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-size: cover;
        }

        #wrapper {
            color: white;
            width: 70%;
            margin: 0 auto;
            padding: 1em;
            text-align: center
        }

        h1 {
            font-size: 4em
        }

        p, h1, label {
            text-shadow: 0 0 5px black;
        }

        p, label {
            font-size: 1.7em;
        }

        input {
            font-size: 1rem;
            font-family: 'Raleway', sans-serif;
        }

        input[type="submit"] {
            width: 200px
        }
    </style>
</head>
<body>

    <div id="background">
        <div id="wrapper">
            <h1>Raspi Alarm Clock</h1>
            <?php
                // if there's an info message, print it
                if (isset($_GET['info'])) {
                    echo("<p>" . $_GET['info'] . "<p>");
                }
            ?>
            <form action="alarm_controller.php" method="post">
                <label for="alarmtime">Alarm time: </label><input name="alarmtime" id="alarmtime" type="time" required >
                <p>
                    <input type="submit" name="send" value="Set alarm">
                </p>
            </form>
            <form action="alarm_controller.php" method="post">
                <p>
                    <input type="submit" name="send" value="Cancel alarm">
                </p>
            </form>
        </div>
    </div>
</body>
</html>
