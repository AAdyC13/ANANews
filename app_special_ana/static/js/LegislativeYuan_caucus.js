document.addEventListener("DOMContentLoaded", function () {
    //初始化
    const smallBar = document.getElementById("smallBar").getContext("2d");
    const lineBar = document.getElementById("Line").getContext("2d");
    const latest_news_time = document.getElementById("latest_news_time")

    // 長條圖初始
    Chart1 = new Chart(smallBar, {
        type: "bar",
        options: {
            legend: { labels: { fontColor: "#777", fontSize: 12 } },
            scales: {
                xAxes: [
                    {
                        display: true,
                    },
                ],
                yAxes: [
                    {
                        display: true,
                    },
                ],
            },
        },
        data: {
            labels: [],
            datasets: [
                {
                    data: [],
                    label: "國民黨",
                    backgroundColor: "rgba(79, 77, 217, 0.6)",
                    borderColor: "rgba(79, 77, 217, 0.6)",
                    borderWidth: 0.3,
                    barPercentage: 0.6,

                },
                {
                    data: [],
                    label: "民進黨",
                    backgroundColor: "rgba(77, 217, 84, 0.6)",
                    borderColor: "rgba(77, 217, 84, 0.6)",
                    borderWidth: 0.3,
                    barPercentage: 0.6,

                },
                {
                    data: [],
                    label: "民眾黨",
                    backgroundColor: "rgba(77, 217, 217, 0.6)",
                    borderColor: "rgba(77, 217, 217, 0.6)",
                    borderWidth: 0.3,
                    barPercentage: 0.6,

                },
            ],
        },
    });

    // 點線圖初始
    Chart2 = new Chart(lineBar, {
        type: "line",
        options: {
            legend: { labels: { fontColor: "#777", fontSize: 12 } },
            scales: {
                xAxes: [
                    {
                        display: true,
                    },
                ],
                yAxes: [
                    {
                        display: true,
                    },
                ],
            },
        },
        data: {
            labels: [],
            datasets: [
                {
                    label: "國民黨",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(79, 77, 217, 0.6)",
                    borderColor: "rgba(79, 77, 217, 0.6)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    borderWidth: 1,
                    pointBorderColor: "rgba(79, 77, 217, 0.6)",
                    pointBackgroundColor: "rgba(79, 77, 217, 0.6)",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(79, 77, 217, 0.6)",
                    pointHoverBorderColor: "rgba(79, 77, 217, 0.6)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                    spanGaps: false,
                },
                {
                    label: "民進黨",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(77, 217, 84, 0.6)",
                    borderColor: "rgba(77, 217, 84, 0.6)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    borderWidth: 1,
                    pointBorderColor: "rgba(77, 217, 84, 0.6)",
                    pointBackgroundColor: "rgba(77, 217, 84, 0.6)",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(77, 217, 84, 0.6)",
                    pointHoverBorderColor: "rgba(77, 217, 84, 0.6)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                    spanGaps: false,
                },
                {
                    label: "民眾黨",
                    fill: true,
                    lineTension: 0.3,
                    backgroundColor: "rgba(77, 217, 217, 0.6)",
                    borderColor: "rgba(77, 217, 217, 0.6)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    borderWidth: 1,
                    pointBorderColor: "rgba(77, 217, 217, 0.6)",
                    pointBackgroundColor: "rgba(77, 217, 217, 0.6)",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(77, 217, 217, 0.6)",
                    pointHoverBorderColor: "rgba(77, 217, 217, 0.6)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [],
                    spanGaps: false,
                }
            ],
        },
    })

    // fetch.請求資料並動作
    function sendRequest_one() {
        fetch("/special_ana/api/LegislativeYuan/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        })
            .then(response => response.json())
            .then(data => {
                latest_news_time.innerText = `最新收錄時間：${data.latest_news_time}`;
                web_remaker(data);
            })
            .catch(error => console.error("❗js錯誤:", error));
    }
    sendRequest_one()

    // 函數.更新Chart
    function web_remaker(data) {
        Chart1.data.labels = data.category;
        const id_list = ["KMT", "DPP", "TPP"]
        let counter = 0;
        let isFirst = true;
        for (let word in data.df_dict) {
            each_df = data.df_dict[word];

            let occu = each_df["num_occurrence"]['全部']
            let freq = each_df["num_frequency"]['全部']
            document.getElementById(`${id_list[counter]}_count`).innerText = `總聲量：${occu}篇　${freq}次`
            const sentiRow = document.getElementById(`${id_list[counter]}_foot`);
            const spans = sentiRow.querySelectorAll("span[data-type]");
            spans.forEach(span => {
                const type = span.getAttribute("data-type");
                if (type === "good") {
                    span.innerText = `正面：${percentage_maker(each_df["sentiCount"]['Positive'], occu)}%`;
                } else if (type === "mid") {
                    span.innerText = `中立：${percentage_maker(each_df["sentiCount"]['Neutral'], occu)}%`;
                } else if (type === "bad") {
                    span.innerText = `負面：${percentage_maker(each_df["sentiCount"]['Negative'], occu)}%`;
                }
            });


            if (isFirst) {
                let time_x = [];
                for (let i = 0; i < each_df["freqByDate"].length; i++) {
                    time_x.push(each_df["freqByDate"][i]["x"])
                }
                Chart2.data.labels = time_x;
                isFirst = false;
            }

            let time_y = [];
            for (let i = 0; i < each_df["freqByDate"].length; i++) {
                time_y.push(each_df["freqByDate"][i]["y"])
            }
            Chart2.data.datasets[counter].data = time_y;

            let y = [];
            for (let each in each_df["num_occurrence"]) {
                y.push(each_df["num_occurrence"][each]);
            }
            Chart1.data.datasets[counter].data = y;
            counter += 1;
        }
        Chart1.update();
        Chart2.update();
    }
    function percentage_maker(num_1, num_2) {
        return ((num_1 / num_2) * 100).toFixed(1)
    }
});