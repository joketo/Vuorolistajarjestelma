%include header
%include navigaatio
<p>Lisää valitsemallesi asiakkaalle hoitokäynti</p>
<form action="">
    <select name="asiakas">
    %for asiakas in asiakkaat:
    <option value="{{asiakas}}">{{asiakas}}</option>
    %end
</select>
</form>
%include footer
