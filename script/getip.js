/*获取User IP IPCity href
<script src="https://www.aicheteach.com/script/jquery-1.12.4.js"></script>
<script src="https://pv.sohu.com/cityjson"></script>
<script src="https://www.aicheteach.com/script/mix/getip.js"></script>
*/
function GetIP() {
        $.ajax({
        url: "//"+RequestHost+"/GetIP/",
        type: "POST",
        data: {"ip":""+returnCitySN["cip"],"ipcity":""+returnCitySN["cname"],"href":""+window.location.href},
        async: true,
        dataType: "json",
        timeout: 5000,
    });}
GetIP();
// console.log(returnCitySN["cip"]+','+returnCitySN["cname"]);