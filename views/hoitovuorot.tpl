%include header
%include navigaatio
<p>tänne tulee näkymä jaetuista vuoroista hoitajittain</p>

<table border="2">
<tr>
  <td><b>hoitaja</b></td>
  <td><b>hoidettavat</b></td>  
</tr>
<tr>
%for h in hoitajat:
  <td>{{h}}</td>
  <td>  
  {{", ".join([a.nimi for a in hoitajat[h]])}}
  </td>  
</tr>
%end
</table>

%include footer
