//* Elements
const accountEditForm = document.getElementById("account-edit-form");

const usernameInput = document.getElementById("username");
const emailInput = document.getElementById("email");
const firstNameInput = document.getElementById("first-name");
const lastNameInput = document.getElementById("last-name");
const bioInput = document.getElementById("bio");
const avatarInput = document.getElementById("avatar");

const accountUrl = accountEditForm.dataset.accountUrl;
const accountDetail = accountEditForm.dataset.accountDetail;

// Тут будемо зберігати початкові дані
let originalAccount = null;

//* Render
function renderAccount(account) {
    originalAccount = account;

    usernameInput.value = account.username ?? "";
    emailInput.value = account.email ?? "";
    firstNameInput.value = account.first_name ?? "";
    lastNameInput.value = account.last_name ?? "";
    bioInput.value = account.bio ?? "";
}

//* API
async function getAccountData() {
    const token = localStorage.getItem("access");
    if (!token) return null;

    const response = await fetch(accountUrl, {
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

async function editAccount(formData) {
    const token = localStorage.getItem("access");
    if (!token) return null;

    const response = await fetch(accountUrl, {
        method: "PATCH",
        headers: {
            Authorization: `Bearer ${token}`,
        },
        body: formData,
    });

    const result = await response.json();

    if (!response.ok) {
        throw result;
    }

    return result;
}

//* Helpers
function createPatchData() {
    const formData = new FormData();

    if (usernameInput.value.trim() !== originalAccount.username) {
        formData.append("username", usernameInput.value.trim());
    }

    if (emailInput.value.trim() !== originalAccount.email) {
        formData.append("email", emailInput.value.trim());
    }

    if (firstNameInput.value.trim() !== (originalAccount.first_name ?? "")) {
        formData.append("first_name", firstNameInput.value.trim());
    }

    if (lastNameInput.value.trim() !== (originalAccount.last_name ?? "")) {
        formData.append("last_name", lastNameInput.value.trim());
    }

    if (bioInput.value.trim() !== (originalAccount.bio ?? "")) {
        formData.append("bio", bioInput.value.trim());
    }

    if (avatarInput.files.length > 0) {
        formData.append("avatar", avatarInput.files[0]);
    }

    return formData;
}

//* Handling
async function handleAccountEdit(event) {
    event.preventDefault();

    const formData = createPatchData();

    // FormData не має length
    if ([...formData.keys()].length === 0) {
        alert("Немає змін.");
        return;
    }

    try {
        const account = await editAccount(formData);

        renderAccount(account);

        window.location.href = accountDetail;
    } catch (error) {
        console.error(error);
    }
}

accountEditForm.addEventListener("submit", handleAccountEdit);

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