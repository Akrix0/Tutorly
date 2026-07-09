//* Display forms from templates
const subjectsContainer = document.querySelector("#subjects-container");
const subjectTemplate = document.querySelector("#subject-template");

subjectsContainer.appendChild(subjectTemplate.content.cloneNode(true));

const availabilitiesContainer = document.querySelector("#availabilities-container");
const availabilityTemplate = document.querySelector("#availability-template");

availabilitiesContainer.appendChild(availabilityTemplate.content.cloneNode(true));

document.getElementById("next-step-1").addEventListener("click", () => {
    nextStep(2);
});

document.getElementById("prev-step-2").addEventListener("click", () => {
    prevStep(1);
});

document.getElementById("next-step-2").addEventListener("click", () => {
    nextStep(3);
});

document.getElementById("prev-step-3").addEventListener("click", () => {
    prevStep(2);
});

//! Deleting and Adding items

//* Deleting and adding subject items
subjectsContainer.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-subject")) {
        e.target.closest(".subject-item").remove();
    }
});

const addSubjectsBtn = document.getElementById("add-subject");
addSubjectsBtn.addEventListener("click", (e) => {
    subjectsContainer.appendChild(subjectTemplate.content.cloneNode(true));
})

//* Deleting and adding availabilities items
availabilitiesContainer.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-availability")) {
        e.target.closest(".availability-item").remove();
    }
});

const addAvailabilityBtn = document.getElementById("add-availability");
addAvailabilityBtn.addEventListener("click", (e) => {
    availabilitiesContainer.appendChild(availabilityTemplate.content.cloneNode(true));
})

//! Function to move between forms

//* Function to move to next step of form
function nextStep(step) {
    const currentStep = document.getElementById(`step${step - 1}`);

    const fields = currentStep.querySelectorAll("input, select, textarea");

    for (const field of fields) {
        if (!field.checkValidity()) {
            field.reportValidity();
            return;
        }
    }

    currentStep.classList.remove("active");
    document.getElementById(`step${step}`).classList.add("active");
}

//* Function to move to previous step of form
function prevStep(step) {
    document.getElementById(`step${step + 1}`).classList.remove("active");
    document.getElementById(`step${step}`).classList.add("active");
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

const homeUrl = "/"
const loginUrl = "/login/";
const tutorProfileCreateUrl = "/profiles/api/profile/create/"


//?|———————————————————CREATE—TUTOR—PROFILE———————————————————|

//* Function to create tutor profile
async function createTutorProfile(formData) {
    const token = localStorage.getItem("access");
    if (!token) {return}
    const response = await fetch(tutorProfileCreateUrl, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
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


//* Function to handle tutor profile creation form
async function handleTutorProfileCreationSubmit(tutorCardContainer, subjectsContainer, availabilitiesContainer,) {
    const subjects = [...subjectsContainer.children].map(item => ({
        subject: Number(item.querySelector("[name='subject']").value),
        price_per_hour: item.querySelector("[name='price-per-hour']").value,
        currency: item.querySelector("[name='currency']").value,
    }));

    const availabilities = [...availabilitiesContainer.children].map(item => ({
        weekday: Number(item.querySelector("[name='weekday']").value),
        start_time: item.querySelector("[name='start-time']").value,
        end_time: item.querySelector("[name='end-time']").value,
    }));

    const data = {
        birth_date: tutorCardContainer.elements["birth-date"].value,
        experience_years: Number(
            tutorCardContainer.elements["experience-years"].value
        ),
        country: tutorCardContainer.elements["country"].value,
        subjects,
        availabilities,
    };

    try {
        await createTutorProfile(data);
        console.log("Tutor profile created");
        window.location.href = homeUrl;
    } catch (errors) {
        handleErrors(errors);
    }
}

const globalForm = document.getElementById("tutor-profile-form")
const tutorCardContainer = document.getElementById("tutor-card-container");

if (subjectsContainer && availabilitiesContainer && tutorCardContainer) {
    globalForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await handleTutorProfileCreationSubmit(globalForm, subjectsContainer, availabilitiesContainer);
    });
} 
