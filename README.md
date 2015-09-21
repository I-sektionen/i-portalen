# [I-portalen](http://i-portalen.se)
## Innehåll
- [Sätt upp utvecklingsmiljön (Ubuntu 14.04)](#s-tt-upp-utvecklingsmilj-n-ubuntu-14-04)
  - [Installera beroenden](#installera-beroenden)
  - [Installera Pycharm](#installera-pycharm)
  - [Skapa en virtuel miljö](#skapa-en-virtuel-milj)
  - [Klona ner gitprojektet](#klona-ner-gitprojektet)
  - [Installera beroenden till miljön](#installera-beroenden-till-milj-n)
  - [Konfigurera din lokala databas](#konfigurera-din-lokala-databas)
  - [Ställ in Pycharm](#st-ll-in-pycharm)
- [Sätt upp miljö på Mac (pycharm)](#satt-upp-utvecklingsmilj-p-mac)
- [Pycharm tips](#pycharm-tips)
- [Länkar](#l-nkar)
  
 
## Sätt upp utvecklingsmiljön (Ubuntu 14.04)
### Installera beroenden 

Kör följande kommandon:

```Bash
sudo apt-get update
sudo apt-get install java-common openjdk-7-jdk sqlite3 git python-pip python3-pip npm nodejs-legacy libmysqlclient-dev -y
sudo apt-get install mysql-server-5.6 -y
sudo pip install virtualenvwrapper
sudo pip3 install virtualenvwrapper
sudo npm install -g bower
```

Skapa sedan en mapp ".envs" i din hemmapp genom kommandot `mkdir ~/.envs` i terminalen. 
 
Öppna __.bash_aliases__ förslagsvis i terminalen med `nano .bash_aliases` och klistra in följande:
```
export WORKON_HOME=~/.envs
source /usr/local/bin/virtualenvwrapper.sh
```

Stäng terminalen och öppna en ny när du sparat det för att läsa in ändringarna.

### Installera Pycharm
  1. Skapa studentkonto och ladda ner Pycharm från: https://www.jetbrains.com/student/
  1. Extrahera mappen på valfritt ställe förslagsvis i en mapp "program" i hemmappen
  1. Navigera till mappen bin i pycharm och kopiera sökvägen.
  1. Öppna __.bash_aliases__ förslagsvis i terminalen med `nano .bash_aliases`. och klistra in följande, glöm inte att ändra sökvägen till pycharm om ni sparat den någon annan stans: `alias pycharm='sh ~/program/pycharm/bin/pycharm.sh'`  

### Skapa en virtuel miljö

Skapa en virtualenv med: `mkvirtualenv --python=/usr/bin/python3 i-portalen`
  
Använd sedan `workon i-portalen` för att öppna miljön och `deactivate` för att stänga den.

### Klona ner gitprojektet
1. Skapa en mapp: `mkdir ~/repos`
1. Navigera in i mappen: `cd ~/repos`
1. Klona projektet*: `git clone git@gitlab.ida.liu.se:isaek808/i-portalen.git`  
  *Fungerar det inte har du förmodligen inte lagt in din sshnyckel:
     1. `ssh-keygen -t rsa -C "$your_email"`
     2. `cat ~/.ssh/id_rsa.pub`
     3. Kopiera nyckeln och klistra in här: https://gitlab.ida.liu.se/profile/keys/new
1. Checka ut lämplig branch ex. `git checkout development`

### Installera beroenden till miljön
```
workon i-portalen
cd ~/repos/i-portalen/
pip install -r requirements.txt
```

### Konfigurera din lokala databas
1.  Starta mysql i en terminal: `mysql -u root -p`
2.  Skriv in ditt lösenord och logga in.
3.  Skapa databasen: `CREATE DATABASE django_iportalen CHARACTER SET UTF8;`
4.  Skapa en mysql användare med rätt behörigheter:
```
CREATE USER '<namn>'@'localhost' IDENTIFIED BY '<lösenord>';
GRANT ALL PRIVILEGES ON django_iportalen.* TO <namn>@localhost;
GRANT ALL PRIVILEGES ON test_django_iportalen.* TO <namn>@localhost;
```
*OBS: <namn> och <lösenord> som står i koden ovan måste bytas ut till något godtyckligt. Dock utan mellanslag i namn eller lösenord!

5.  Kopiera filen `i-portalen/wsgi/iportalen_django/iportalen/mysql_credentials.example` och spara den nya som `i-portalen/wsgi/iportalen_django/iportalen/mysql_credentials`
    Skriv in valt namn och lösenord (alltså <namn> och <lösenord> ovan) i den nya filen och se till att ta bort det som är skrivet så att filen blir på formen:
    ```
    host localhost
    port 3306
    user django_iportalen
    password top_secret_password
    ```

6.  Migrera din databas. Hitta filen manage.py. Se därefter till att ha aktiverat din python miljö i terminalen du arbetar i (`workon i-portalen`). Skriv sedan:
    ```python managey.py migrate```
    Då skapas alla tabeller och relationer i databasen.

7.  Om du vill kan du skapa en superanvändare på din lokala miljö:
    ```python manage.py createsuperuser```
    Följ instruktionerna. 
    

### Ställ in Pycharm
1. Starta pycharm med `pycharm` från terminalen.
1. Öppna i-portalen projektet.
1. Öppna settings, __File->Settings...__
1. Under __>Project: i-portalen__ klickar du på __Project interpreter__ och sedan på kugghjulet i högra hörnet och väljer __Add Local__ i sökfältet klistrar ni in `~/.envs/i-portalen/bin/python` om den inte hittar så får du navigera till `/home/användarnamn/.envs/i-portalen/bin/` och klicka på `python` själv.
1. Klicka sedan på __>Languages & Frameworks__ i vänster menyn och sedan på django.
1. Kryssa i __Enable Django Support__ och fyll i följande:
  * Django project root: `~repos/i-portalen/wsgi/iportalen_django`
  * Settings: `iportalen/settings.py`
  * Manage script: `manage.py`
1. Klicka sedan på OK.
1. Starta Django-servern med `Ctrl + Alt + R` och skriv `runserver`
1. __Happy coding__

TODO: Updatera ovan, test måste köras med `option:` ``-t ..`` 

## Sätt upp utvecklingsmiljö på Mac

### Installera homebrew
1. Ladda ner homebrew genom att köra följande rad i terminalen  
``` bash
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
1. I terminalen: ``brew update``
1. Kör också en `` brew doctor `` för att kolla om något gått verkligt snett. Är det bara `` warning `` brukar det vara lugnt.

### Installera python 3
`` brew install python3 ``
### Ladda ner Pycharm
Följ instruktionerna ovan

### Klona ner projektet
Följ instruktionerna ovan

### Konfigurera din lokala databas
1. I terminalen skriv ``brew install mysql``
2. Start din mysql server genom att skriva ``mysqld`` i terminalen. Detta fönster går nu att stänga, trots att den klagar på att process ska stängas. (Du kommer att behöva starta din mysql server med ``mysqld`` varje gång du har startat om din dator)
3. Följ sedan instruktionerna ovan.

### Skapa virtuell miljö
1. Starta Pycharm och öppna projektet (repot) genom ``File > Open``
2. Öppna ``Preferences ⌘, `` för Pycharm
3. Välj `` Project [namn på repot] -> Project interpreters ``
4. Klicka på kugghjulet vid `` Project interpreter `` och välj `` Create virtualenv ``
5. Ge miljön ett namn tex. `` iportalen_virtualEnv `` och väl `` base interpreter `` till `` python 3.x ``
6. När det är klart: se till att `` pip `` och `` setuptools `` finns med i din interpreter
7. Öppna valfri fil i projektet, t.ex. setup.py och tryck på "Install Requirments" som kommer upp som en gul popup

### Om mysqlclient inte går att installer och den klagar på att den inte hittar mysql_config
1. Starta terminalen och skriv ``which mysql_config``, du borde få ut något som är typ ``/usr/local/bin/mysql_config``, skriv då ner detta utan mysql_config, så i detta fall spara ``/usr/local/bin``
2. Ta dig till din virtuella miljö i repot med hjälp av ``cd``, hitta dig in till filen ``activate``, brukar ligga i ``/usr/i-portalenblabla/bin/activate``
3. Redigera denna filen i nano genom att skriva ``nano activate``
4. Ta dig ned till följande den i filen:
```
_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH
```
Lägg där till ``PATH="$PATH:/usr/local/bin/"`` innan ``export PATH``. Spara filen genom ctrl+o och enter och gå ur nano med ctrl+x.
5. Starta virtuella miljön genom terminalen med ``source activate``
6. Skriv ``pip install mysqlclient`` för att installera mysqlclient manuellt
7. Avaktivera din virtuella miljö med ``deactivate``
8. Dubbelkolla i PyCharm att din virtuella miljö nu har ``mysqlclient`` installerat

### Configurera django och fixa en lokal server

1. Öppna `` Preferences ⌘, `` för Pycharm
2. Välj `` languages and framwork ``
3. Välj Django och välj följande inställningar. Avsluta med OK:
    - Django project root: `~repos/i-portalen/iportalen`
    - Settings: `iportalen/settings.py`
    - Manage script: ``manage.py``
4. Klicka på dropdown menyn uppe i högra hörnet bredvid play-symbolen och väl `` Edit configurations ``
5. Välj ``+`` sedan ``Django server``
6. Fyll i enligt:
    * Name : `` iportalen ``
    * Interpreter: `` iportalen_virtualEnv ``
    * Working directory: `` /Users/<user>/repos/i-portalen/iportalen ``
7. Klicka på `` Play `` för att kolla om allt fungerar

## Pycharm tips
* Istället för att använda __Git__ terminalen kan man i menyn under __VCS->Git__ använda det inbyggda stödet i Pycharm.

Resten löser sig på vägen.


## Statiskt innehåll
Javascript, css och annat statiskt innehåll kan läggas till genom att i appen det statiska tillhör så skapas en undermapp 'static' i den läggs ytterligare en mapp med samma namn som appen. Tex: `event/static/event`. Statiskt innehåll som inte hör till någon speciell app kan läggas direkt i wsgi/static. 


## Länkar
* Rekommenderad Django tutorial: https://docs.djangoproject.com/en/1.8/intro/install/
* Cheat Sheet: http://www.mercurytide.co.uk/media/resources/django-cheat-sheet-a4.pdf
 
