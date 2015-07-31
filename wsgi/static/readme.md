# Front-end environment

> Innhåller dokumentation för hur front end-utveckling görs på I-portalen. Kort sammanfattat utgörs det av Sass, Grunt och jQuery

## Innehåll
- [Grunt-kommandon](#grunt---kommandon)
- [Installation](#installation)  
     - [Node](#node)
     - [Node package manager](#node-package-manager)
     - [Grunt](#grunt)
     
## Grunt-kommandon

+ Komplilera JS & sass, starta en 'watch' med

````bash
    grunt
````
+ Kompilera och minifiera alla filer och spara till `/dist`
````bash
grunt dist
````

## Installation

### Node
Ladda ner och installera [NodeJS](https://nodejs.org "Node JS")

### Node package manager (NPM)
Följer med NodeJS. Efter installation av NodeJS kan du kontrollera och uppgradera till senaste versionen med:   

```Bash
sudo npm install npm -g.

```

### Grunt
Installera en global version av Grunt's Command Line Interface (CLI)

````Bash
npm install -g grunt-cli
````

### Package dependencies
NPM använder sig av en fil som heter `package.json` för konfiguration. Där finns lite information om projektet och vilka paket som projektet beror av. Denna gör det enkelt att lokalt installera alla de paket som krävs för projektet.

För att installera de moduler som finns definerade i `package.json` skriver man

````Bash
npm install
````

Vill du installera egna moduler görs detta genom kommandot
````Bash
npm install <module> --save-dev
````

Detta lägger också till paketet till devDependencies i `package.json`

## CSS & SASS
För att vår CSS ska bli lätt att underhålla används en pre-processor som heter SASS. När man använder SASS skriver man SASS/SCSS-syntax som sedan genom någon typ av magi översätts till vanlig CSS som alla webbläsare kan förstå. Denna magi gör det möjligt att deklarera variabler, göra egna funktioner och använda "nesting" och massor av andra bra grejer.  

För att använda SASS krävs följande är det lästtast att läsa instruktionerna på [Sass](http://sass-lang.com "SASS hemsida"). Där finns också dokumentation.

### Annat
Utöver ren SASS används också  
+ Ett mixin-bibliotek som heter [Bourbon](http://bourbon.io "Bourbon")
## JS & jQuery  
Inga konstigheter här än så länge.