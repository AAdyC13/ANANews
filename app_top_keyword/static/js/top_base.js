document.addEventListener("DOMContentLoaded", function () {
    // 長條圖初始
    window.top = window.top || {};
    var ctx = document.getElementById("keyword_barChart").getContext("2d");
    window.top.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: '次數',
                data: [],
                backgroundColor: 'rgb(133, 77, 217)',
                borderColor: "rgba(134, 77, 217, 088)",
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                borderWidth: 1,
                spanGaps: false,
            }]
        },
        options: { responsive: true }
    });


})