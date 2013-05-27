%include header
%include navigaatio 
<form method="POST" action="/login">
  Name: <input name="name"     type="text" /><br>
  Password: <input name="password" type="password" />
  <input type="submit" value="Login" />
</form>
%include footer
