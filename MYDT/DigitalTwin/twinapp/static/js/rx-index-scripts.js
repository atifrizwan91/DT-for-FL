
$(document).ready(function () {


});
var nodesStatus = JSON.parse(nodes);
var devicesStatus = JSON.parse(devices);

if (!nodesStatus.length == 0) {

    $.ajax({
        type: "GET",
        dataType: 'json',
        url: '/nodeStatus'
    }).done(function (data) {
        data.forEach(node => {
            nodeInfo = node;
            if (nodeInfo.status) {

                console.log('node name is '+nodeInfo.deviceName);
                $('#node-' + nodeInfo.deviceName).addClass('border-bottom-success');
                if ($('#node-' + node.deviceName).hasClass('border-left-primary')) {
                    $('#node-' + node.deviceName).removeClass('border-left-primary');
                }
            }
            else{
                if ($('#node-' + nodeInfo.deviceName).hasClass('border-bottom-success')) {
                    $('#node-' + nodeInfo.deviceName).removeClass('border-bottom-success');
                }
                $('#node-' + node.deviceName).addClass('border-left-primary');
            }
        });
    });
}
console.log("--------------------------")
if (!devicesStatus.length == 0) {
    // console.log(devices);
    var devicesInfo = JSON.parse(devices);
    devicesInfo.forEach(device => {

        $.ajax({
            type: "GET",
            dataType: 'json',
            data: { 'address': device.address },
            url: '/deviceStatus'
        }).done(function (data) {
            console.log('device ..... 01');
            if (data) {
                $('#device-' + device.name).addClass('border-bottom-success');
                if ($('#device-' + device.name).hasClass('border-left-primary')) {
                    $('#device-' + device.name).removeClass('border-left-primary');
                }
            } else {
                if ($('#device-' + device.name).hasClass('border-bottom-success')) {
                    $('#device-' + device.name).removeClass('border-bottom-success');
                }
                $('#device-' + device.name).addClass('border-left-primary');
            }

        });
    });

}
if (!nodesStatus.length == 0) {
    var updator = setInterval(function refresh() {

        console.log('updating the status of devices');
        $.ajax({
            type: "GET",
            dataType: 'json',
            url: '/nodeStatus'
        }).done(function (data) {
            data.forEach(node => {
                nodeInfo = node;
                if (nodeInfo.status) {
    
                    console.log('node name is '+nodeInfo.deviceName);
                    $('#node-' + nodeInfo.deviceName).addClass('border-bottom-success');
                    if ($('#node-' + node.deviceName).hasClass('border-left-primary')) {
                        $('#node-' + node.deviceName).removeClass('border-left-primary');
                    }
                }
                else{
                    if ($('#node-' + nodeInfo.deviceName).hasClass('border-bottom-success')) {
                        $('#node-' + nodeInfo.deviceName).removeClass('border-bottom-success');
                    }
                    $('#node-' + node.deviceName).addClass('border-left-primary');
                }
            });

        });
        console.log("--------------------------")
        if (devices) {
            // console.log(devices);
            var devicesInfo = JSON.parse(devices);
            devicesInfo.forEach(device => {

                $.ajax({
                    type: "GET",
                    dataType: 'json',
                    data: { 'address': device.address },
                    url: '/deviceStatus'
                }).done(function (data) {
                    console.log('device .....');
                    if (data) {
                        $('#device-' + device.name).addClass('border-bottom-success');
                        if ($('#device-' + device.name).hasClass('border-left-primary')) {
                            $('#device-' + device.name).removeClass('border-left-primary');
                        }
                    } else {
                        if ($('#device-' + device.name).hasClass('border-bottom-success')) {
                            $('#device-' + device.name).removeClass('border-bottom-success');
                        }
                        $('#device-' + device.name).addClass('border-left-primary');
                    }

                });
            });

        }
    }, 3000);
}

window.onpageshow = function (event) {
    if (event.persisted || (window.performance && window.performance.navigation.type == 2)) {
        location.reload();
    } else {
        // 새로운 페이지 로드 시
    }
}

if (!nodesStatus.length == 0) {
    var nodesInfo2 = JSON.parse(nodes);
    nodesInfo2.forEach(node => {

        tippy('#i-node-' + node.name, {

            content: 'Loading...',
            allowHTML: true,
            onShow(instance) {
                $.ajax({
                    type: "GET",
                    dataType: 'json',
                    url: `/nodeInfo/${node.name}`
                }).done(function (data) {
                    console.log(data);

                    console.log('#i-node-' + node.name);
                    var card = `\
                    <div class="container-fluid">\
                
                    <div class="row">\
                        <div class="col-sm-12">\
                            <div class="card shadow mb-1">\
                                <div class="card-header py-1 text-primary">\
                                <h6 class="m-0 font-weight-bold text-primary">${node.name}</h6>\
                                </div>\
                                <div class="card-body text-primary">\
                                    ${data.node}\
                                    ${data.device}\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                </div>\
                    `;
                    instance.setContent(card);

                });
            },
        });
    });
}
if (!devicesStatus.length == 0) {
    var devicessInfo2 = JSON.parse(devices);
    devicessInfo2.forEach(device => {

        tippy('#i-device-' + device.name, {

            content: 'Loading...',
            allowHTML: true,
            onShow(instance) {
                $.ajax({
                    type: "GET",
                    dataType: 'json',
                    url: `/deviceProfileInfo/${device.name}`
                }).done(function (data) {
                    console.log(data);

                    console.log('#i-device-' + device.name);
                    var card = `\
                    <div class="container-fluid">\
                
                    <div class="row">\
                        <div class="col-sm-12">\
                            <div class="card shadow mb-1">\
                                <div class="card-header py-1 text-primary">\
                                <h6 class="m-0 font-weight-bold text-primary">${device.name}</h6>\
                                </div>\
                                <div class="card-body text-primary">\
                                    ${data.device}\
                                    ${data.node}\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                </div>\
                    `;
                    instance.setContent(card);

                });
            },
        });
    });
}
$('div.device-click').bind('click', function () {
    id = $(this).attr('id');
    console.log(id);
    window.location.href = `/deviceInfo/${id}`;
});
$('div.node-click').bind('click', function () {
    id = $(this).attr('id');
    console.log(id);
    window.location.href = `/getEdgeNodeInfo/${id}`;
});
