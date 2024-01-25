function loadContent(event, url, targetSelector = '.main-dynamic-content-block') {
    event.preventDefault(); // Stop the page from navigating to the href
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const contentBlock = document.querySelector(targetSelector);
            contentBlock.innerHTML = html;
            // Execute any script tags found in the HTML
            const scripts = contentBlock.querySelectorAll('script');
            for (let script of scripts) {
                const newScript = document.createElement('script');
                if (script.src) {
                    newScript.src = script.src;
                } else {
                    newScript.textContent = script.textContent;
                }
                // Replace the old script with the new one to ensure it's executed
                script.parentNode.replaceChild(newScript, script);
            }
            // You might need to update the URL in the browser if desired
            window.history.pushState({}, '', url);
        })
        .catch(error => console.error('Error loading content:', error));
}