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
    }
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

  <script src="./p5/p5.min.js"></script>
  <script src=def.js></script>
</head>
<body>
  <?php
    echo "hello";
  ?>
  <!-- <div id="test">Test</div> -->
  <div id="definition">
  <div class="day">
    <div id="add_day"><button type="button" onclick="create_daybox();">+</button></div>
    <div id="del_day"><button type="button" onclick="delete_daybox();">-</button><br></div>
  </div>
  <div id="job">
    <div id="add_job"><button type="button" onclick="create_jobbox();">+</button><br></div>
  </div>

  <div id="savebtn"><button type="submit" onclick="write_to_file();">SAVE</button><br></div>

</div>
<div id="hide"><button id="hidebtn" onclick="hide_it()">HIDE DEFINITIONS</button></div>
<!-- <div id="Create Table"><button id="create_tab_btn" onclick="hide_it()">HIDE DEFINITIONS</button></div> -->
<!-- <a href="https://www.google.com/">Google Search</a>
<a href="https://www.tutorialrepublic.com/">Tutorial Republic</a>
<a href="images/kites.jpg">
    <img src="kites-thumb.jpg" alt="kites">
</a> -->
<a href="./tab.html">TABLE</a>
<main>
</main>
  <!-- <div>
    <form action="" method="GET">
      <fieldset>
        <label>
          <select name="sendfinal" size="1">
            <option value="save.py">Jep, abschicken. </option>
            <option value="no">Nope, noch nicht abschicken.</option>
          </select>
        </label>
        <input type="submit" value="Alles bestätigen"/>
      </fieldset>
    </form>
  </div> -->


</body>

</html>
