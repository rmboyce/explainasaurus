let selectionStarted = false;
let sidepanelActive = false;

let mouseStartX;
let mouseStartY;

// Save to DB
function saveToDB(text, response) {
  const link = window.location.toString()
  const data = {link: link, selected: text, response: response}
  const body = JSON.stringify(data);

  fetch("http://localhost:8000/add_expl/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: body
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then(data => {
    console.log("Response data:", data);
  })
  .catch(error => {
    console.error("Error:", error);
  });
}

document.addEventListener('selectionchange', () => {
//   if(!sidepanelActive) {
//     const exampleDiv = document.getElementById('sidepanel');
//     sidepanelActive = (exampleDiv !== null);
//     console.log(sidepanelActive);
//   }
  if(document.getElementById('sidepanel') !== null) {
    const selectedText = window.getSelection().toString();
      if (selectedText && !selectionStarted) {
        selectionStarted = true;
        console.log('Selection started');
    }
  }
});

document.addEventListener('mousedown', (event) => {
  mouseStartX = event.clientX + window.scrollX;
  mouseStartY = event.clientY + window.scrollY;
});

document.addEventListener('mouseup', (event) => {
  if (selectionStarted) {
    selectionStarted = false;
    const selectedText = window.getSelection().toString();
    console.log('Selection ended: '+selectedText);

    const sidepanel = document.getElementById('sidepanel');
    var box = document.createElement("div");
    box.style.position = "absolute";
    box.style.top = mouseStartY + "px";
    box.style.border = "2px solid black";
    box.style.width = "29%";
    box.style.display = "block";
    sidepanel.appendChild(box);
    
    const boxHeight = "20px";
    var boxButtonContainer = document.createElement("div");
    // boxButtonContainer.style.backgroundColor = "red";
    boxButtonContainer.style.margin = "auto";
    boxButtonContainer.style.marginTop = "10px";
    boxButtonContainer.style.height = boxHeight;
    boxButtonContainer.style.width = "90%"
    box.appendChild(boxButtonContainer);

    var explanation = document.createElement("div");
    var saveBoxButton = document.createElement("div");
    saveBoxButton.style.height = boxHeight;
    saveBoxButton.style.width = boxHeight;
    saveBoxButton.style.backgroundColor = "white";
    saveBoxButton.style.float = "left";
    saveBoxButton.addEventListener("click", function() {
      console.log("save it");
      saveToDB(selectedText, explanation.innerText)
    });
    boxButtonContainer.appendChild(saveBoxButton);

    var saveIcon = document.createElement("img");
    saveIcon.src = chrome.runtime.getURL('./save.png');
    saveIcon.style.width = boxHeight;
    saveIcon.style.height = boxHeight;
    saveIcon.style.margin = "0px";
    saveBoxButton.appendChild(saveIcon);

    var deleteBoxButton = document.createElement("div");
    deleteBoxButton.style.height = boxHeight;
    deleteBoxButton.style.width = boxHeight;
    deleteBoxButton.style.backgroundColor = "white";
    deleteBoxButton.style.float = "right";
    deleteBoxButton.addEventListener("click", function() {
        box.remove();
    });
    boxButtonContainer.appendChild(deleteBoxButton);

    var deleteIcon = document.createElement("img");
    deleteIcon.src = chrome.runtime.getURL('./delete.png');
    deleteIcon.style.width = boxHeight;
    deleteIcon.style.height = boxHeight;
    deleteIcon.style.margin = "0px";
    deleteBoxButton.appendChild(deleteIcon);

    explanation.innerText = "thinking..."; //selectedText;
    explanation.style.margin = "15px";
    box.appendChild(explanation);

    // TODO: uncomment this once we want to generate the actual text
    const prompt = "Your task is to simplify the following text about Alzheimer's disease. Aim to convey the essential information in a clear and concise way, using fewer words than the original text. A non professional should be able to understand the response. Do not introduce any new information or change the meaning of the text. Do not include any special formatting like bold or italics in your response. Here is the text to simplify:\n"+selectedText;
    fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyCQHLZBNZws5jvxIRP1oIEkAiVaVoiInoI', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      contents: [{
        parts: [{
          text: prompt
        }]
      }]
    })
  })
  .then(response => response.json())
      .then(data => {
        // Process the response data
        console.log(data);
        explanation.innerText = data["candidates"][0]["content"]["parts"][0]["text"]
    })
    .catch(error => {
      // Handle errors
      console.error('Error:', error);
    });
  }
});