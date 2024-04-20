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