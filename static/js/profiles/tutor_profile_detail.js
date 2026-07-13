//* Elements
const birthDateField = document.getElementById("birth-date");
const experienceYearsField = document.getElementById("experience-years");
const countryField = document.getElementById("country");

const subjectsContainer = document.getElementById("subjects-container");
const availabilitiesContainer = document.getElementById("availabilities-container");

const tutorProfilePk = document.getElementById("tutor-profile").dataset.profilePk;
const tutorProfileDetailUrl = `/profiles/api/profile/${tutorProfilePk}/`;

//* API
async function getTutorProfileData() {
    const token = localStorage.getItem("access");
    if (!token) return null;

    const response = await apiFetch(tutorProfileDetailUrl, {
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
function renderList(items, templateId, container, callback) {
    container.innerHTML = "";

    const template = document.getElementById(templateId);

    items.forEach(item => {
        const clone = template.content.cloneNode(true);
        callback(clone, item);
        container.appendChild(clone);
    });
}

function renderSubjects(subjects) {
    renderList(subjects, "subject-template", subjectsContainer, (clone, subject) => {
        clone.querySelector(".subject").textContent = subject.subject;
        clone.querySelector(".price-per-hour").textContent = subject.price_per_hour;
        clone.querySelector(".currency").textContent = subject.currency;
    });
}

function renderAvailabilities(availabilities) {
    renderList(availabilities, "availability-template", availabilitiesContainer, (clone, availability) => {
        clone.querySelector(".weekday").textContent = availability.weekday;
        clone.querySelector(".start-time").textContent = availability.start_time;
        clone.querySelector(".end-time").textContent = availability.end_time;
    });
}

function renderTutorProfile(profile) {
    birthDateField.textContent = profile.birth_date;
    experienceYearsField.textContent = profile.experience_years;
    countryField.textContent = profile.country;

    renderSubjects(profile.subjects);
    renderAvailabilities(profile.availabilities);
}

//* Init
async function init() {
    try {
        const profile = await getTutorProfileData();
        if (!profile) return;

        renderTutorProfile(profile);
    } catch (error) {
        console.error(error);
    }
}

init();