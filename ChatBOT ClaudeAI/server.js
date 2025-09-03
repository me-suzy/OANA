const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');
const path = require('path');
const fs = require('fs');
const cheerio = require('cheerio');

const app = express();
const port = 3000;

// Middleware pentru logging
app.use((req, res, next) => {
    console.log(`Request for: ${req.url}`);
    next();
});

// Configurare CORS
app.use(cors({
    origin: 'http://localhost:3000'
}));

// Middleware pentru parsare JSON și servire fișiere statice
app.use(express.json());
app.use(express.static(__dirname));

const CLAUDE_API_KEY = 'YOUR-API-KEY';

// Funcție pentru extragerea informațiilor din HTML
function extractInfoFromHTML(filePath) {
    const html = fs.readFileSync(filePath, 'utf8');
    const $ = cheerio.load(html);
    
    // Extragem conținutul dintre comentariile ARTICOL START și ARTICOL FINAL
    const articleContent = html.split('<!-- ARTICOL START -->')[1].split('<!-- ARTICOL FINAL -->')[0];
    const $article = cheerio.load(articleContent);
    
    return {
        title: $('title').text().trim(),
        canonical: $('link[rel="canonical"]').attr('href'),
        description: $('meta[name="description"]').attr('content'),
        h1: $('h1').first().text().trim(),
        customH1: $('h1.custom-h1[itemprop="name"]').text().trim(),
        h2: $article('h2.text_obisnuit2').text().trim(),
        h3: $article('h3.text_obisnuit2').text().trim(),
        textObisnuit2: $article('p.text_obisnuit span.text_obisnuit2').map((i, el) => $(el).text().trim()).get().join(' '),
        textObisnuit: $article('p.text_obisnuit').map((i, el) => {
            // Păstrăm conținutul tuturor sub-tagurilor, inclusiv span și em
            return $(el).text().trim();
        }).get().join(' ')
    };
}

// Rută pentru pagina principală
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Rută pentru obținerea informațiilor despre o pagină
app.get('/page-info', (req, res) => {
    console.log("Received request for page info:", req.query.page);
    const pagePath = path.join(__dirname, req.query.page);
    console.log("Full path:", pagePath);
    if (fs.existsSync(pagePath)) {
        console.log("File exists, extracting info");
        try {
            const pageInfo = extractInfoFromHTML(pagePath);
            console.log("Page info extracted:", pageInfo);
            res.json(pageInfo);
        } catch (error) {
            console.error("Error extracting page info:", error);
            res.status(500).json({ error: "Error extracting page info" });
        }
    } else {
        console.log("File not found");
        res.status(404).send('Pagina nu a fost găsită');
    }
});

// Rută pentru procesarea mesajelor chat
app.post('/chat', async (req, res) => {
    try {
        console.log('Received request body:', req.body);

        const systemMessage = req.body.messages.find(msg => msg.role === 'system');
        const userMessages = req.body.messages.filter(msg => msg.role !== 'system');

        const response = await fetch('https://api.anthropic.com/v1/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': CLAUDE_API_KEY,
                'anthropic-version': '2023-06-01'
            },
            body: JSON.stringify({
                model: "claude-2.1",
                max_tokens: 1000,
                system: systemMessage ? systemMessage.content : "",
                messages: userMessages
            })
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('API error:', response.status, errorText);
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        
        const data = await response.json();
        console.log('API response:', data);
        res.json({ content: data.content[0].text });
    } catch (error) {
        console.error('Detailed error:', error);
        res.status(500).json({ error: error.message, stack: error.stack });
    }
});

// Pornire server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});