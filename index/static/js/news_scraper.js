document.addEventListener("DOMContentLoaded", function () {
    //初始化變數
    let each_Num = 0;
    let categorys = [];
    const NoUI_each_gatNum = document.getElementById("news_scraper_each_gatNum");
    const code_HowCat = document.getElementById("news_scraper_HowCat");
    const code_HowMany = document.getElementById("news_scraper_HowMany");
    const spen_HowTime = document.getElementById("news_scraper_HowTime");
    const categorys_select = document.getElementById("news_scraper_category_set");
    const logDiv = document.getElementById("log-output");
    // 與asgi伺服器建立連線
    const scraper_socket = new WebSocket("ws://127.0.0.3:8001/ws/celery-logs/");
    const button_sews_scraper_start = document.getElementById("news_scraper_start")
    const shower_news_scraper_isWork = document.getElementById("news_scraper_isWork")

    //初始爬蟲工作確認
    fetch('/index/api/check_scraper_isWork/')
        .then(response => response.json())
        .then(data => {
            scraper_isWork(data.Response)
        })
        .catch(error => console.error("爬蟲工作確認器錯誤:", error));

    //爬蟲工作顯示變更器
    function scraper_isWork(bool) {
        if (bool) {
            button_sews_scraper_start.disabled = true
            shower_news_scraper_isWork.innerText = "工作中🟢"
        } else {
            button_sews_scraper_start.disabled = false
            shower_news_scraper_isWork.innerText = "未啟動🔴"
        }
    }

    // 滑桿初始
    if (NoUI_each_gatNum) {
        noUiSlider.create(NoUI_each_gatNum, {
            behaviour: 'tap-drag',
            format: wNumb({ decimals: 0 }),
            pips: { mode: 'steps', stepped: true, density: 100 },
            //tooltips: true,
            connect: 'lower',
            start: [0],
            step: 1,
            range: { 'min': 0, 'max': 20 }
        });
    }

    // 多重選項框初始
    fetch('/top/api/get-categories/')
        .then(response => response.json())
        .then(data => {
            categorys_select.innerHTML = ""; // 清空默認
            data.categories.forEach(category => {
                if (category != "全部") {
                    let option = document.createElement("option");
                    option.value = category;
                    option.textContent = category;
                    option.selected = true;
                    categorys_select.appendChild(option);
                }
            });
            multi(categorys_select, {
                enable_search: false,
                non_selected_header: "未選區",
                selected_header: "已選區",
                "limit": -1,
                "limit_reached": function () { },
                "hide_empty_groups": true,
            });
            categorys = Array.from(categorys_select.selectedOptions).map(option => option.value);
            calculate_crawl_estimation()
        })
        .catch(error => console.error("多重選項框初始錯誤:", error));


    // 更新爬蟲預測欄
    function calculate_crawl_estimation() {
        code_HowCat.innerText = categorys.length
        code_HowMany.innerText = each_Num
        loading_time = each_Num > 0 ? categorys.length * 10 : 0
        second_calcu = categorys.length * each_Num * 10 + loading_time
        if (second_calcu < 60) {
            spen_HowTime.innerHTML = `預計耗時
                <code >${second_calcu}</code>秒`
        } else {
            spen_HowTime.innerHTML = `預計耗時 <code>${Math.floor(second_calcu / 60)}</code> 分 <code>${second_calcu % 60}</code> 秒`;
        }
    }

    // 事件.當按下取消已選類別按鈕時
    document.getElementById("news_scraper_category_reset").addEventListener("click", function () {
        categorys_select.querySelectorAll("select option").forEach(opt => opt.selected = false);
        categorys_select.dispatchEvent(new Event("change"));
        //scraper_isWork(false)
    });

    // 事件.當按下啟動按鈕時
    button_sews_scraper_start.addEventListener("click", function () {
        scraper_isWork(true)
        fetch('/index/api/news_scraper_start/', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ categorys: categorys, each_Num: each_Num })
        })
            .then(response => response.json())
            .then(data => {
                console.log(data.Response)
            })
            .catch(error => console.error("事件.當按下啟動按鈕時錯誤:", error));

    });

    // 事件.當選擇框change時
    categorys_select.addEventListener("change", function () {
        categorys = Array.from(categorys_select.selectedOptions).map(option => option.value);
        calculate_crawl_estimation()
    });

    // 事件.當滑桿end時
    NoUI_each_gatNum.noUiSlider.on("change", function (values, handle) {
        each_Num = values[handle] || 0;
        calculate_crawl_estimation()
    });


    // WebSocket有新消息時
    scraper_socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (typeof data.message === "string") {
            logDiv.innerText += `\n`;
            logDiv.innerText += `${data.message}`;  // 更新前端顯示
            logDiv.scrollTop = logDiv.scrollHeight;
        }
        // 檢測是否為dict
        if (typeof data.message === "object" && data.message !== null && !Array.isArray(data.message)) {
            scraper_isWork(data.message["bool"]);
        }

    };

    // WebSocket狀態顯示
    scraper_socket.onopen = function () {
        console.log("✅WebSocket 連線成功！");
    };
    scraper_socket.onclose = function (event) {
        console.log("❗WebSocket已關閉");
    };


})