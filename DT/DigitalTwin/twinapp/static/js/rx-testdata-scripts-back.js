$(document).ready(function () {
});

$(function () {
    if(datasets){
        datasets = JSON.parse(datasets);
        console.log(datasets[0].data);
        n = datasets[0].data.length;
        labels = Array.from({length: n}, (_, index) => index + 1);
        
        var ctx = $('#myDataChart');
        var myLineChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                title: {
                    display: true,
                    text: 'Optimization Results'
                }
            }
        });
    }


});
