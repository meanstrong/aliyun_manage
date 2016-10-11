function check_return(data){
    if (data.hasOwnProperty("Code")) {
        alert("操作失败 "+data["Code"]+" : "+data["Message"]);
    }
}

function api_CreateInstance(callback) {
    var url = "/api/aliyun?Action=CreateInstance";
    $.get(url, callback, "json");
}

function api_DescribeInstances(callback) {
    var url = "/api/aliyun?Action=DescribeInstances";
    $.get(url, callback, "json");
}

function api_StartInstance(InstanceId, callback) {
    var url = "/api/aliyun?Action=StartInstance&InstanceId="+InstanceId;
    $.get(url, callback, "json");
}

function api_StopInstance(InstanceId, callback) {
    var url = "/api/aliyun?Action=StopInstance&InstanceId="+InstanceId;
    $.get(url, callback, "json");
}

function api_DeleteInstance(InstanceId, callback) {
    var url = "/api/aliyun?Action=DeleteInstance&InstanceId="+InstanceId;
    $.get(url, callback, "json");
}

function api_DescribeInstanceVncUrl(InstanceId, callback) {
    var url = "/api/aliyun?Action=DescribeInstanceVncUrl&InstanceId="+InstanceId;
    $.get(url, callback, "json");
}

function api_ExecCommand(InstanceId, command, callback) {
    var url = "/api/aliyun/exec_command?InstanceId="+InstanceId;
    $.post(url, {"command": command}, callback, "json");
}

function get_url_vars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }       
    var hashes = window.location.pathname.slice(1).split('/');
    for (var i = 0; i < hashes.length-1; i++) {
        vars.push(hashes[i]);
        vars[hashes[i]] = hashes[i+1];
    }         
    return vars;
}
