// Check for iOS / Safari.
console.log("Loading");

document.cookie = "embeddedCookie=Cookie loaded; SameSite=None; Secure; path=/";

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener('DOMContentLoaded', event => {

    // Always try to get the cookie.
    const cookieValue = getCookie('embeddedCookie');
    if (cookieValue) {
        document.getElementById('cookieValue').innerText = cookieValue;
    }
});

if (!!document.hasStorageAccess) {
    console.log("hasStorageAccess() available");
    document.hasStorageAccess().then(result => {

        // If we don't have access we must request it, but the request
        // must come from a UI event.
        console.log("hasStorageAccess() => " + result);

        if (!result) {
            // Show the button and tie to the click.
            const requestStorageAccessButton =
                    document.getElementById('requestStorageAccessButton');
            requestStorageAccessButton.style.visibility = "visible";
            requestStorageAccessButton.addEventListener("click", event => {
                console.log("Clicked");
                // On UI event, consume the event by requesting access.
                document.requestStorageAccess().then(() => {
                    console.log("requestStorageAccess()");
                    document.cookie = "embeddedCookie=Cookie loaded; SameSite=None; Secure; path=/";
                    // Finally, we are allowed! Reload to get the cookie.
                    window.location.reload();
                }).catch(err => {

                    // If we get here, it means either our page
                    // was never loaded as a first party page,
                    // or the user clicked 'Don't Allow'.
                    // Either way open that now so the user can request
                    // from there (or learn more about us).
                    window.top.location = window.location.href + "requeststorageaccess.html";
                });
            });
        }
    }).catch(err => console.error(err));
}