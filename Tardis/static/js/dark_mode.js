// Function to toggle dark mode
function toggleDarkMode() {
    const body = document.body;
    const isDarkMode = body.classList.toggle("dark");

    // Save preference in local storage
    localStorage.setItem("darkMode", isDarkMode ? "dark" : "light");

    // Optionally, update the server-side session
    fetch("/home/toggle-dark-mode", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ darkMode: isDarkMode }),
    });
}

// Check local storage on page load and apply the saved mode
document.addEventListener("DOMContentLoaded", () => {
    const savedMode = localStorage.getItem("darkMode");
    if (savedMode === "dark") {
        document.body.classList.add("dark");
    }

    // Attach event listener to the toggle button
    const toggleButton = document.getElementById("darkModeToggle");
    toggleButton.addEventListener("click", toggleDarkMode);
});
