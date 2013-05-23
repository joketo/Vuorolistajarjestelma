%#ottaa listan hoitajat ja listan asiakkaat
%#muodostaa taulukon siitä, keillä kaikilla asiakkailla kukin hoitaja voi käydä
<table>
%for i in hoitajat:
    <tr>
        <td>{{i}}</td>
%for a in potilaat:
%if rand():            
        <td>{{a}}</td>
%end
%end
    </tr>

%end
</table>	
<!--            
<html>
    <body>
        <table>
            <tr>
                <td>One</td>
            </tr>
            <tr>
                <td>Two</td>
            </tr>
            <tr>
                <td>Three</td>
            </tr>
        </table>
    </body>
</html>
-->
