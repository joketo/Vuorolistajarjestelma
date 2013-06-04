%include header
%include navigaatio
%if islogged:
Olet kirjautunut sisään tunnuksella {{name}}
%else:
Et ole kirjautuneena sisään.
%end
%include footer
