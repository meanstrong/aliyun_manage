$(document).ready(function() {
    vars = get_url_vars();
    var InstanceId = vars["InstanceId"];
    $("#ExecCommand").click(function () {
        api_ExecCommand(InstanceId, $("#command").val(), function (data) {
            var output_old = $("#command_output").val();
            $("#command_output").text("$"+$("#command").val()+"\n"+data["stdout"]+data["stderr"]+output_old);
        });
    });
})
