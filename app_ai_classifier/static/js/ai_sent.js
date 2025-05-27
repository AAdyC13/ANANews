document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("input");
    const example_selector = document.getElementById("example_selector");
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
        //console.log("Input Text:", inputText);
        if (!inputText) {
            alert("請輸入文字");
            return;
        }

        fetch("/app_ai_classifier/api/get_sentiment/", {
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
                got = `情緒：${data.classification}\n` +
                    `信心：${data.confidence}\n`;
                analized_results.innerText = got;


            })
            .catch(error => {
                console.error("Error:", error);
                analized_results.innerText = "發生錯誤，請稍後再試";
            });
    });

    // 範例選擇器功能
    example_selector.addEventListener("change", function () {
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.value !== "") {
            input.innerText = selectedOption.innerText.trim();
            input.value = selectedOption.innerText.trim();
        }
    });
});