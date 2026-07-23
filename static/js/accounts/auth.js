import { handleErrors } from "../core/utils.js";

//* URLs
const apiUrl = "/api";
const homeUrl = "/";
const registerUrl = "/register/";
const loginUrl = "/login/";
const logoutUrl = "/logout/";

//* Elements
const registerForm = document.getElementById("register-form");
const loginForm = document.getElementById("login-form");
const logoutForm = document.getElementById("logout-form");

//* Helpers
async function postJson(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
        throw result;
    }

    return result;
}

//* API
async function registerUser(formData) {
    return postJson(apiUrl + registerUrl, formData);
}

async function loginUser(formData) {
    const result = await postJson(apiUrl + loginUrl, formData);

    localStorage.setItem("access", result.access);
    localStorage.setItem("refresh", result.refresh);

    return result;
}

async function logoutUser() {
    const refresh = localStorage.getItem("refresh");

    if (!refresh) {
        return;
    }

    const result = await postJson(apiUrl + logoutUrl, { refresh });

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

    return result;
}

//* Event Handlers
async function handleRegisterSubmit(form) {
    const data = {
        username: form.elements.username.value.trim(),
        email: form.elements.email.value,
        password: form.elements.password.value,
        password2: form.elements.password2.value,
    };

    if (!data.username || !data.email || !data.password || !data.password2) {
        alert("Заповніть усі поля");
        return;
    }

    try {
        await registerUser(data);
        console.log("Користувача створено");
        window.location.href = loginUrl;
    } catch (errors) {
        handleErrors(errors);
    }
}

async function handleLoginSubmit(form) {
    const data = {
        username: form.elements.username.value.trim(),
        password: form.elements.password.value,
    };

    if (!data.username || !data.password) {
        alert("Заповніть усі поля");
        return;
    }

    try {
        await loginUser(data);
        window.location.replace(homeUrl);
    } catch (errors) {
        handleErrors(errors);
    }
}

async function handleLogoutSubmit() {
    try {
        await logoutUser();
        window.location.href = loginUrl;
    } catch (errors) {
        handleErrors(errors);
    }
}

function bindFormSubmit(form, handler) {
    if (!form) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        await handler(form);
    });
}

//* Init
bindFormSubmit(registerForm, handleRegisterSubmit);
bindFormSubmit(loginForm, handleLoginSubmit);

if (logoutForm) {
    logoutForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await handleLogoutSubmit();
    });
}