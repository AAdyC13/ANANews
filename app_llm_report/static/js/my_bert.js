document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("input");
    const interest_del = document.getElementById("interest_del");
    const interest_submit = document.getElementById("interest_submit");
    const analized_results = document.getElementById("analized_results");

    // 清空按鈕功能
    interest_del.addEventListener("click", function () {
        input.value = "";
    });

    // 提交按鈕功能
    interest_submit.addEventListener("click", function () {
        const inputText = input.value.trim();
        if (!inputText) {
            alert("請輸入文字");
            return;
        }

        fetch("/llm_report/api/my_bert_ana/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: inputText })
        })
            .then(response => response.json())
            .then(data => {
                let got;
                analized_results.innerText = ""; // 清空之前的結果
                for (const [key, value] of Object.entries(data.data)) {
                    got = `${key}: ${value}\n`;
                    analized_results.innerText += got;
                };


            })
            .catch(error => {
                console.error("Error:", error);
                analized_results.innerText = "發生錯誤，請稍後再試";
            });
    });
});