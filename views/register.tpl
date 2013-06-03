%include header
%include navigaatio 
<form method="POST" action="/register">
  Tunnus: <input name="name" type="text" /> <br>
  Salasana: <input name="password" type="password" />
  <input type="submit" value="rekisteröidy">
</form>
%include footer
