%include header
%include navigaatio
<p>Tässä voit lisätä uuden asiakkaan tietokantaan<p>
<p>Erottele luvat pilkulla. Tyhjä tarkoittaa luvatonta</p>

  <form method="POST" action="/asiakkaat">
    Nimi: <input name="nimi"     type="text" /><br>
    Luvat: <input name="luvat" type="text" />
    <input type="submit" value="luo uusi" />
  </form>
<p style = "color:green">Kantaan talletetut asiakkaat:</p>
<p>
  %for a in asiakkaat:
  {{a.nimi + ": " + ", ".join(a.luvat)}}<br>
  %end
</p>
%include footer

