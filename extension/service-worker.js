function addSidePage() {
  const notActive = (document.getElementById('explainer_container') === null);
  if(notActive) {
    const existingContent = document.body.innerHTML;
    document.body.innerHTML = `<div id="explainer_container"><div id="existing_content_wrapper">${existingContent}</div></div>`;
  
    const explainerContainer = document.querySelector('#explainer_container');
    const existingContentWrapper = document.querySelector('#existing_content_wrapper');
  
    // add elements to page
    var sidePanel = document.createElement("div");
    sidePanel.id = 'sidepanel';
    explainerContainer.appendChild(sidePanel);
    var placeholderText = document.createElement("div");
    placeholderText.innerText='Select text to explain!';
    sidePanel.appendChild(placeholderText);
  
    // style new elements
    explainerContainer.style.display = "flex";
    existingContentWrapper.style.width = "67%";
    sidePanel.style.width = "33%";
    sidePanel.style.border = "2px solid black";
    sidePanel.style.display = "flex";
    sidePanel.style.justifyContent = "center";
    placeholderText.style.marginTop = "40px";
  }
}

chrome.action.onClicked.addListener((tab) => {
  if (!tab.url.includes('chrome://')) {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: addSidePage
    });
  }
});
