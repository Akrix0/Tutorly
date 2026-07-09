//* Tutor card fields
const birthDateField = document.getElementById("birth-date")
const expirienceYearsField = document.getElementById("experience-years")
const countryField = document.getElementById("country")


const subjectsContainer = document.getElementById("subjects-container")


const availabilitiesContainer = document.getElementById("availabilities-container")

const tutorProfilePk = document.getElementById("tutor-profile").dataset.profilePk;
const tutorProfileDetailUrl = `/profiles/api/profile/${tutorProfilePk}/`

async function getTutorProfileData() {
    const token = localStorage.getItem("access");
    if (!token) {return}
    const response = await fetch(tutorProfileDetailUrl, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
        }
    });

    const result = await response.json();

    if (!response.ok) {
        throw result;
    }

    return result;
}

function renderSubjects(subjects) {
    subjectsContainer.innerHTML = "";

    const template = document.getElementById("subject-template");

    subjects.forEach(subject => {
        const clone = template.content.cloneNode(true);

        clone.querySelector(".subject").textContent = subject.subject;
        clone.querySelector(".price-per-hour").textContent = subject.price_per_hour;
        clone.querySelector(".currency").textContent = subject.currency;

        subjectsContainer.appendChild(clone);
    });
}

function renderAvailabilities(availabilities) {
    availabilitiesContainer.innerHTML = "";

    const template = document.getElementById("availability-template");

    availabilities.forEach(availability => {
        const clone = template.content.cloneNode(true);

        clone.querySelector(".weekday").textContent = availability.weekday;
        clone.querySelector(".start-time").textContent = availability.start_time;
        clone.querySelector(".end-time").textContent = availability.end_time;

        availabilitiesContainer.appendChild(clone);
    });
}

function handleTutorProfile(profile) {
    birthDateField.textContent = profile.birth_date;
    expirienceYearsField.textContent = profile.experience_years;
    countryField.textContent = profile.country;

    renderSubjects(profile.subjects);
    renderAvailabilities(profile.availabilities);
}

async function init() {
    try {
        const profile = await getTutorProfileData();
        handleTutorProfile(profile);
    } catch (error) {
        console.error(error);
    }
}

init();