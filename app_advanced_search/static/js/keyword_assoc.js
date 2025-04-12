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
      });
    })
    .catch((error) => console.error("Error fetching categories:", error));

  // 所有Table_清空
  function tbody_clear() {
    newsTitle_tbody.innerHTML = "";
    newsContext_tbody.innerHTML = "";
    words_tbody.innerHTML = "";
  }

  // fetch.請求資料並動作
  function assoc_sendRequest() {
    let category = selectElement.value;
    let cond =
      document.querySelector('input[name="search_type"]:checked').id || "and";
    let user_keywords = document.getElementById("tagsInput").value;
    fetch("/advanced_search/api/assoc_ana/", {
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
        tbody_clear();
        for (let i = 0; i < data.newslinks.length; i++) {
          const newCell = newsTitle_tbody.insertRow().insertCell();
          newCell.innerHTML =
            get_Tag(`${data.newslinks[i].category}`) +
            "　" +
            get_Title(data.newslinks[i].title, data.newslinks[i].link);
        }
        for (let i = 0; i < data.same_paragraph.length; i++) {
          const newCell = newsContext_tbody.insertRow().insertCell();
          newCell.innerHTML = data.same_paragraph[i];
        }
        const words = data.related_words;
        for (let i = 0; i < words.length; i += 2) {
          const newRow = words_tbody.insertRow();

          // 第1組詞語
          newRow.insertCell().innerText = words[i][0];
          newRow.insertCell().innerText = words[i][1];

          // 第2組詞語（確認存在再加）
          if (i + 1 < words.length) {
            newRow.insertCell().innerText = words[i + 1][0];
            newRow.insertCell().innerText = words[i + 1][1];
          } else {
            // 若是單數，補空欄位讓排版漂亮
            newRow.insertCell();
            newRow.insertCell();
          }
        }



        
      })
      .catch((error) => console.error("❗js錯誤:", error));
  }

  // 事件.當按下查詢按鈕時
  document.getElementById("interest_submit").addEventListener("click", function () {
    assoc_sendRequest();
  });

  // 事件.當按下清空按鈕時
  document.getElementById("interest_del").addEventListener("click", function () {
    tagsInput.removeActiveItems();
  });

  // 事件.當滑桿end時
  stepSlider.noUiSlider.on("change", function (values, handle) {
    weeks = values[handle] || 1;
  });

  // 函數.取得Tag的html代碼
  function get_Tag(category) {
    return `<div class="d-inline py-1 px-3 rounded bg-dash-dark-3 fw-bold text-sm">${category}</div>`;
  }
  // 函數.取得Title的html代碼
  function get_Title(text, href) {
    return `<a href="https://udn.com${href}"target="_blank"rel="noopener noreferrer">${text}</a>`;
  }
});
