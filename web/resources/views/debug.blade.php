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
            <br>
            <div id="this-posibilities" class="flex vertical">
                
            </div>
        </div>
    </body>

    <script>
        function thisAddPosibility() {

            let provideText = document.getElementById('this-provide-text').value;
            let provideValue = document.getElementById('this-provide-range').value;

            let rangeInput, textInput, pdiv;
            let pChanceSum, pSum;

            var x = document.getElementsByClassName("this-chance-range");
            for(var i = 0; i<x.length; i++){
               pChanceSum += x[i].value;
            }

            document.getElementById('this-provide-range').setAttribute("max",(provideValue - pChanceSum));
            document.getElementById('this-provide-range').setAttribute("value",(provideValue - pChanceSum));

            document.getElementById('this-provide-range-num').setAttribute("max",(provideValue - pChanceSum));
            document.getElementById('this-provide-range-num').setAttribute("value",(provideValue - pChanceSum));

            var container = document.getElementById('this-posibilities');
            var div = document.createElement("div");
            div.className = "this-posibility flex";

            let p = document.createElement("p");
            p.innerText = provideText;

            var inputRange = document.createElement("input");
            inputRange.type = "range";
            inputRange.setAttribute("value",provideValue);
            div.className = "this-chance-range";

            var inputNum = document.createElement("input");
            inputNum.type = "number";
            inputNum.setAttribute("value",provideValue);

            var button = document.createElement("button");
            button.setAttribute("onclick",'closeParent(event)'); // "key-word-'+(count + 1)+'"
            button.innerText = "Delete";
            button.type="button";

            div.appendChild(p);
            div.appendChild(inputRange);
            div.appendChild(inputNum);
            div.appendChild(button);

            container.appendChild(div);
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
