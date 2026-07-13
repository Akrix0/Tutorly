//* Imports
import {apiFetch} from "../api.js"

//* Elements
const accountContainer = document.getElementById("account-profile")
const avatarWrapper = document.getElementById("avatar-wrapper");

const avatarField = document.getElementById("avatar")
const usernameField = document.getElementById("username")
const bioField = document.getElementById("bio")
const emailField = document.getElementById("email")
const firstNameField = document.getElementById("first-name")
const lastNameField = document.getElementById("last-name")

const accountUrl = accountContainer.dataset.accountUrl;
const accountEdit = accountContainer.dataset.accountEdit

//* API
async function getAccountData() {
    const token = localStorage.getItem("access");
    if (!token) return null;

    const response = await apiFetch(accountUrl, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await response.json();

    if (!response.ok) {
        throw data;
    }

    return data;
}

//* Rendering
function getInitials(account) {
    const first = account.first_name?.trim()?.[0] ?? "";
    const last = account.last_name?.trim()?.[0] ?? "";

    if (first || last) {
        return (first + last).toUpperCase();
    }

    return account.username[0].toUpperCase();
}

function renderAvatar(account) {
    if (account.avatar) {
        avatarField.src = account.avatar;
        avatarField.alt = `${account.username}'s avatar`;
        return;
    }

    avatarWrapper.replaceChildren();

    const initials = document.createElement("div");
    initials.className = "avatar-initials";
    initials.textContent = getInitials(account);

    avatarWrapper.append(initials);
}

function renderAccount(account) {
    renderAvatar(account);

    usernameField.textContent = account.username;
    bioField.textContent = account.bio;
    emailField.textContent = account.email;
    firstNameField.textContent = account.first_name;
    lastNameField.textContent = account.last_name;
}

//* Init
async function init() {
    try {
        const account = await getAccountData();
        if (!account) return;

        renderAccount(account);
    } catch (error) {
        console.error(error);
    }
}

init();