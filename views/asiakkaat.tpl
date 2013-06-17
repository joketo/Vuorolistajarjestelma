<p>Tässä voit lisätä uuden asiakkaan tietokantaan<p>
  <form method="POST" action="/asiakkaat">
    Nimi: <input name="nimi"     type="text" /><br>
    <input type="submit" value="luo uusi" />
  </form>
<p style = "color:green">Kantaan talletetut asiakkaat:</p>
<p>
  %for a in asiakaslista:
  {{a.nimi + ": " + "; ".join([str(k) for k in a.kaynnit])}}<br>
  %end
</p>

