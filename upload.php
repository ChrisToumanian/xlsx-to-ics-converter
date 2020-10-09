<?php
    error_reporting(-1);
    ini_set('display_errors', 'On');

    $target_dir = "/var/www/ott/calendar/uploads/";
    $file_name = $_FILES["fileToUpload"]["name"];
    $uploadOk = 0;
    $fileType = strtolower(pathinfo($target_dir . $file_name, PATHINFO_EXTENSION));
    $employees = "";
	$employee_list = [];
	$ics_filename = explode(".", $file_name)[0];
	$separate_files = true;
	$label = "";

	function downloadFile($file, $name) {
		header("Cache-Control: public");
		header("Content-Description: File Transfer");
		header("Content-Disposition: attachment; filename=$name");
		header("Content-Length: ".filesize($file));
		header("Content-Type: application/force-download");
		header("Content-Transfer-Encoding: binary");
		readfile($file);
	}

	// Check if calendars should be combined
	if (isset($_POST["combine"]) && $_POST["combine"] == "yes") {
		$separate_files = false;
	}
	
	// Check label
	if (isset($_POST["label"]) && $_POST["label"] != "") {
		$label = $_POST["label"];
	}

    // Check if file is csv
    if (isset($_POST["submit"])) {
        // Allow certain file formats
        if ($fileType == "csv" || $fileType == "xlsx") {
            $uploadOk = 1;
		}
	}

    // Upload file
    if ($uploadOk) {
        if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_dir . $file_name)) {

			// Convert XLSX to CSV
			if ($fileType == "xlsx") {
				$command_text = '/var/www/ott/calendar/convert_xlsx_to_csv.py ' . $target_dir . $file_name;
				$command = escapeshellcmd($command_text);
				$output = shell_exec($command);
				$file_name = explode(".", $file_name)[0] . ".csv";
			}

            // employees
            if (isset($_POST["employees"])) {
                $employee_list = explode(",", $_POST["employees"]);
                foreach ($employee_list as &$employee) {
                    $employees = $employees . ' -e "' . $employee . '"';
					$ics_filename = $ics_filename . "-" . str_replace(' ', '_', $employee);
                }
				$ics_filename = $ics_filename . ".ics";
            }

			// convert & download
			if (!$separate_files) {
				$command_text = '/var/www/ott/calendar/readschedule.py' . ' -i ' . $target_dir . $file_name . $employees . ' -o "' . $target_dir . $ics_filename . '" -l "' . $label . '"';
            	$command = escapeshellcmd($command_text);
            	$output = shell_exec($command);
            	unlink($target_dir . $file_name);
				downloadFile('uploads/' . $ics_filename, $ics_filename);
			} else {
				// create zip
				$zipname = $ics_filename . '.zip';
				$zip = new ZipArchive;
				$zip->open($zipname, ZipArchive::CREATE);

				// create ics for each employee
				foreach ($employee_list as &$employee) {
					$ics_filename = explode(".", $file_name)[0] . "-" . str_replace(' ', '_', $employee) . ".ics";
					$command_text = '/var/www/ott/calendar/readschedule.py' . ' -i ' . $target_dir . $file_name . ' -e "' . $employee . '" -o "' . $target_dir . $ics_filename . '" -l "' . $label . '"';
					$command = escapeshellcmd($command_text);
					$output = shell_exec($command);
					$zip->addFile('uploads/' . $ics_filename, $ics_filename);
				}

				// wrap-up zip and download file
				$zip->close();
				downloadFile($zipname, $zipname);

				// clean up files in uploads folder
				$files = glob('uploads/*'); // get all file names
				foreach($files as $file){
					if(is_file($file))
						unlink($file);
				}

				unlink($zipname);
			}
        } else {
           echo "Sorry, there was an error uploading your file.";
        }
	}
?>
