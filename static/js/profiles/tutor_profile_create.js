//* Elements
const subjectsContainer = document.querySelector("#subjects-container");
const availabilitiesContainer = document.querySelector("#availabilities-container");

const subjectTemplate = document.querySelector("#subject-template");
const availabilityTemplate = document.querySelector("#availability-template");

const globalForm = document.getElementById("tutor-profile-form");
const tutorCardContainer = document.getElementById("tutor-card-container");

const addSubjectBtn = document.getElementById("add-subject");
const addAvailabilityBtn = document.getElementById("add-availability");

//* URLs
const HOME_URL = "/";
const TUTOR_PROFILE_CREATE_URL = "/profiles/api/profile/create/";

//* Helpers
function appendTemplate(container, template) {
    container.appendChild(template.content.cloneNode(true));
}

function removeItem(event, className, itemClass) {
    if (event.target.classList.contains(className)) {
        event.target.closest(itemClass).remove();
    }
}

function getSubjectData(item) {
    return {
        subject: Number(item.querySelector("[name='subject']").value),
        price_per_hour: item.querySelector("[name='price-per-hour']").value,
        currency: item.querySelector("[name='currency']").value,
    };
}

function getAvailabilityData(item) {
    return {
        weekday: Number(item.querySelector("[name='weekday']").value),
        start_time: item.querySelector("[name='start-time']").value,
        end_time: item.querySelector("[name='end-time']").value,
    };
}

function validateStep(step) {
    const currentStep = document.getElementById(`step${step}`);

    for (const field of currentStep.querySelectorAll("input, select, textarea")) {
        if (!field.checkValidity()) {
            field.reportValidity();
            return false;
        }
    }

    return true;
}

function showStep(step) {
    document.querySelector(".form-step.active")?.classList.remove("active");
    document.getElementById(`step${step}`).classList.add("active");
}

function nextStep(step) {
    if (!validateStep(step - 1)) {
        return;
    }

    showStep(step);
}

function prevStep(step) {
    showStep(step);
}

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

//* API
async function createTutorProfile(formData) {
    const token = localStorage.getItem("access");

    if (!token) {
        return;
    }

    const response = await fetch(TUTOR_PROFILE_CREATE_URL, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${token}`,
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

//* Event Handlers
async function handleTutorProfileCreationSubmit(form) {
    const subjects = [...subjectsContainer.children].map(getSubjectData);
    const availabilities = [...availabilitiesContainer.children].map(getAvailabilityData);

    const data = {
        birth_date: form.elements["birth-date"].value,
        experience_years: Number(form.elements["experience-years"].value),
        country: form.elements["country"].value,
        subjects,
        availabilities,
    };

    try {
        await createTutorProfile(data);
        console.log("Tutor profile created");
        window.location.href = HOME_URL;
    } catch (errors) {
        handleErrors(errors);
    }
}

//* Init
appendTemplate(subjectsContainer, subjectTemplate);
appendTemplate(availabilitiesContainer, availabilityTemplate);

document.getElementById("next-step-1").addEventListener("click", () => nextStep(2));
document.getElementById("next-step-2").addEventListener("click", () => nextStep(3));
document.getElementById("prev-step-2").addEventListener("click", () => prevStep(1));
document.getElementById("prev-step-3").addEventListener("click", () => prevStep(2));

subjectsContainer.addEventListener("click", (event) => {
    removeItem(event, "remove-subject", ".subject-item");
});

availabilitiesContainer.addEventListener("click", (event) => {
    removeItem(event, "remove-availability", ".availability-item");
});

addSubjectBtn.addEventListener("click", () => {
    appendTemplate(subjectsContainer, subjectTemplate);
});

addAvailabilityBtn.addEventListener("click", () => {
    appendTemplate(availabilitiesContainer, availabilityTemplate);
});

if (subjectsContainer && availabilitiesContainer && tutorCardContainer) {
    globalForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await handleTutorProfileCreationSubmit(globalForm);
    });
}