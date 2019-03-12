<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/html">

<head>
    <title> Witam na mojej stronie</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <link rel="stylesheet" href="/static/bundles/bootstrap/css/bootstrap.min.css" type="text/css"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js"
            integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4"
            crossorigin="anonymous"></script>
    <script src="/static/bundles/jquery/jquery.min.js"></script>
    <script src="/static/bundles/bootstrap/js/bootstrap.min.js"></script>
    <script src="/static/bundles/jquery/jquery.min.js"></script>
    <script src="/static/underscore-min.js"></script>
    <script src="/static/bundles/charts/Chart.bundle.js"></script>
    <script src="/static/backbone-min.js"></script>
    <script src="/static/deviceslist.js"></script>
    <style>
    	canvas{
		-moz-user-select: none;
		-webkit-user-select: none;
		-ms-user-select: none;
	}



    </style>
</head>

<body class="row">
<div class="container-fluid">
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark" id="uppernavbar">
        <a class="navbar-brand" href="#">
            <img src="/static/logo.png" alt="Logo" style="width:40px;" class="rounded-circle">
        </a>
    </nav>
    <br/>
    <div class="col-12">
        <div class="row">
            <div class="col-3" id="devices_list"></div>
            <div class="col-9">
                <div class="float-right" id="filtering"></div>
                <div class="" id="chart_holder"></div>
            </div>

        </div>
    </div>
</div>
</body>

</html>