document.addEventListener("DOMContentLoaded", function () {
    //初始化
    let personCount = 5;
    const tbody = document.getElementById("top_tbody");
    const selectElement = document.getElementById("person_select");
    let category = selectElement.value;

    // 關鍵字選項框初始
    fetch('/top/api/get-categories/')
        .then(response => response.json())
        .then(data => {
            
            selectElement.innerHTML = ""; // 清空原有
            let first_get_selected = true;
            data.categories.forEach(category => {
                let option = document.createElement("option");
                if(first_get_selected){option.selected = true;}
                first_get_selected = false;
                option.value = category;
                option.textContent = category;
                selectElement.appendChild(option);
            });
            person_sendRequest()
        })
        .catch(error => console.error("Error fetching categories:", error));

    // fetch.請求keyword並動作
    function person_sendRequest() {
        fetch("/top/api/person-data/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },

            body: JSON.stringify({ person_count: personCount, category: category })

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
    selectElement.addEventListener("change", function () {
        category = this.value;
        person_sendRequest()
    });
    // 事件委派.當form底下的
    document.getElementById("person_radios_row").addEventListener("change", function (event) {
        if (event.target.name === "person_radios") {
            personCount = event.target.nextElementSibling.textContent || 5;
            person_sendRequest()
            
        }
    });
})