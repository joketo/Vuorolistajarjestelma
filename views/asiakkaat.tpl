%include header
<form method="POST" action="/hoitajat">
  Nimi: <input name="name"     type="text" /><br>
  Luvat: <input name="password" type="text" />
  <input type="submit" value="luo uusi" />
</form>
<a href="/">Etusivulle</a>
%include footer
