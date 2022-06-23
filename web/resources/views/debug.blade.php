<!DOCTYPE html>
<html>
    <head>
        <title> Wild West Post Office | Manage</title>
	    <link rel="stylesheet" type="text/css" href="/assets/css/app.css" />
	    <script type="text/javascript" src="/assets/js/app.js"></script>
	    <meta name="description" content="Main site featuring Discord multi-task bot Wild West Post Office!" />
	    <meta name="keywords" content="discord, bot" />
	    <meta name="author" content="Lukas" />
	    <meta charset="UTF-8" />
	    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <style>
        #this-random-picker {
            width: 100%;
            height: 100%;
        }
    </style>
    <body>
        DEBUGGING
        <div id="this-random-picker">
            <div class="flex">
                <input type="text" id="this-provide-text" placeholder="Thing to random"/>
                <input type="range" id="this-provide-range" value='100'  min='10' max='100'/>
                <button onclick="thisAddPosibility()">Add posibility</button>
            </div>
            <div id="possibilities">
                
            </div>
        </div>
    </body>

    <script>
        function thisAddPosibility() {
            let rangeInput, textInput, pdiv;
            let pChanceSum, pSum;
        }
    </script>
</html>
