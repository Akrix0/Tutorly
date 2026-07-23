export function handleErrors(errors) {
    console.error(errors);

    const errorsContainer = document.getElementById("errors");

    let html = "";

    for (const [field, fieldErrors] of Object.entries(errors)) {

        const messages = Array.isArray(fieldErrors)
            ? fieldErrors
            : [fieldErrors];

        html += `<strong>${field}</strong><ul>`;

        for (const error of messages) {
            html += `<li>${error}</li>`;
        }

        html += "</ul>";
    }

    if (errorsContainer) {
        errorsContainer.innerHTML = html;
        errorsContainer.hidden = false;
        errorsContainer.scrollIntoView({
            behavior: "smooth",
            block: "start",
        });
    } else {
        alert(html.replace(/<[^>]*>/g, ""));
    }
}