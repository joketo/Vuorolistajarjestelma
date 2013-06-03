%include header
%if viesti:
{{viesti}}
%end
<h3>Tervetuloa Vuorolistajärjestelmään!</h3>
<h2>Kirjaudu sisään</h2>
<form method="POST" action="/login">
  Tunnus: <input name="name"     type="text" /><br>
  Salasana: <input name="password" type="password" />
  <input type="submit" value="Kirjaudu" />
</form>
<p>Etkö ole rekisteröitynyt?</p>
<a href="/register">Rekisteröidy täällä</a>
%include footer
