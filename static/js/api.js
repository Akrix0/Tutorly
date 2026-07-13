export async function apiFetch(url, options) {
    let response = await fetch(url, options);

    if (response.status === 401) {
        const refreshResponse = await fetch("/api/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                refresh: localStorage.getItem("refresh"),
            }),
        });

        if (refreshResponse.ok) {
            const data = await refreshResponse.json();

            localStorage.setItem("access", data.access);

            options.headers.Authorization = `Bearer ${data.access}`;

            response = await fetch(url, options);
        } else {
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");

            window.location.href = "/login/";
        }
    }

    return response;
}
