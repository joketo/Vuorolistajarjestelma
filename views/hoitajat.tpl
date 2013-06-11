%include header
<p>
  %for h in hoitajat:
  {{h.nimi + ": " + ",".join(h.luvat)}}<br>
  %end
</p>
<p>
  <form method="POST" action="/hoitajat">
    Nimi: <input name="nimi"     type="text" /><br>
    Luvat: <input name="luvat" type="text" />
    <input type="submit" value="luo uusi" />
  </form>
  <a href="/">Etusivulle</a>
</p>
%include footer
