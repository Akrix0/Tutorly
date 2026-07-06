const registerUrl = "/accounts/api/register/";

async function registerUser(formData) {
    const response = await fetch(registerUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
    });

    const result = await response.json();

    if (!response.ok) {
        throw result;
    }

    return result;
}

async function handleRegisterSubmit(form) {
    const data = {
        username: form.elements["username"].value,
        email: form.elements["email"].value,
        password: form.elements["password"].value,
        password2: form.elements["password2"].value,
    };
    if (!data.username || !data.email || !data.password || !data.password2) {
        alert("Заповніть усі поля");
        return;
    }
    try {
        await registerUser(data);
        console.log("Користувача створено");
        window.location.href = "/accounts/login/";
    } catch (errors) {
        console.error(errors);
        let message = "";
        for (const [field, fieldErrors] of Object.entries(errors)) {
            message += `${field}:\n`;
            for (const error of fieldErrors) {
                message += ` • ${error}\n`;
            }
            message += "\n";
        }
        alert(message);
    }
}

const registerForm = document.getElementById("register-form");

registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await handleRegisterSubmit(registerForm);
});