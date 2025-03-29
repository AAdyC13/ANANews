document.addEventListener("DOMContentLoaded", function () {
    //初始化
    let category = document.getElementById("keyword_select").value;
    let keywordCount = 0;
    const tbody = document.getElementById("top_tbody");

    // 滑桿初始
    var stepSlider = document.getElementById("keyword_maxNum_NoUISlider");
    if (stepSlider) {
        noUiSlider.create(stepSlider, {
            behaviour: 'tap-drag',
            format: wNumb({ decimals: 0 }),
            pips: { mode: 'steps', stepped: true, density: 8 },
            tooltips: true,
            connect: 'lower',
            start: [0],
            step: 5,
            range: { 'min': 0, 'max': 100 }
        });
    }

    // 關鍵字選項框初始
    fetch('/top/api/get-categories/')
    .then(response => response.json())
    .then(data => {
        const selectElement = document.getElementById("keyword_select");
        selectElement.innerHTML = ""; // 清空原有

        data.categories.forEach(category => {
            let option = document.createElement("option");
            option.value = category;
            option.textContent = category;
            selectElement.appendChild(option);
        });
    })
    .catch(error => console.error("Error fetching categories:", error));

    // fetch.請求keyword並動作
    function keyword_sendRequest() {
        fetch("/top/api/chart-data/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            
            body: JSON.stringify({ keyword_count: keywordCount, category: category })

        })
            .then(response => response.json())
            .then(data => {
                let words = data.words;
                let counts = data.counts;
                window.top.myChart.data.labels = words;
                window.top.myChart.data.datasets[0].data = counts;
                window.top.myChart.update();
                tbody.innerHTML = "";
                for (let i = 0; i < words.length; i++) {
                    let row = tbody.insertRow();
                    row.insertCell(0).innerText = i + 1; // 序號
                    row.insertCell(1).innerText = words[i]; // 關鍵字
                    row.insertCell(2).innerText = counts[i]; // 次數
                }
            })
            .catch(error => console.error("❗js錯誤:", error));
    }
    // 事件.當選擇框change時
    document.getElementById("keyword_select").addEventListener("change", function () {
        category = this.value;
        keyword_sendRequest()
    });

    // 事件.當滑桿end時
    stepSlider.noUiSlider.on("change", function (values, handle) {
        keywordCount = values[handle] || 0;
        keyword_sendRequest()
    });
});