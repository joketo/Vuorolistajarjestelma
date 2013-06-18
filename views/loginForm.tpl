
<h3>Tervetuloa Vuorolistajärjestelmään!</h3>
<h2>Kirjaudu sisään</h2>
%if viesti:
<p style="color: red; font-size:12px">{{viesti}}</p>
%end


<form method="POST" action="/login">
  Tunnus: <input name="name"     type="text" /><br>
  Salasana: <input name="password" type="password" />
  <input type="submit" value="Kirjaudu" />
</form>
<p>Etkö ole rekisteröitynyt?</p>
<a href="/register">Rekisteröidy täällä</a>
%rebase loginlayout otsikko="Kirjaudu"
