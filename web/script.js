

async function getResponseFromBackend(userInput) {
    try {
      const response = await fetch('/api/dialogflow', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      return data.reply; // Assuming the backend sends back a JSON with a 'reply' field
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  }

async function onUserSubmit() {
  const userInput = document.getElementById('user-input').value;
  const reply = await getResponseFromBackend(userInput);
  document.getElementById('bot-response').innerText = reply;
}

document.addEventListener('DOMContentLoaded', function() {
  const sendMessageButton = document.getElementById('send-message-btn');
  const messageInput = document.getElementById('message-input');

  sendMessageButton.addEventListener('click', function() {
      const userMessage = messageInput.value;
      // Clear the input
      messageInput.value = '';

      // Send the message to the backend
      fetch('http://localhost:5000/send_message', { // Make sure the URL matches your Flask app's route
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 'message': userMessage })
      })
      .then(response => response.json())
      .then(data => {
          // Display the response message on the frontend
          const responseDiv = document.getElementById('response');
          responseDiv.textContent = data.message; // Adjust according to your HTML structure
      })
      .catch(error => console.error('Error:', error));
  });
});

