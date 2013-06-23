%#from vakioita import paivat, ajat, kestot
<p>Lisää valitsemallesi asiakkaalle hoitokäynti</p>
<form method="POST" action="/lisaaVuoro">
    <select name="asiakas">
        <option value="ei valittu">--asiakas--</option>
        %for asiakas in asiakkaat:
        <option value="{{asiakas.asiakasid}}">{{asiakas.nimi}}</option>
        %end
    </select>
    <select name="paiva">
        <option value="ei valittu">--päivä--</option>
        %for pvm in paivat:
        <option value="{{pvm[0]}}">{{pvm[1]}}</option>
        %end
    </select>
    <select name="aika">
        <option value="ei valittu">--aika--</option>        
        %for aika in ajat:
        <option value="{{aika[0]}}">{{aika[1]}}</option>
        %end
    </select>
    <select name="kesto">
        <option value="ei valittu">--kesto--</option>
        %for kesto in kestot:
        <option value="{{kesto[0]}}">{{kesto[1]}}</option>
        %end
    </select><br>
    <p style = "color:green">Valitse lupavaatimukset käynnille</p>
        %for lupa in luvat:
        <input type="checkbox" name="lupa" value="{{lupa[0]}}">{{lupa[1]}}
        %end
        <br>
        <input type="submit" value="Lisää" />
</form>
