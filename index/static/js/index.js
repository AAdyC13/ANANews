document.addEventListener("DOMContentLoaded",function(){
    //初始化變數
    const latest_news_time = document.getElementById("latest_news_time");
    const total_news = document.getElementById("total_news");
    const total_news_bar = document.getElementById("total_news_bar");
    

    //初始化網頁顯示內容
    fetch('/index/api/get_news_DBinfo')
    .then(response => response.json())
    .then(data => {
        latest_news_time.innerText = `最新收錄時間：${data.latest_news_time}`
        total_news.innerText= data.total_news

        total_news_bar.setAttribute("aria-valuenow", data.total_news);
        total_news_bar.setAttribute("style",`width: ${data.total_news/100}%`)
        


    })
    .catch(error => console.error("Error fetching get_latest_news_time:", error));


})