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
    /* .jobbox {
      display: inline;
    } */
    #del_day {
      display: inline;
    }
    #add_day {
      display: inline;
    }
    /* #test {
      background-color: yellow;
    } */
    /* div {text-align: center;} */
  </style>

  <?php include("db.php"); ?>
  <script src="./p5/p5.min.js"></script>
 <!-- <script src="./p5/addons/p5.sound.js"></script> -->
  <!-- <script defer src=https://cdn.JsDelivr.net/npm/p5></script>
  <script defer src=https://cdn.JsDelivr.net/npm/p5/lib/addons/p5.dom.min.js></script>
  <script defer src=https://cdn.JsDelivr.net/npm/p5/lib/addons/p5.sound.min.js></script> -->
  <script src=deftabsketch.js></script>
  <script language="javascript">

  function insertarrayintohiddenformfield(){
    let values = [];
    for (let i=0; i<job_instances.length; i++){
      values.push(JSON.stringify(job_instances[i]));
    }
    console.log(values);
    document.Form.jobs.value = values;
  }

  </script>
  <?php

  $ar = $_POST['jobs'];
  $js = explode("}", $ar);
  $jobs = [];
  $jobobjs = [];
  if (isset($ar)){
    echo "PHP array \$jobs()<BR>";
  for ($i=0;$i<count($js);$i++){
    $j = json_encode($js[$i]);
    if (str_ends_with($j, 'false"') || str_ends_with($j, 'true"')){
      $j = rtrim($j, '"');
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
    array_push($jobs, $j);
  }
  for ($i=0; $i<count($jobs); $i++){
    echo $jobs[$i];
    echo "<BR>";
    array_push($jobobjs, json_decode($jobs[$i]));
  }
  echo "----_______----";
}
  ?>

</head>

<body>
  <a href="./index.php">Back to definitions</a>
  <div style='position:absolute;top:200px;left:450px'>
  <form name="Form" method="post" onsubmit="insertarrayintohiddenformfield()" action="tab.php">
  <input name='jobs' type=hidden>
  <input name="INSERT INTO DB" type="submit" value="INSERT INTO DB">

  </form>
  </div>

  <main>
  </main>

</body>
</html>
