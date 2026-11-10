
document.addEventListener("DOMContentLoaded", function () {

    // Automatically hide success messages
    const messages = document.querySelectorAll(".toast");

    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.transition = "opacity 0.5s";
            message.style.opacity = "0";

            setTimeout(() => message.remove(), 500);
        }, 3500);
    });

    // Smooth page appearance
    document.body.style.opacity = "0";

    requestAnimationFrame(() => {
        document.body.style.transition = "opacity 0.5s ease";
        document.body.style.opacity = "1";
    });

});
