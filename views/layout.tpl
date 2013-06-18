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
    <div id="container">
      %include ylapalkki otsikko=otsikko
      %include navigaatio
      <div id="content">
        %setdefault('virheviesti', None)
        %include virhe virheviesti=virheviesti
        %include
      </div>
      %include footer
    </div>
  </body>
</html>


