console.log("Chatbot script loaded");

async function getPageInfo() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    console.log("Requesting info for page:", currentPage);
    try {
        const response = await fetch(`/page-info?page=${currentPage}`);
        if (response.ok) {
            const data = await response.json();
            console.log("Page info received:", data);
            return data;
        }
        console.error("Error response:", response.status, response.statusText);
        throw new Error(`HTTP error! status: ${response.status}`);
    } catch (error) {
        console.error("Error in getPageInfo:", error);
        throw error;
    }
}

function toggleChat() {
    var chatContainer = document.getElementById('chatbot-container');
    if (chatContainer.style.display === 'none' || chatContainer.style.display === '') {
        chatContainer.style.display = 'flex';
    } else {
        chatContainer.style.display = 'none';
    }
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    
    if (userInput.value.trim() === '') return;
    
    chatMessages.innerHTML += `<p><strong>Tu:</strong> ${userInput.value}</p>`;
    
    try {
        console.log("Attempting to get page info...");
        const pageInfo = await getPageInfo();
        console.log("Page info retrieved successfully");

        console.log("Sending chat message...");
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: [
                    { role: "system", content: `Informații despre pagina curentă: ${JSON.stringify(pageInfo)}` },
                    { role: "user", content: userInput.value }
                ]
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error("Error response from chat:", errorData);
            throw new Error(`HTTP error! status: ${response.status}, message: ${JSON.stringify(errorData)}`);
        }
        
        const data = await response.json();
        console.log('API Response:', data);
        
        if (data.content) {
            const botReply = data.content;
            chatMessages.innerHTML += `<p><strong>Bot:</strong> ${botReply}</p>`;
        } else {
            throw new Error('Răspunsul API nu are structura așteptată');
        }
    } catch (error) {
        console.error('Eroare detaliată:', error);
        chatMessages.innerHTML += `<p><strong>Eroare:</strong> ${error.message}</p>`;
    }
    
    userInput.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}