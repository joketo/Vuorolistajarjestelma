<form method="POST" action="/poistaHoitaja">
  <select name="poistettava">
    %for hoitaja in hoitajat:
    <option value="{{hoitaja.nimi}}">{{hoitaja.nimi}}</option>
    %end
  </select>
  <input type="submit" value="Poista" />
</form>
