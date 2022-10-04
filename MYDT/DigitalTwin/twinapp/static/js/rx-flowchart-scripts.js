
$(document).ready(function () {
});
jsPlumb.ready(function () {

    jsPlumb.setContainer($('#for-edge-device'));
    var common = {
        anchor: "Continuous",
        endpoint: ["Rectangle", { width: 20, height: 20 }],
        paintStyle: { fill: "gray", stroke: "gray", strokeWidth: 3 }
    };
    var i = 0;
    var source_ids = [];
    var target_ids = [];

    source = [];
    target = [];

    $('.task-item').each(function () {
        source.push(this.id)
    });

    $('.vo-item').each(function () {
        target.push(this.id)
    });

    console.log(source)


    jsPlumb.makeSource(source, {
        connector: 'StateMachine'
    }, common);
    jsPlumb.makeTarget(target, {
        connector: 'StateMachine',
        allowLoopback: true,
        maxConnection: 3,
        isTarget: true,
        overlays: [
            ["Arrow", { width: 12, length: 12, location: 0.67 }]
        ]
    }, common);
    var rep;
    jsPlumb.bind('connection', function (info) {
        console.log("before posting");
        // rep = $.get(save_url_val, { from: info.sourceId.split("-")[1], to: info.targetId.split("-")[1] });
        var conn = info;
        $.ajax({
            type: "GET",
            dataType: 'json',
            data: { from: info.sourceId.split("-")[1], to: info.targetId.split("-")[1] },
            crossDomain: true,
            url: save_url_val
        }).done(function (data) {
            if (data) {
                console.log(data.resp)
                if (data.resp === 0) {
                    var con = jsPlumb.getConnections({
                        source: conn.sourceId,
                        target: conn.targetId
                    });
                    if (con[0]) {
                        jsPlumb.deleteConnection(con[0]);
                    }
                }
            }
        }).fail(function (data) {

        });
    });
    jsPlumb.bind('connectionDetached', function (info) {
        console.log(info.targetId);
        console.log(info.sourceId);

        // after detaching Connection manually:
        // info.targetId === the source Element's jsPlumb DOM ID

        // after programmatically cancelling a Connection:
        // info.targetId === the source Endpoint's dragid DOM attribute
    });


});







