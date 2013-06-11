%include header
<p>
  %for a in asiakkaat:
  {{a.nimi + ": " + ",".join(a.luvat)}}<br>
  %end
</p>Tässä voit lisätä uuden asiakkaan tietokantaan
<p>
  <form method="POST" action="/asiakkaat">
    Nimi: <input name="nimi"     type="text" /><br>
    Luvat: <input name="luvat" type="text" />
    <input type="submit" value="luo uusi" />
  </form>
  <a href="/">Etusivulle</a>
</p>
%include footer

