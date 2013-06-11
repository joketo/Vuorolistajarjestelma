%include header
%include navigaatio
<p>Tässä voit lisätä uuden hoitajan tietokantaan<p>
<p>Erottele luvat pilkulla. Tyhjä tarkoittaa luvatonta</p>
  <form method="POST" action="/hoitajat">
    Nimi: <input name="nimi"     type="text" /><br>
    Luvat: <input name="luvat" type="text" />
    <input type="submit" value="luo uusi" />
  </form>

</p><p style = "color:green">Kantaan talletetut hoitajat:</p>
<p>
  %for h in hoitajat:
  {{h.nimi + ": " + ", ".join(h.luvat)}}<br>
  %end
</p>
%include footer
