$(document).ready(function() {
    api_DescribeInstances(function (data) {
        check_return(data);
        var instances = data["Instances"]["Instance"];
        $.each(instances, function(i, n) {
            var tr = $("<tr></tr>");
            tr.append($("<td></td>").text(n["InstanceId"]));
            tr.append($("<td></td>").text(n["PublicIpAddress"]["IpAddress"][0]));
            tr.append($("<td></td>").text(n["Status"]));
            var action_td = $("<td></td>");
            action_td.append($("<a href=\"javascript:void(0)\" InstanceId="+n["InstanceId"]+" class=\"StartInstance\">Start</a>"));
            action_td.append($("<span class=\"cut-line\" style=\"margin-right: 5px;margin-left: 5px;\">¦</span>"));
            action_td.append($("<a href=\"javascript:void(0)\" InstanceId="+n["InstanceId"]+" class=\"StopInstance\">Stop</a>"));
            action_td.append($("<span class=\"cut-line\" style=\"margin-right: 5px;margin-left: 5px;\">¦</span>"));
            action_td.append($("<a href=\"javascript:void(0)\" InstanceId="+n["InstanceId"]+" class=\"DeleteInstance\">Delete</a>"));
            action_td.append($("<span class=\"cut-line\" style=\"margin-right: 5px;margin-left: 5px;\">¦</span>"));
            action_td.append($("<a href=\"/send_file?InstanceId="+n["InstanceId"]+"\" target=\"_blank\">SendFile</a>"));
            action_td.append($("<span class=\"cut-line\" style=\"margin-right: 5px;margin-left: 5px;\">¦</span>"));
            action_td.append($("<a href=\"/exec_command?InstanceId="+n["InstanceId"]+"\" target=\"_blank\">ExecCommand</a>"));
            tr.append(action_td);
            $("table tbody").append(tr);
        });
    });

    $("#CreateInstance").click(function () {
        $(this).attr('disabled',"true");
        api_CreateInstance(function (data) {
            check_return(data);
            window.location.assign('/')
        });
    });

    $("tbody").delegate(".StartInstance", "click", function () {
        var InstanceId = $(this).attr("InstanceId");
        api_StartInstance(InstanceId, function (data) {
            check_return(data);
            window.location.reload();
        });
    });
    $("tbody").delegate(".StopInstance", "click", function () {
        var InstanceId = $(this).attr("InstanceId");
        api_StopInstance(InstanceId, function (data) {
            check_return(data);
            window.location.reload();
        });
    });
    $("tbody").delegate(".DeleteInstance", "click", function () {
        var InstanceId = $(this).attr("InstanceId");
        api_DeleteInstance(InstanceId, function (data) {
            check_return(data);
            window.location.reload();
        });
    });
})
