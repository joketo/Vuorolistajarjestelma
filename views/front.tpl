%include header
%include navigaatio
<div id="container" style="width:1000px">

<div id="header" style="background-color:#B5DCE8;">        
<h1 style="margin-bottom:0;">Vuorolistajärjestelmä</h1></div>

<div id="menu" style="background-color:#CEE8F0;height:100px;width:200px;float:left;">    
    <a href="/hoitajat">Hallitse hoitajia</a> <br>
    <a href="/asiakkaat">Hallitse asiakkaita</a> <br>
    <a href="/hoitovuorot">Muodosta vuorolista</a> <br>
    <a href="/logout">Kirjaudu ulos</a>
</div>

<div id="content" style="background-color:#E0FFFF;height:200px;width:1000px;float:left;">
    <a href ="/hoitajat"><img src= "/static/hallitsehoitajia.png" width="150" height="100"/></a>
    <a href ="/asiakkaat"><img src= "/static/hallitseasiakkaita.png" width="200" height="100" /></a>
</div>

<div id="footer" style="background-color:#FFA500;clear:both;text-align:center;">
Copyright © Meme-kissa</div>
<!--<img src="http://i.imgur.com/VzmnRZv.jpg"width="600" height="400" title="Meme"/>
<p style = "font-size: 30px; color:violet">motivaatioMeme!</p>-->
</div>
%include footer.tpl
