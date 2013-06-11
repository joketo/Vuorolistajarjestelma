%include header
%for h in hoitajat:
{{h.nimi + ": " + ",".join(h.luvat)}} <br>
%end
<form method="POST" action="/hoitajat">
  Nimi: <input name="nimi"     type="text" /><br>
  Luvat: <input name="luvat" type="text" />
  <input type="submit" value="luo uusi" />
</form>
<a href="/">Etusivulle</a>
%include footer
