<!DOCTYPE html>
<html>
<head>
	<title>FanDuel OTT Dashboard</title>
	<link rel="stylesheet" href="./includes/login-form.css">
	<link rel="shortcut icon" href="images/favicon.ico" />

	<script>
		function enableSubmit() {
			document.getElementById("submit").disabled = false;
		}
	</script>
</head>
<body>

	<div style="padding:0px;">

    <h4>ICS Converter</h4>

    <form action="calendar/upload.php" method="post" enctype="multipart/form-data">

        <h5>Label</h5>
        <input type="text" value="" name="label" id="label" style="width:620px;"><br>

        <h5>Select employee(s)</h5>
        <input type="text" value="Dean Humphus,David Crown,David Leonardson,Chris Toumanian" name="employees" id="employees" style="width:620px;"><br>
		<input type="checkbox" id="combine" name="combine" value="yes">
		<label for="combine"> Combine into single calendar</label><br>

		<h5>Select an XLSX or CSV schedule to upload</h5>
		<input class="file" type="file" name="fileToUpload" id="fileToUpload" style="width:620px;"><br><br>

        <input class="button" id="submit" type="submit" value="Upload" name="submit" disabled=true>

    </form>

	<script>
	document.getElementById('fileToUpload').addEventListener('change', () => {
		document.getElementById("submit").disabled = false;
	});
	</script>

	</div>

</body>
</html>
