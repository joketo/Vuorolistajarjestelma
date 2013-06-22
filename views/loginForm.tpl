
<h3>Tervetuloa Vuorolistajärjestelmään!</h3>
<h2>Kirjaudu sisään</h2>
%setdefault('virheviesti', None)
%include virhe virheviesti=virheviesti

<form method="POST" action="/login">
  Tunnus: <input name="name"     type="text" /><br>
  Salasana: <input name="password" type="password" />
  <input type="submit" value="Kirjaudu" />
</form>
<p>Etkö ole rekisteröitynyt?</p>
<a href="/register">Rekisteröidy täällä</a>
%rebase loginlayout otsikko="Kirjaudu"
