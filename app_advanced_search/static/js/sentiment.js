document.addEventListener("DOMContentLoaded", function () {
  //初始化
  const newsTitle_tbody = document.getElementById("assoc_newsTitle_tbody");
  const newsContext_tbody = document.getElementById("assoc_newsContext_tbody");
  const words_tbody = document.getElementById("assoc_words_tbody");
  const selectElement = document.getElementById("keyword_select");
  let weeks = 1;

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
      });
    })
    .catch((error) => console.error("Error fetching categories:", error));

  // fetch.請求資料並動作
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
      })
      .catch((error) => console.error("❗js錯誤:", error));
  }

  // 事件.當按下查詢按鈕時
  document.getElementById("interest_submit").addEventListener("click", function () {
    sentiment_sendRequest();
  });

  // 事件.當按下清空按鈕時
  document.getElementById("interest_del").addEventListener("click", function () {
    tagsInput.removeActiveItems();
  });

  // 事件.當滑桿end時
  stepSlider.noUiSlider.on("change", function (values, handle) {
    weeks = values[handle] || 1;
  });

});
