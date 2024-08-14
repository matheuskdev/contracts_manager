document.addEventListener("DOMContentLoaded", () => {
    const message = document.getElementById("message");

    const removeMessage = () => {
        if (message && message.parentNode) {
            message.parentNode.removeChild(message);
        }
    };

    setTimeout(removeMessage, 5000);
});
