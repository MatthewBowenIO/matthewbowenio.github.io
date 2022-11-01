document.addEventListener('DOMContentLoaded', event => {
    document.getElementById('theButton').addEventListener("click", event => {

        // Just go back to the outside iframe we came from.
        document.cookie = "embeddedCookie=Cookie loaded; SameSite=None; Secure; path=/";
        window.history.back();
    });
});