
$(document).ready(function () {


});


window.onpageshow = function (event) {
    if (event.persisted || (window.performance && window.performance.navigation.type == 2)) {
        location.reload();
    } else {
        // 새로운 페이지 로드 시
    }
}
respinfo = JSON.parse(resp);
deviceinfo = JSON.parse(device);
var mycontainer = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
var myoptions = { //지도를 생성할 때 필요한 기본 옵션
    center: new kakao.maps.LatLng(respinfo.lat, respinfo.long), //지도의 중심좌표.
    level: 3 //지도의 레벨(확대, 축소 정도)
};

var map = new kakao.maps.Map(mycontainer, myoptions); //지도 생성 및 객체 리턴
// 지도에 마커를 표시합니다 
var marker = new kakao.maps.Marker({
    map: map,
    position: new kakao.maps.LatLng(respinfo.lat, respinfo.long)
});

// 커스텀 오버레이에 표시할 컨텐츠 입니다
// 커스텀 오버레이는 아래와 같이 사용자가 자유롭게 컨텐츠를 구성하고 이벤트를 제어할 수 있기 때문에
// 별도의 이벤트 메소드를 제공하지 않습니다 
var card = `\
<div class="container-fluid">\

<div class="row">\
    <div class="col-sm-12">\
        <div class="card shadow mb-1">\
            <div class="card-header py-1 text-primary close" onclick="closeOverlay()" title="닫기">\
            <h6 class="m-0 font-weight-bold text-primary ">${deviceinfo.name}</h6>\
            </div>\
            <img src="/static/img/01.edgedevice.png" width="73" height="70">\
            <div class="card-body text-primary">\
            Device Address: ${deviceinfo.address}<hr>\
            Device Resource:${deviceinfo.resource}<hr>\
            AdminState: ${respinfo.adminState}<hr>\
            제주특별자치도 제주시 제주대학로 <hr>(우) 63243  102(아라일동 제주대학교)<hr>\ 
            </div>\
        </div>\
    </div>\
</div>\
</div>\
`;


// 마커 위에 커스텀오버레이를 표시합니다
// 마커를 중심으로 커스텀 오버레이를 표시하기위해 CSS를 이용해 위치를 설정했습니다
var overlay = new kakao.maps.CustomOverlay({
    content: card,
    map: map,
    position: marker.getPosition()
});

// 마커를 클릭했을 때 커스텀 오버레이를 표시합니다
kakao.maps.event.addListener(marker, 'click', function () {
    overlay.setMap(map);
});

// 커스텀 오버레이를 닫기 위해 호출되는 함수입니다 
function closeOverlay() {
    overlay.setMap(null);
}

statisticsInfo = JSON.parse(statistics);
statisticsInfo.forEach(statistic => {
    datasets = statistic.datasets;
    labels = statistic.labels;
    var ctx = $(`#barDataChart-${statistic.node}`);
    var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            title: {
                display: true,
                text: 'Results of '+statistic.node
            }
        }
    });
});
