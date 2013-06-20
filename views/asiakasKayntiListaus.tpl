<p style = "color:green">Kantaan talletetut asiakkaat käynteineen:</p>

%for a in asiakaslista:
<p>
  <h3>{{a.nimi}}:</h3>
  %for kaynti in a.kaynnit:
  <ul>
    <li>{{kaynti}}</li>        
  </ul>
  %end
</p>
%end
