function copyText() {
    const textBox = document.getElementById("textBox");
    textBox.select();
    document.execCommand("copy");
  
    document.getElementById("message").textContent = "Text copied!";
    setTimeout(() => {
      document.getElementById("message").textContent = "";
    }, 2000);
  }
  
  function submitText() {
    const content = document.getElementById("textBox").value;
  
    if (content.trim() === "") {
      document.getElementById("message").textContent = "Textbox is empty.";
      return;
    }
  
    // Simulate submitting the data (e.g., to a server or log it)
    console.log("Submitted Text:", content);
    document.getElementById("message").textContent = "Text submitted successfully!";
    
    setTimeout(() => {
      document.getElementById("message").textContent = "";
    }, 2000);
  }
  