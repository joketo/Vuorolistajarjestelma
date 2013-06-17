%include header

%include navigaatio
<div id="container">

  <div id="header" style="background-color:#B5DCE8;">        
    <h1 style="margin-bottom:0;">Vuorolistajärjestelmä</h1></div>

  <div id="menu" style="background-color:#E0FFFF;width:200px;float:left;">
    <a href ="/hoitajat"><img src= "/static/hallitsehoitajia.png" width="160" height="102"/></a>
    <a href ="/asiakkaanHallinta"><img src= "/static/hallitseasiakkaita.png" width="160" height="102" /></a>
    <a href="/logout">Kirjaudu ulos</a>
  </div>

  <div id="content" style="background-color:#E0FFFF;height:320px;"><br>
    
    <a href ="/hoitovuorot"><img src= "/static/muodostalista.png" width="500" height="164"/></a><br>
    <img src="http://i.imgur.com/VzmnRZv.jpg"width="600" height="400" title="Meme"/>
    <p style = "font-size: 30px;
    color:violet">
  </div>

  <div id="footer" style="background-color:#FFA500;clear:both;text-align:center;">
    Copyright © Meme-kissa</div>

</div>
</marquee>
%include footer.tpl
