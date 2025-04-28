const alertBox = document.getElementById("alert-box");
const violationList = document.getElementById("violation-list");

function updateDetectionStatus() {
    fetch("/detect_result")
        .then(response => response.json())
        .then(data => {
            if (data.violation_count > 0) {
                alertBox.classList.remove("hidden");

                // 목록 갱신
                violationList.innerHTML = "";
                if (data.labels) {
                    data.labels.forEach(label => {
                        const li = document.createElement("li");
                        li.textContent = label;
                        violationList.appendChild(li);
                    });
                }
            } else {
                alertBox.classList.add("hidden");
                violationList.innerHTML = "";
            }
        })
        .catch(err => {
            console.error("감지 상태 가져오기 실패:", err);
        });
}

setInterval(updateDetectionStatus, 2000);
