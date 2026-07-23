import { handleErrors } from "../core/utils.js";

//* Elements
const lessonEditForm = document.getElementById("lesson-edit-form");

const subjectInput = document.getElementById("subject");
const dateInput = document.getElementById("date");
const startTimeInput = document.getElementById("start-time");
const endTimeInput = document.getElementById("end-time");
const lessonLinkInput = document.getElementById("lesson-link");

const lessonUrl = lessonEditForm.dataset.lessonUrl;
const lessonDetail = lessonEditForm.dataset.lessonDetail;


let originalLesson = null;

//* Render
function renderLesson(lesson) {
    originalLesson = lesson;

    subjectInput.value = lesson.subject.id ?? "";
    dateInput.value = lesson.date ?? "";
    startTimeInput.value = lesson.start_time ?? "";
    endTimeInput.value = lesson.end_time ?? "";
    lessonLinkInput.value = lesson.lesson_link ?? "";
}

//* API
async function getLessonData() {
    const token = localStorage.getItem("access");
    if (!token) return null;

    const response = await fetch(lessonUrl, {
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

async function editLesson(formData) {
    const token = localStorage.getItem("access");
    if (!token) return null;

    const response = await fetch(lessonUrl, {
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

    if (subjectInput.value.trim() !== String(originalLesson.subject.id)) {
        formData.append("subject", subjectInput.value.trim());
    }

    if (dateInput.value.trim() !== (originalLesson.date ?? "")) {
        formData.append("date", dateInput.value.trim());
    }

    if (startTimeInput.value.trim() !== (originalLesson.start_time ?? "")) {
        formData.append("start_time", startTimeInput.value.trim());
    }

    if (endTimeInput.value.trim() !== (originalLesson.end_time ?? "")) {
        formData.append("end_time", endTimeInput.value.trim());
    }

    if (lessonLinkInput.value.trim() !== (originalLesson.lesson_link ?? "")) {
        formData.append("lesson_link", lessonLinkInput.value.trim());
    }

    return formData;
}

//* Handling
async function handleLessonEdit(event) {
    event.preventDefault();

    const formData = createPatchData();

    // FormData не має length
    if ([...formData.keys()].length === 0) {
        alert("Немає змін.");
        return;
    }

    try {
        const lesson = await editLesson(formData);

        renderLesson(lesson);

        window.location.href = lessonDetail;
    } catch (error) {
        handleErrors(errors)
    }
}

lessonEditForm.addEventListener("submit", handleLessonEdit);

//* Init
async function init() {
    try {
        const lesson = await getLessonData();
        if (!lesson) return;

        renderLesson(lesson);
    } catch (error) {
        handleErrors(errors)
    }
}

init();