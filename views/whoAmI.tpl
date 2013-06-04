%include header
%if islogged:
%include navigaatio
Olet kirjautunut sisään tunnuksella {{name}}
%else:
Et ole kirjautuneena sisään. </br>
<a href="/login">Kirjaudu sisään</a>
%end
%include footer
