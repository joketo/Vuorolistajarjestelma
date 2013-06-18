%setdefault('virheviesti', None)
%include virhe virheviesti=virheviesti

<h3>Rekisteröityminen</h3>
<form method="POST" action="/register">
  Tunnus: <input name="name" type="text" /> <br>
  Salasana: <input name="password1" type="password" /> <br>
  Salasana uudelleen: <input name="password2" type="password" />
  <input type="submit" value="rekisteröidy">
</form>

<a href="/">Etusivulle</a>
%rebase loginlayout otsikko="Rekisteröidy"