const scanForm = document.getElementById("url-form");
const scanButton = document.getElementById("scan-button");
const urlInput = document.getElementById("url");

if (scanForm && scanButton && urlInput) {
    scanForm.addEventListener("submit", function (event) {
        const enteredUrl = urlInput.value.trim();

        if (!enteredUrl) {
            event.preventDefault();
            urlInput.focus();
            return;
        }

        scanButton.disabled = true;
        scanButton.textContent = "Analyzing...";
    });
}