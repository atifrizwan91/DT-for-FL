$(document).ready(function() {
});
$(function () {

    
    function updateDeviceSelection() {
        var send = {
            node: $('#select_node').val()
        };
    
        console.log(send)
        $.ajax({
            type: "GET",
            url: url_val,
            data: send,
            success: function (resp) {
                if (resp) {
                    var htmMark = '';
                    for (var i = 0; i < resp.length; i++) {
    
                        var ind = resp[i].toString().split(",")[0];
                        var val = resp[i].toString().split(",")[1];
                        console.log('the resources '+ val)
                        htmMark += "<option value=" + ind + ">" + val + "</option>";
                    }
                    //dropdown.mserv.attr('enabled', 'enabled');
                    $('#select_device').html(htmMark)
                }
            }
        });
    }
    
    // event listener to state dropdown change for node while add work
    $('#select_node').on('change', function () {
        console.log("node selection changed");
        updateDeviceSelection();
    });

});


