# [I-portalen](http://i-portalen.se)
## Innehåll
- [Sätt upp utvecklingsmiljön (Ubuntu 14.04)](#s-tt-upp-utvecklingsmilj-n-ubuntu-1404)
  - [Installera beroenden](#installera-beroenden)
  - [Installera Pycharm](#installera-pycharm)
  - [Skapa en virtuel miljö](#skapa-en-virtuel-milj)
  - [Klona ner gitprojektet](#klona-ner-gitprojektet)
  - [Installera beroenden till miljön](#installera-beroenden-till-milj-n)
  - [Ställ in Pycharm](#st-ll-in-pycharm)
- [Pycharm tips](#pycharm-tips)
- [Länkar](#l-nkar)
  

## Sätt upp utvecklingsmiljön (Ubuntu 14.04)
### Installera beroenden 

Kör följande kommandon:

```
sudo apt-get update
sudo apt-get install java-common openjdk-7-jdk mysql sqlite3 mysql-server git python-pip python-pip3 -y
sudo pip install virtualenvwrapper
sudo pip3 install virtualenvwrapper
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

### Ställ in Pycharm
1. Starta pycharm med `pycharm` från terminalen.
1. Öppna i-portalen projektet.
1. Öppna settings, __File->Settings...__
1. Under __>Project: i-portalen__ klickar du på __Project interpreter__ och sedan på kugghjulet i högra hörnet och väljer __Add Local__ i sökfältet klistrar ni in `~/.envs/i-portalen/bin/python` om den inte hittar så får du navigera till `/home/användarnamn/.envs/i-portalen/bin/` och klicka på `python` själv.
1. Klicka sedan på __>Languages & Frameworks__ i vänster menyn och sedan på django.
1. Kryssa i __Enable Django Support__ och fyll i följande:
  * Django project root: `~repos/i-portalen/iportalen`
  * Settings: `iportalen/settings.py`
  * Manage script: `manage.py`
1. Klicka sedan på OK.
1. Starta Django-servern med `Ctrl + Alt + R` och skriv `runserver`
1. __Happy coding__

## Pycharm tips
* Istället för att använda __Git__ terminalen kan man i menyn under __VCS->Git__ använda det inbyggda stödet i Pycharm.

Resten löser sig på vägen.


## Länkar
* Rekommenderad Django tutorial: https://docs.djangoproject.com/en/1.8/intro/install/
* Cheat Sheet: http://www.mercurytide.co.uk/media/resources/django-cheat-sheet-a4.pdf