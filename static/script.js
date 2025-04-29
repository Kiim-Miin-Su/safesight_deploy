const video = document.getElementById("video-capture");
const canvas = document.getElementById("overlay-canvas");
const ctx = canvas.getContext("2d");
const missingList = document.getElementById("missing-list");

async function setupCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    await video.play();
}

function captureFrame() {
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = video.videoWidth;
    tempCanvas.height = video.videoHeight;
    const tempCtx = tempCanvas.getContext("2d");
    tempCtx.drawImage(video, 0, 0);
    return new Promise(resolve => tempCanvas.toBlob(resolve, "image/jpeg"));
}

async function detectAndDraw() {
    const task = document.getElementById("task-select").value;
    const frame = await captureFrame();

    const formData = new FormData();
    formData.append("task", task);
    formData.append("file", frame);

    const response = await fetch("/detect", { method: "POST", body: formData });
    const data = await response.json();

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height); // 매 프레임 그려야 한다.

    missingList.innerHTML = "";
    const totalMissing = new Set();

    if (data.results.length === 0) {
        missingList.innerHTML = "<li>아직 탐지 전입니다</li>";
        return;
    }

    data.results.forEach(result => {
        const [x1, y1, x2, y2] = result.bbox;
        const missingItems = result.missing;

        ctx.strokeStyle = "red";
        ctx.lineWidth = 3;
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        ctx.font = "20px Arial";
        ctx.fillStyle = "red";
        ctx.fillText(missingItems.join(", ") + " 미착용", x1, y1 - 10);

        missingItems.forEach(item => totalMissing.add(item));
    });

    if (totalMissing.size === 0) {
        missingList.innerHTML = "<li>모든 장비 착용 완료</li>";
    } else {
        totalMissing.forEach(item => {
            missingList.innerHTML += `<li>${item} 미착용</li>`;
        });
    }
}

setupCamera().then(() => {
    setInterval(detectAndDraw, 2000);
});