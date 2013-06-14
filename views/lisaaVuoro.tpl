%include header
%include navigaatio
%from vakioita import paivat, ajat, kestot, luvat
<p>Lisää valitsemallesi asiakkaalle hoitokäynti</p>
<form action="">
    <select name="asiakas">
        <option value="ei valittu">--asiakas--</option>
        %for asiakas in asiakkaat:
        <option value="{{asiakas}}">{{asiakas}}</option>
        %end
    </select>
    <select name="pvm">
        <option value="ei valittu">--pvm--</option>        
        %for pvm in paivat:
        <option value="{{pvm}}">{{pvm}}</option>
        %end
    </select>
    <select name="ajankohta">
        <option value="ei valittu">--ajankohta--</option>        
        %for aika in ajat:
        <option value="{{aika}}">{{aika}}</option>
        %end
    </select>
    <select name="kestot">
        <option value="ei valittu">--kesto--</option>
        %for kesto in kestot:
        <option value="{{kesto}}">{{kesto}}</option>
        %end
    </select><br>
    <p style = "color:green">Valitse lupavaatimukset käynnille</p>
        %for lupa in luvat:
        <input type="checkbox" name="lupa" value="{{lupa}}">{{lupa}}<br>
        %end 
</form>
%include footer
