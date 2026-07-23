import { handleErrors } from "../core/utils.js";

//* Elements;
const lessonForm = document.getElementById("lesson-form");
const studentValue = lessonForm.dataset.studentId;
const subjectField = document.getElementById("subject");
const dateField = document.getElementById("date");
const startTimeField = document.getElementById("start-time");
const endTimeField = document.getElementById("end-time");
const lessonLinkField = document.getElementById("lesson-link");

//* URLs
const lessonDetailUrl = (lesson_pk) => `/lessons/${lesson_pk}/`;
const lessonCreateApiUrl = lessonForm.dataset.lessonCreateApiUrl;

//* API
async function createLesson(formData) {
    const token = localStorage.getItem("access");

    if (!token) {
        return;
    }

    const response = await fetch(lessonCreateApiUrl, {
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
async function handleLessonCreationSubmit(data) {
    const formData = {
        student: data.studentId,
        subject: data.subjectValue,
        date: data.dateValue,
        start_time: data.startTimeValue,
        end_time: data.endTimeValue,
        lesson_link: data.lessonLinkValue,
    };

    try {
        const lessonObj = await createLesson(formData);
        console.log("Lesson Created!");
        window.location.href = lessonDetailUrl(lessonObj.id);
    } catch (errors) {
        handleErrors(errors);
    }
}

//* Init
if (lessonForm) {
    lessonForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const rawData = {
            studentId: studentValue,
            subjectValue: Number(subjectField.value),
            dateValue: dateField.value,
            startTimeValue: startTimeField.value,
            endTimeValue: endTimeField.value,
            lessonLinkValue: lessonLinkField.value,

        }
        await handleLessonCreationSubmit(rawData);
    });
}