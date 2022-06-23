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
                <input type="text" id="this-provide-text" placeholder="Posibility"/>
                <input type="range" oninput="thischangeProvideInput(event)" id="this-provide-range" value='100'  min='10' max='100'/>
                <input type="number" oninput="thischangeProvideInput(event)" id="this-provide-range-num" value ='100' min="10" max="100"/>
                <button onclick="thisAddPosibility()">Add</button>
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

        function thischangeProvideInput(e) {
            if (e.target.id == 'this-provide-range') {
                document.getElementById('this-provide-range-num').value = e.target.value;
            } else {
            document.getElementById('this-provide-range').value = e.target.value;
            }
        }
    </script>
</html>
