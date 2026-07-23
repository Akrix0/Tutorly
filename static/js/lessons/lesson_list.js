import { handleErrors } from "../core/utils.js";

//* Elements
const lessonsListContainer = document.getElementById("lessons-list-container");
const lessonTemplate = document.getElementById("lesson-template");

//* URLs
const lessonDetailUrl = (lesson_pk) => `/lessons/${lesson_pk}/`;
const lessonListApiUrl = lessonsListContainer.dataset.lessonListUrl;

//* Render
function renderTitle(lesson) {
    return `${lesson.display_subject_name} Lesson for ${lesson.student.username} with ${lesson.tutor.username}`
}

function renderStatus(field, status) {
    field.textContent = status
    switch (status) {
        case "Pending":
            field.classList.add("bg-secondary");
            break;
        case "Confirmed":
            field.classList.add("bg-warning");
            break;
        case "Completed":
            field.classList.add("bg-success");
            break;
        case "Cancelled":
            field.classList.add("bg-danger");
            break;
        default:
            field.classList.add("bg-secondary");
        }
}

function renderLink(link) {
    return `
        <a href="${link}" class="text-decoration-none">
            Link to lesson
        </a>
        `;  
}

function getWeekday(date) {
    return new Date(date).toLocaleDateString("en-US", {
        weekday: "long",
    });
}

function renderLessons(lessons) {
    lessons.forEach(lesson => {
        const clone = lessonTemplate.content.cloneNode(true);

        clone.querySelector(".lesson-title").textContent = renderTitle(lesson);
        renderStatus(clone.querySelector(".lesson-status"), lesson.display_status);
        clone.querySelector(".lesson-id").textContent = lesson.id;
        clone.querySelector(".lesson-tutor").textContent = lesson.tutor.username;
        clone.querySelector(".lesson-student").textContent = lesson.student.username;
        clone.querySelector(".lesson-subject").textContent = lesson.display_subject_name;
        clone.querySelector(".lesson-date").textContent = lesson.display_date;
        clone.querySelector(".lesson-time").textContent = `${getWeekday(lesson.date)}, ${lesson.display_start_time} - ${lesson.display_end_time}`;
        clone.querySelector(".lesson-link").innerHTML = renderLink(lesson.lesson_link);
        clone.querySelector(".lesson-created").textContent = lesson.display_created_at;
        clone.querySelector(".lesson-detail-link").href = lessonDetailUrl(lesson.id);

        lessonsListContainer.appendChild(clone)
    });
}


//* API
async function getLessonsData() {
    const token = localStorage.getItem("access");
    if (!token) return null;

    const response = await fetch(lessonListApiUrl, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    const data = await response.json();
    console.log(data);

    if (!response.ok) {
        throw data;
    }

    return data;
}

//* Init
async function init() {
    try {
        const lessons = await getLessonsData();
        if (!lessons) return;

        renderLessons(lessons);
    } catch (errors) {
        handleErrors(errors)
    }
}

init();