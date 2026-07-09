//* URLs
const apiUrl = "/api"
const homeUrl = "/"
const registerUrl = "/register/";
const loginUrl = "/login/";
const logoutUrl = "/logout/";

function handleErrors(errors) {
    console.error(errors);
    let message = "";
    for (const [field, fieldErrors] of Object.entries(errors)) {
        message += `${field}:\n`;
        if (typeof fieldErrors === "string") {
            message += `${fieldErrors}\n`;
        } else {
            for (const error of fieldErrors) {
                message += ` • ${error}\n`;
            }
        }
        message += "\n";
    }
    alert(message);
}

//!/——————————————————————————————————————————————\
//!|———————————————————FUNCTIONS———————————————————|
//!\——————————————————————————————————————————————/

//?|———————————————————REGISTER———————————————————|

//* Function to register user
async function registerUser(formData) {
    const response = await fetch(apiUrl + registerUrl, {
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

//* Function to handle register form
async function handleRegisterSubmit(registerForm) {
    const data = {
        username: registerForm.elements["username"].value.trim(),
        email: registerForm.elements["email"].value,
        password: registerForm.elements["password"].value,
        password2: registerForm.elements["password2"].value,
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
        handleErrors(errors)
    }
}

//?|———————————————————LOGIN———————————————————|

//* Function to login user
async function loginUser(formData) {
    const response = await fetch(apiUrl + loginUrl, {
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
    
    localStorage.setItem("access", result.access);
    localStorage.setItem("refresh", result.refresh);


    return result;
}

//* Function to handle login form
async function handleLoginSubmit(loginForm) {
    const data = {
        username: loginForm.elements["username"].value.trim(),
        password: loginForm.elements["password"].value,
    };
    if (!data.username || !data.password) {
        alert("Заповніть усі поля");
        return;
    }
    try {
        await loginUser(data);
        window.location.replace(homeUrl);
    } catch (errors) {
        handleErrors(errors)
    }
}

//?|———————————————————LOGOUT———————————————————|

//* Function to logout user
async function logoutUser() {
    const refresh = localStorage.getItem("refresh")

    if (!refresh) {
        return;
    }

    const response = await fetch(apiUrl + logoutUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            refresh
        }),
    });

    const result = await response.json();

    if (!response.ok) {
        throw result;
    }
    
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

    return result;
}

//* Function to handle logout
async function handleLogoutSubmit() {
    try {
        
        await logoutUser();
        window.location.href = loginUrl;
    } catch (errors) {
        handleErrors(errors)
    }
}

//* Forms
const registerForm = document.getElementById("register-form");
const loginForm = document.getElementById("login-form");
const logoutForm = document.getElementById("logout-form");


if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await handleRegisterSubmit(registerForm);
    });
} 
if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await handleLoginSubmit(loginForm);
    });
}
if (logoutForm) {
    logoutForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await handleLogoutSubmit();
    });
}