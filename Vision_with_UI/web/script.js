// Add an event listener to the navigation links
document.querySelector('nav a').addEventListener('click', function() {
    // Get the current URL
    var currentURL = window.location.href;
    // Get the target URL
    var targetURL = window.location.hash;
    // Get the current URL path
    var currentURLPath = currentURL.split('#')[0];
    // Get the target URL path
    var targetURLPath = targetURL.split('#')[1];
    // Check if the target URL is the same as the current URL
    if (targetURLPath === currentURLPath) {
        // If they are the same, navigate to the current URL
        window.location.href = currentURL;
    } else {
        // If they are not the same, navigate to the target URL
        window.location.href = targetURL;
    }
});