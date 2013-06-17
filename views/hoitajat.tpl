%include header
%include navigaatio
%from vakioita import luvat
<p>Tässä voit lisätä uuden hoitajan tietokantaan<p>

  <form method="POST" action="/hoitajat">
    Nimi: <input name="nimi"     type="text" />
        %for lupa in luvat:
        <input type="checkbox" name="lupa" value="{{lupa}}">{{lupa}}
        %end
        
        <input type="submit" value="Lisää" />
    
  </form>
       

<p style = "color:green">Kantaan talletetut hoitajat:</p>
<p>
  %for h in hoitajat:
  {{h.nimi + ": " + ", ".join(h.luvat)}}<br>
  %end
</p>
%include footer
