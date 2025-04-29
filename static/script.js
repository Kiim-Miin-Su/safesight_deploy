const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const violationsList = document.getElementById('violations');
const taskSelect = document.getElementById('task');

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        console.error("카메라 접근 실패:", error);
    }
}

async function sendFrame() {
    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);

    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
    const formData = new FormData();
    formData.append('file', blob, 'frame.jpg');
    formData.append('task', taskSelect.value);

    try {
        const response = await fetch('/detect', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        // 서버에서 받은 hex 인코딩 이미지를 base64로 변환
        const hexString = result.image;
        const base64String = btoa(
            hexString.match(/.{1,2}/g)
                .map(byte => String.fromCharCode(parseInt(byte, 16)))
                .join('')
        );

        const img = new Image();
        img.src = 'data:image/jpeg;base64,' + base64String;
        img.onload = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
        };

        // 미착용 리스트 표시
        violationsList.innerHTML = '';
        if (result.violations.length > 0) {
            result.violations.forEach(v => {
                const li = document.createElement('li');
                li.innerText = v;
                violationsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.innerText = '모든 장비 착용 완료';
            violationsList.appendChild(li);
        }

    } catch (error) {
        console.error('서버 통신 오류:', error);
    }
}

startCamera();

// 2초마다 서버에 프레임 전송
setInterval(sendFrame, 2000);
