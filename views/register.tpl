%include header
%include navigaatio
%if viesti:
{{viesti}}
%end 
<form method="POST" action="/register">
  Tunnus: <input name="name" type="text" /> <br>
  Salasana: <input name="password1" type="password" /> <br>
  Salasana uudelleen: <input name="password2" type="password" />
  <input type="submit" value="rekisteröidy">
</form>
%include footer
