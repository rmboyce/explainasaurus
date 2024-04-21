// let existingContent;

function addSidePage() {
  const notActive = (document.getElementById('sidepanel') === null);
  if(notActive) {
    // existingContent = document.body.innerHTML;
    // document.body.innerHTML = `<div id="explainer_container"><div id="existing_content_wrapper">${existingContent}</div></div>`;

    // const explainerContainer = document.querySelector('#explainer_container');
    // const existingContentWrapper = document.querySelector('#existing_content_wrapper');
  
    // add elements to page
    var sidePanel = document.createElement("div");
    sidePanel.id = 'sidepanel';
    console.log(document.body.style.display);
    document.body.style.display = "grid";
    document.body.style.gridTemplateColumns = "67% 33%";
    document.body.style.gap = "10px";
    const elements = document.querySelectorAll("body > *");
    let i = 0;
    elements.forEach((element) => {
      i += 1;
      element.style.gridColumn = "1";
    })

    document.body.appendChild(sidePanel);
    sidePanel.style.gridColumn = "2";
    sidePanel.style.gridRowStart = "1";
    sidePanel.style.gridRowEnd = `${i}`;

    var placeholderText = document.createElement("div");
    placeholderText.innerText='Select text to explain!';
    sidePanel.appendChild(placeholderText);
  
    // style new elements
    // explainerContainer.style.display = "flex";
    // existingContentWrapper.style.width = "67%";

    sidePanel.style.width = "90%";
    sidePanel.style.border = "2px solid black";
    sidePanel.style.display = "flex";
    sidePanel.style.justifyContent = "center";
    placeholderText.style.marginTop = "40px";
  }
  else {
    document.getElementById('sidepanel').remove();
    document.body.style.display = "";
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
