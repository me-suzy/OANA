# Integrate ChatBOT with CLAUDE.AI on your website (Step by step) - Second Method

ChatBOT-ul va citi urmatoarele taguri din fisierul html:

    <title>(.*?)</title>
    
    <link rel="canonical" href="(.?)" />
    
    <meta name="description" content="(.?)">
    
    <h1>(.?)</h1>
    
    <h1 class="custom-h1" itemprop="name">(.?)</h1>
    
    <h2 class="text_obisnuit2">(.?)</h2>
    
    <h3 class="text_obisnuit2">(.?)</h3>
    
    <p class="text_obisnuit">(.?)</p>
   
    <p class="text_obisnuit"><span class="text_obisnuit2">(.*?)</span> (.*?)</p>


# 1. Instalați Node.js:

Descărcați și instalați Node.js de la https://nodejs.org/

Verificați instalarea rulând în CMD comenzile:

node --version 

npm --version 


# 2. Creați un director pentru proiect. 
Puteti crea in mod simplu acest folder in care sa adaugati fisierele, sau puteti sa creati cu cmd, astfel:

mkdir chatbot-claudeai

cd chatbot-claudeai

# 3. Inițializați proiectul Node.js cu ajutorul CMD din acel folder:
npm init -y

# 4. Instalați dependențele necesare in CMD din acel folder:
npm install 

express cors

node-fetch

node-fetch@2 dotenv

# 5. Adaugati in folder fișierele necesare:

server.js

index.html

chatbot-script.js

.env

.gitignore

chatbot-style.css

package.json

# Mentiune: 

In fisierul .env adaugati urmatoarea linie:

CLAUDE_API_KEY=YOUR-API-KEY  (puneti al vostru api-key)

In fisierul .gitignore adaugati urmatoarele liniI:

node_modules/
   .env


# 5. Adăugați conținutul corespunzător în fiecare fișier (așa cum ați furnizat în atașamente).
Change API-KEY in fisierele urmatoare:

.env 

server.js


# 6. Rulați serverul in CMD din acel folder prin comanda:
node server.js

# 7. Accesați chatbot-ul:

Deschideți un browser web

Navigați la http://localhost:3000 

Se va deschide automat pagina index.html 

Introduceți un mesaj în caseta de chat

Apăsați butonul "Trimite" sau apăsați Enter

Verificați răspunsul primit de la Claude AI
