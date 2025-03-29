document.addEventListener("DOMContentLoaded",function(){
    //初始化變數
    let keywordCount = 0;
    const MutiSel_category_set = document.getElementById("news_scraper_category_set");
    const NoUI_each_gatNum = document.getElementById("news_scraper_each_gatNum");
    const code_HowCat = document.getElementById("news_scraper_HowCat");
    const code_HowMany = document.getElementById("news_scraper_HowMany");
    const code_HowTime = document.getElementById("news_scraper_HowTime");

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

    //初始化網頁顯示內容
    // fetch('/index/api/get_news_DBinfo')
    // .then(response => response.json())
    // .then(data => {
    //     latest_news_time.innerText = `最新收錄時間：${data.latest_news_time}`
    //     total_news.innerText= data.total_news

    //     total_news_bar.setAttribute("aria-valuenow", data.total_news);
    //     total_news_bar.setAttribute("style",`width: ${data.total_news/100}%`)
        


    // })
    // .catch(error => console.error("Error fetching get_latest_news_time:", error));


})