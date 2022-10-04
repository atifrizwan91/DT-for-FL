
$(document).ready(function () {
    $.ajax({
        type: "GET",
        dataType: 'json',
        url: '/getstatusoffl'
    }).done(function (data) {
        if (data) {
            for( n in data){
                console.log('the status is');
                console.log(data[n].status);
                if(data[n].status){
                    $('#lmapid-' + data[n].id).text('Operating');
                    $('#lmapid-' + data[n].id).addClass('btn-danger');
                    $('#spinner-lmapid-' + data[n].id).show();
                }else{
                    $('#lmapid-' + data[n].id).text('Operate');
                    $('#lmapid-' + data[n].id).removeClass('btn-danger');
                    $('#spinner-lmapid-' + data[n].id).hide();
                }
                
            }
            
        }
    });
});
window.onpageshow = function (event) {
    if (event.persisted || (window.performance && window.performance.navigation.type == 2)) {
        location.reload();
    } else {
        // 새로운 페이지 로드 시
    }
}

$(function () {
    $('a.operate').bind('click', function () {
        var option = $(this).text();
        id = $(this).attr('id');
        console.log("the status is " + option)
        if (option === 'Operating') {
            $(this).text('Operate');
            $(this).removeClass('btn-danger');
            $('#spinner-' + id).hide();
            $.ajax({
                type: "GET",
                dataType: 'json',
                data: { 'id': id, 'status': 0 },
                crossDomain: true,
                url: '/activatefl'
            }).done(function (data) {
                location.reload();
            });
        } else {
            $(this).text('Operating');
            $('#spinner-' + id).show();
            $.ajax({
                type: "GET",
                dataType: 'json',
                data: { 'id': id, 'status': 1 },
                crossDomain: true,
                url: '/activatefl'
            }).done(function (data) {

                if (data) {
                    // $('#spinner-' + id).parent().next().html("Reading Time: " + data[0].timestamp + "<br />Sensor Value: " + data[1].sensor_val);
                    // $('#' + id).text('Operate');
                    $('#' + id).addClass('btn-danger');
                    // $('#' + id).attr('href', '#');
                    location.reload();
                }
            })
        }
        return false;
    });

});
