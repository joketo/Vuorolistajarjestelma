%setdefault('virheviesti', None)
%include virhe virheviesti=virheviesti

<p>Tässä voit lisätä uuden hoitajan tietokantaan<p>

  <form method="POST" action="/hoitajat">
    Nimi: <input name="nimi"     type="text" />
        %for lupa in luvat:
        <input type="checkbox" name="lupa" value="{{lupa[0]}}">{{lupa[1]}}
        %end
        
        <input type="submit" value="Lisää" />
    
  </form>
       

<p style = "color:green">Kantaan talletetut hoitajat:</p>
<p>
  %for h in hoitajat:
  %if h.luvat:
  {{h.nimi + ": " + ", ".join(h.luvat)}}<br>
  %else:
  {{h.nimi + ": ei lupia"}}<br>
  %end
  %end
</p>

%include poistaHoitaja hoitajat=hoitajat
%rebase layout otsikko="Hallitse hoitajia"
