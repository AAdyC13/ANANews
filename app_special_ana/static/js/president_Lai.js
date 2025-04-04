document.addEventListener("DOMContentLoaded", function () {
    //初始化
    const smallBar = document.getElementById("president_smallBar").getContext("2d");
    const lineBar = document.getElementById("president_Line").getContext("2d");
    const count_art = document.getElementById("count_art")
    const count_num = document.getElementById("count_num")
    const latest_news_time = document.getElementById("latest_news_time")

    // 長條圖初始
    Chart1 = new Chart(smallBar, {
        type: "bar",
        options: {
            scales: {
                yAxes: [
                    {
                        ticks: {
                            min: 0,
                        },
                        display: false,
                    },
                ],
            },
            legend: {
                display: false,
            },
        },
        data: {
            labels: [],
            datasets: [
                {
                    data: [],

                    label: "次數",
                    backgroundColor: "#EF8C99",
                    borderColor: "#EF8C99",
                    borderWidth: 0.3,
                    barPercentage: 0.2,

                },
            ],
        },
    });

    // 點線圖初始
    Chart2 = new Chart(lineBar, {
        type: "line",
        options: {
            legend: {
                display: false,
            },
        },
        data: {
            labels: [],
            datasets: [
                {
                    data: [],
                    label: "新聞數量",
                    fill: true,
                    lineTension: 0.4,
                    backgroundColor: "rgba(134, 77, 217, 0.88)",
                    borderColor: "rgba(134, 77, 217, 0.88)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    borderWidth: 1,
                    pointBorderColor: "rgba(134, 77, 217, 0.88)",
                    pointBackgroundColor: "rgba(134, 77, 217, 0.88)",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(134, 77, 217, 0.88)",
                    pointHoverBorderColor: "rgba(134, 77, 217, 0.88)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 3,
                    pointHitRadius: 10,
                    spanGaps: false,
                }
            ],
        },


    })

    // fetch.請求資料並動作
    function president_sendRequest() {
        fetch("/special_ana/api/president_data/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        })
            .then(response => response.json())
            .then(data => {
                Chart2.data.labels = data.date;
                Chart2.data.datasets[0].data = data.y;

                Chart1.data.labels = data.BarCat;
                Chart1.data.datasets[0].data = data.BarValue;

                Chart1.update();
                Chart2.update();
                count_art.innerText = `總篇數：${data.num_occurrence}篇`;
                count_num.innerText = `總次數：${data.num_frequency}次`;
                latest_news_time.innerText = `最新收錄時間：${data.latest_news_time}`;
            })
            .catch(error => console.error("❗js錯誤:", error));
    }
    president_sendRequest()
});