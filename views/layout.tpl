<!DOCTYPE html>
<html>
  <head>
    <title>
      Vuorolistajärjestelmä - {{otsikko}}
    </title>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="/static/style.css">
  </head>
  <body>
    <div class="container">
      %include ylapalkki otsikko=otsikko
      %include navigaatio
      <div class="content">
        %include
      </div>
      %include footer
    </div>
  </body>
</html>


