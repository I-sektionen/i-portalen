### mysql_credentials
En fil som används i lokala utvecklingsmiljöer (ej Jenkins eller Openshift) där 
användar uppgifter till mysql skrivs ned. Formen måste vara:

```
password losenord
user anvandare
host localhost
port 3306
```

Annars kommer get_mysql_credentials i helpers.py sluta att fungera.

Filen är lagd i .gitignore så att ändringar ska ignoreras och användaruppgifter inte råkas pushas upp. 