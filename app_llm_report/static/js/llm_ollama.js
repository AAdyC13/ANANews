document.addEventListener("DOMContentLoaded", function () {
  //初始化
  const selectElement = document.getElementById("keyword_select");
  let weeks = 1;
  const lineBar = document.getElementById("sentiment_barChart").getContext("2d");
  const pieChart = document.getElementById("sentiment_pieChart").getContext("2d");
  const newsCount_tbody = document.getElementById("interest_newsCount_tbody");

  // 滑桿初始
  var stepSlider = document.getElementById("week_NoUISlider");
  if (stepSlider) {
    noUiSlider.create(stepSlider, {
      behaviour: "tap-drag",
      format: wNumb({ decimals: 0 }),
      pips: { mode: "steps", stepped: true, density: 20 },
      tooltips: true,
      connect: "lower",
      start: [1],
      step: 1,
      range: { min: 1, max: 6 },
    });
  }
  // tage輸入框初始
  const tagsInput = new Choices("#tagsInput", {
    delimiter: ",",
    editItems: true,
    removeItemButton: true,
    addItemText: (value) => `請按「Enter」鍵選擇：${value}`,
  });
  document.querySelector(".choices__inner").classList.add("form-control");

  // 關鍵字類別選項框、按類統計初始
  fetch("/top/api/get-categories/")
    .then((response) => response.json())
    .then((data) => {
      selectElement.innerHTML = ""; // 清空原有
      tbody_clear();

      let first_get_selected = true;
      data.categories.forEach((category) => {
        let option = document.createElement("option");
        if (first_get_selected) {
          option.selected = true;
        }
        first_get_selected = false;
        option.value = category;
        option.textContent = category;
        selectElement.appendChild(option);
        tbody_category(category);
      });
    })
    .catch((error) => console.error("Error fetching categories:", error));

  // 所有Table_清空
  function tbody_clear() {
    newsCount_tbody.innerHTML = "";
  }

  // 兩個Table_初始化類別
  function tbody_category(category) {
    let rowA = newsCount_tbody.insertRow();
    rowA.insertCell(0).innerText = category
    rowA.insertCell(1).innerText = ""
  }

  // fetch. userInterest請求資料並動作
  function interest_sendRequest() {
    let category = selectElement.value;
    let cond = document.querySelector('input[name="search_type"]:checked').id || "and"
    let user_keywords = document.getElementById("tagsInput").value
    fetch("/advanced_search/api/interest-data/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },

      body: JSON.stringify({ user_keywords: user_keywords, cond: cond, category: category, weeks: weeks })

    })
      .then(response => response.json())
      .then(data => {
        let date = data.date;
        let y = data.y;
        let wordCount = data.wordCount;
        let newsCount = data.newsCount;
        window.top.myChart.data.labels = date;
        window.top.myChart.data.datasets[0].data = y;
        window.top.myChart.update();
        for (let i = 0; i < wordCount.length; i++) {
          newsCount_tbody.rows[i].cells[1].innerText = newsCount[i];
        }
      })
      .catch(error => console.error("❗js錯誤:", error));
  }

  // fetch. sentiment請求資料並動作
  function sentiment_sendRequest() {
    let category = selectElement.value;
    let cond =
      document.querySelector('input[name="search_type"]:checked').id || "and";
    let user_keywords = document.getElementById("tagsInput").value;
    fetch("/advanced_search/api/sentiment_ana/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },

      body: JSON.stringify({
        user_keywords: user_keywords,
        cond: cond,
        category: category,
        weeks: weeks,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        Chart2.data.labels = data.x;
        Chart2.data.datasets[0].data = data.y_pos;
        Chart2.data.datasets[1].data = data.y_neg;
        Chart2.update();
        pieData = []
        counter = 0;
        for (i in data.sentiCount) {
          pieData.push(data.sentiCount[i])
          counter += data.sentiCount[i]
        }
        Chart1.data.datasets[0].data = pieData;
        Chart1.update();
        pos.innerText = `正面:${data.sentiCount["Positive"]}篇`;
        neg.innerText = `負面:${data.sentiCount["Negative"]}篇`;
        midd.innerText = `中立:${data.sentiCount["Neutral"]}篇`;
        all.innerText = `總和:${counter}篇`;
      })
      .catch((error) => console.error("❗js錯誤:", error));
  }
  // fetch.請求資料並動作
  function ollama_sendRequest() {
    let category = selectElement.value;
    let cond =
      document.querySelector('input[name="search_type"]:checked').id || "and";
    let user_keywords = document.getElementById("tagsInput").value;
    fetch("/llm_report/api/ollama_request/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },

      body: JSON.stringify({
        user_keywords: user_keywords,
        cond: cond,
        category: category,
        weeks: weeks,
      }),
    })
      .then((response) => response.json())
      .then((data) => { })


      .catch((error) => console.error("❗js錯誤:", error));
  }

  // 事件.當按下查詢按鈕時
  document.getElementById("interest_submit").addEventListener("click", function () {
    sentiment_sendRequest();
    interest_sendRequest();
    ollama_sendRequest();
  });

  // 事件.當按下清空按鈕時
  document.getElementById("interest_del").addEventListener("click", function () {
    tagsInput.removeActiveItems();
  });

  // 事件.當滑桿end時
  stepSlider.noUiSlider.on("change", function (values, handle) {
    weeks = values[handle] || 1;
  });
  // 圓餅圖初始
  var Chart1 = new Chart(pieChart, {
    responsive: true,
    type: "pie",
    options: {
      legend: {
        display: true,
        position: "left",
      },
    },
    data: {
      labels: ["正面", "負面", "中立"],
      datasets: [
        {
          data: [],
          borderWidth: 0,
          backgroundColor: ["#a678eb", "#9762e6", "#864DD9"],
          hoverBackgroundColor: ["#a678eb", "#9762e6", "#864DD9"],
        },
      ],
    },
  });

  // 正反面折線圖初始
  var Chart2 = new Chart(lineBar, {
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
          label: "正面",
          fill: true,
          lineTension: 0.3,
          backgroundColor: "rgba(134, 77, 217, 0.6)",
          borderColor: "rgba(134, 77, 217,0.6)",
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0.0,
          borderJoinStyle: "miter",
          borderWidth: 1,
          pointBorderColor: "rgba(134, 77, 217, 0.6)",
          pointBackgroundColor: "rgba(134, 77, 217, 0.6)",
          pointBorderWidth: 1,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(134, 77, 217, 0.6)",
          pointHoverBorderColor: "rgba(134, 77, 217, 0.6)",
          pointHoverBorderWidth: 2,
          pointRadius: 1,
          pointHitRadius: 10,
          data: [],
          spanGaps: false,
        },
        {
          label: "負面",
          fill: true,
          lineTension: 0.3,
          backgroundColor: "rgba(98, 98, 98, 0.7)",
          borderColor: "rgba(98, 98, 98, 0.7)",
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0.0,
          borderJoinStyle: "miter",
          borderWidth: 1,
          pointBorderColor: "rgba(98, 98, 98, 0.7)",
          pointBackgroundColor: "rgba(98, 98, 98, 0.7)",
          pointBorderWidth: 1,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(98, 98, 98, 0.7)",
          pointHoverBorderColor: "rgba(98, 98, 98, 0.7)",
          pointHoverBorderWidth: 2,
          pointRadius: 1,
          pointHitRadius: 10,
          data: [],
          spanGaps: false,
        }
      ],
    },
  });

  // 折線圖初始
  window.top = window.top || {};
  var ctx = document.getElementById("keyword_barChart").getContext("2d");
  window.top.myChart = new Chart(ctx, {
    type: "line",
    options: {
      responsive: true,
      legend: { labels: { fontColor: "#777", fontSize: 12 } },
    },
    data: {
      labels: [],
      datasets: [
        {
          label: "新聞數量",
          fill: true,
          lineTension: 0.5,
          backgroundColor: "rgba(134, 77, 217, 0.88)",
          borderColor: "rgba(134, 77, 217, 088)",
          borderCapStyle: "butt",
          borderDash: [],
          borderDashOffset: 0.0,
          borderJoinStyle: "miter",
          borderWidth: 1,
          pointBorderColor: "rgba(134, 77, 217, 0.88)",
          pointBackgroundColor: "#fff",
          pointBorderWidth: 1,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(134, 77, 217, 0.88)",
          pointHoverBorderColor: "rgba(134, 77, 217, 0.88)",
          pointHoverBorderWidth: 2,
          pointRadius: 1,
          pointHitRadius: 10,
          data: [],
          spanGaps: false,
        }
      ],
    },
  });
});
