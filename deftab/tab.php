<?php
// Start the session
session_start();
?>

<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>schedule definition</title>
  <style>
    body {
      padding: 0;
      margin: 0;
    }
    h1 {text-align: center;}
    p {text-align: center;}
    .daybox {
      display: inline;
      padding: 100;

    }
    .day {
      padding: 100;
      margin: 100;
    }

  </style>

  <?php include("db.php"); ?>

  <?php
  $num_days = 0;
  $days = array();
  foreach($_GET as $key=>$val){
    if (str_starts_with($key, "day")){
      $days[substr($key, 3)] = $val;
      $num_days++;
    }
    else if (str_starts_with($key, "PREday")){
      $num_days++;
    }
  }
  ?>

  <script src="./p5/p5.min.js"></script>
 <!-- <script src="./p5/addons/p5.sound.js"></script> -->
  <!-- <script defer src=https://cdn.JsDelivr.net/npm/p5></script>
  <script defer src=https://cdn.JsDelivr.net/npm/p5/lib/addons/p5.dom.min.js></script>
  <script defer src=https://cdn.JsDelivr.net/npm/p5/lib/addons/p5.sound.min.js></script> -->
  <script src=deftabsketch.js></script>
  <script> make_day_instances(<?php echo json_encode($days); ?>); </script>

  <?php
    $pdo = connect();
    $sql = get_jobs_sql();
    $js = perform_query($pdo, $sql);
    // printf(json_encode($js));
    // printf(json_encode(count($js[0])));

    $jobs = [];
    foreach ($js as $j){
      $tmp = array();
      foreach ($j as $key=>$val){
        if (strlen($key) > 1){
          $tmp[$key] = $val;
          // printf($key." => ".$val);
          // printf("<br>");
          // printf("<br>");
        }
      }
      array_push($jobs, $tmp);
    }
  ?>
  <?php
    $jsjobs = json_encode($jobs);
    echo "<script> insert_predefined_jobs($jsjobs);</script>";
  ?>


  <script language="javascript">
  function insertarrayintohiddenformfield(){
    let day_values = [];
    let job_values = [];
    let jt_values = [];
    save_data();
    for (let i=0; i<days_arr.length; i++){
      day_values.push(JSON.stringify(days_arr[i]));
    }
    for (var [key, value] of jobtypes.entries()){
      jt_values.push(JSON.stringify(value));
    }
    for (let i=0; i<job_instances.length; i++){
      job_values.push(JSON.stringify(job_instances[i]));
    }
    console.log(job_values);
    console.log(job_instances);
    document.Form.days.value = day_values;
    document.Form.jobtypes.value = jt_values;
    document.Form.jobs.value = job_values;
  }
  </script>


<?php
// // WARNINGS
// ini_set('display_errors', 1);
// ini_set('display_startup_errors', 1);
// error_reporting(E_ALL);

  function process_postval($postar){
    $js = explode("}", $postar);
    $vals = [];
    if (isset($postar)){
      // echo count($js);
      for ($i=0;$i<count($js);$i++){
        $j = json_encode(utf8_encode($js[$i]));
        if (str_ends_with($j, '"') || str_ends_with($j, '"')){
          $j = substr($j, 0, -1);
        }
        if ($j[0] == '"'){
          $j = ltrim($j, '"');
        }
        if ($j[0] == ','){
          $j = ltrim($j, ',');
        }
        if ($j == ""){
          break;
        }
        $j = $j."}";
        $j = json_decode(stripslashes($j));
        array_push($vals, $j);
      }
      return $vals;
    }
  }

    $dayar = $_POST['days'];
    if (isset($dayar) && !$_SESSION["days_indb"]){
      $dayvals = process_postval($dayar);
      for ($i=0; $i<count($dayvals); $i++){
        $daysql = insert_day_sql($dayvals[$i]);
        if ($daysql != ""){
          echo "<br".$daysql;
          $pdo = connect();
          perform_query($pdo, $daysql);
          $pdo = null;
          $d = json_encode($dayvals[$i]);
          echo "<script>insert_day_indb($d);</script>";
        }
      }
      $_SESSION["days_indb"] = true;
      unset($_POST['days']);
    }

    // echo count($vals);
    $jtar = $_POST['jobtypes'];
    if (isset($jtar) && !$_SESSION["jts_indb"]){
      $jtvals = process_postval($jtar);
      for ($i=0; $i<count($jtvals); $i++){
        $jobsql = insert_jobtype_sql($jtvals[$i]);
        if ($jobsql != ""){
          echo $jobsql;
          $pdo = connect();
          perform_query($pdo, $jobsql);
          $pdo = null;
          $d = json_encode($jtvals[$i]);
          echo "<script>insert_jobtype_indb($d);</script>";
        }
      }
      $_SESSION["jts_indb"] = true;
      unset($_POST['jobtypes']);
    }

    $jar = $_POST['jobs'];
    if (isset($jar) && !$_SESSION["jobs_indb"]){
      $jvals = process_postval($jar);
      for ($i=0; $i<count($jvals); $i++){
        $jobsql2 = insert_job_sql($jvals[$i]);
        if ($jobsql2 != ""){
          printf("<br>".$jobsql2."<br>");
          $pdo2 = connect();
          perform_query($pdo2, $jobsql2);
          $d = json_encode($jvals[$i]);
          echo "<script>insert_job_indb($d);</script>";
        }
      }
      $_SESSION["jobs_indb"] = true;
      unset($_POST['jobs']);
    }
  // echo "----_______----";
  ?>

</head>

<body>
  <a href="./index.php">Back to definitions</a>
  <div style='position:absolute;top:500px;left:450px'>
    <?php
    for ($i=0; $i<$num_days; $i++){
      echo "<button type='button' onclick='create_dayview($i)'>DAY $i</button>";
    }
    ?>
    <button type="button" onclick="resume_default_view()">WHOLE VIEW</button>
  <form name="Form" method="post" onsubmit="insertarrayintohiddenformfield()" action="tab.php">
    <input name='days' type=hidden>
    <input name='jobs' type=hidden>
    <input name='jobtypes' type=hidden>
    <input name="INSERT INTO DB" type="submit" value="INSERT INTO DB">
  </form>
  </div>
  <main>
  </main>
  <?php
  if ($_SESSION["jobs_indb"]){
    echo "Geschafft.";
    echo "<script>unset_edit_mode();</script>";
  }
  ?>


</body>
</html>
