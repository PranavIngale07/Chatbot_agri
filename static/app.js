document.addEventListener('DOMContentLoaded', function () {
    const sendButton = document.querySelector('.send__button');
    const inputField = document.querySelector('input[type="text"]');
    const messagesDiv = document.querySelector('.chatbox__messages');
    const chatbox = document.querySelector('.chatbox');
    const chatboxButton = document.querySelector('.chatbox__button button');

    // Toggle chatbox visibility on click with animation
    chatboxButton.addEventListener('click', function () {
        chatbox.classList.toggle('chatbox--active');
    });

    // Function to add messages to the chatbox
    function addMessageToChatbox(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('messages__item', `messages__item--${sender}`);
        messageElement.textContent = message;
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    // Handle send button click or "Enter" key press
    function sendMessage() {
        const userMessage = inputField.value;
        if (userMessage.trim() === '') return;

        addMessageToChatbox(userMessage, 'visitor');
        inputField.value = '';

        // Simulate response (replace with actual API call)
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            addMessageToChatbox(data.response, 'operator');
        });
    }

    sendButton.addEventListener('click', sendMessage);

    inputField.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
