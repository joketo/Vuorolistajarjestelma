%include header
%include navigaatio
<p>Tässä voit lisätä uuden asiakkaan tietokantaan<p>
<a href="/lisaaVuoro">Tästä pääset määrittämään asiakkaan vuorot</a>

  <form method="POST" action="/asiakkaat">
    Nimi: <input name="nimi"     type="text" /><br>
    <input type="submit" value="luo uusi" />
  </form>
<p style = "color:green">Kantaan talletetut asiakkaat:</p>
<p>
  %for a in asiakkaat:
  {{a.nimi + ": " + ", ".join(a.kaynnit)}}<br>
  %end
</p>
%include footer

