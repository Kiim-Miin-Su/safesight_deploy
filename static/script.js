const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const output = document.getElementById("output");
const taskSelect = document.getElementById("task");
const violationsList = document.getElementById("violationsList");

let stream = null;
let detectInterval = null;

navigator.mediaDevices.getUserMedia({ video: true }).then(s => {
    stream = s;
    video.srcObject = stream;
});

document.getElementById("startBtn").addEventListener("click", () => {
    if (detectInterval) return;
    detectInterval = setInterval(sendFrame, 500); // ← 감지 주기 0.5초로 설정
});

function sendFrame() {
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append("file", blob, "frame.jpg");
        formData.append("task", taskSelect.value);

        fetch("/detect", {
            method: "POST",
            body: formData,
        })
            .then(res => res.json())
            .then(data => {
                const imageBytes = new Uint8Array(data.image.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
                const blob = new Blob([imageBytes], { type: 'image/jpeg' });
                output.src = URL.createObjectURL(blob);

                violationsList.innerHTML = "";
                data.violations.forEach(item => {
                    const li = document.createElement("li");
                    li.textContent = `Missing: ${item}`;
                    violationsList.appendChild(li);
                });
            })
            .catch(console.error);
    }, "image/jpeg");
}
