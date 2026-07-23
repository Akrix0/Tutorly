//* Elements
const lessonContainer = document.getElementById("lesson-container")
const deleteLessonBtn = document.getElementById("delete-btn")

const titleField = document.getElementById("lesson-title")
const idField = document.getElementById("lesson-id")
const statusField = document.getElementById("lesson-status")
const tutorlField = document.getElementById("lesson-tutor")
const studentField = document.getElementById("lesson-student")
const subjectField = document.getElementById("lesson-subject")
const dateField = document.getElementById("lesson-date")
const timeField = document.getElementById("lesson-time")
const linkField = document.getElementById("lesson-link")
const createdField = document.getElementById("lesson-created")
const updatedField = document.getElementById("lesson-updated")

const lessonId = lessonContainer.dataset.lessonId;
const lessonTitle = lessonContainer.dataset.lessonTitle;

const accountDetail = lessonContainer.dataset.accountDetail;
const lessonApiUrl = lessonContainer.dataset.lessonApiUrl;


//* API
async function getLessonData() {
    const token = localStorage.getItem("access");
    if (!token) return null;

    const response = await fetch(lessonApiUrl, {
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

async function deleteLesson(confirmed) {
    const token = localStorage.getItem("access");
    if (!token) return null;

    if (!confirmed) return null;

    try {
        const response = await fetch(lessonApiUrl, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.status === 204) {
            window.location.href = accountDetail;
            return;
        }

        const data = await response.json();
        if (!response.ok) {
            throw data;
        }
        return data;
    } catch (error) {
        console.error("Error deleting lesson:", error);
        throw error;
    }
}

//* Rendering
function renderStatus(field, status) {
    field.textContent = status
    switch (status) {
        case "Pending":
            field.classList.add("text-secondary");
            break;
        case "Confirmed":
            field.classList.add("text-warning");
            break;
        case "Completed":
            field.classList.add("text-success");
            break;
        case "Cancelled":
            field.classList.add("text-danger");
            break;
        default:
            field.classList.add("text-secondary");
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
    return new Date(date).toLocaleDateString("En", {
        weekday: "long",
    });
}

function renderLesson(lesson) {
    titleField.textContent = lessonTitle
    idField.textContent = lesson.id
    renderStatus(statusField, lesson.display_status)
    tutorlField.textContent = lesson.tutor.username
    studentField.textContent = lesson.student.username
    subjectField.textContent = lesson.display_subject_name;
    dateField.textContent = lesson.display_date;
    timeField.textContent = `${getWeekday(lesson.date)}, ${lesson.display_start_time} - ${lesson.display_end_time}`;
    linkField.innerHTML = renderLink(lesson.lesson_link)
    createdField.textContent = lesson.display_created_at;
    updatedField.textContent = lesson.display_updated_at;
}

deleteLessonBtn.addEventListener("click", (e) => {
    e.preventDefault();
    const confirmed = window.confirm("Are you sure you want to delete this lesson?")
    deleteLesson(confirmed)
})

//* Init
async function init() {
    try {
        const lesson = await getLessonData();
        if (!lesson) return;

        renderLesson(lesson);
    } catch (error) {
        console.error(error);
    }
}

init();