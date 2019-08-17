page=100;//默认page==100 即登录后返回当前页面
function getURL(name) {
var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
var r = window.location.search.substr(1).match(reg);
if (r != null) {
    return unescape(r[2]);
}
return null;
}
function tipssuccess(uname) {
     $('.tips').initTips({
				title: "友情提示", // head头部显示的标题内容
                message:"尊敬的"+uname+":<br><p>欢迎访问山东理工大学新闻网</p>",// 内容区域 动态生成div时,将根据ajax获取的数据并拼接好的html字符串放到此处即可
				duration:10000, // 提示框停留时间(毫秒为单位)  默认值为5000ms
				space:10, // 通知窗之间上下间隔 单位px(默认值为8)
				firstSpace:8, // 第一个提示框距离页面 上方或(下,左,右)的距离 (默认值为8)
				margin:15, // 提示框 距离左右两边的距离 (默认值15px)
				toastType:'success',// 提示类型 有四个样式可选 info warning error success(默认info)
				width:350, // 提示框宽度,默认为auto不换行
				limit:1, // 限制提示框数量(默认值为4)
				timingFun:'linear',// 动画运动曲线(默认值为ease)
				direction:'right bottom', // 提示框滑出方向默认right bottom
				type:'click', // 触发方式(内容区域)
				//上方type属性的事件触发后的回调函数
                action: function () {

                }
			});
}
function tipsinfo() {
     $('.tips').initTips({
				title: "友情提示", // head头部显示的标题内容
                message:"<p>系统检测到您未在本系统注册登录，是否登录？<br></br>点我登录</p>",// 内容区域 动态生成div时,将根据ajax获取的数据并拼接好的html字符串放到此处即可
				duration:500000, // 提示框停留时间(毫秒为单位)  默认值为5000ms
				space:10, // 通知窗之间上下间隔 单位px(默认值为8)
				firstSpace:8, // 第一个提示框距离页面 上方或(下,左,右)的距离 (默认值为8)
				margin:15, // 提示框 距离左右两边的距离 (默认值15px)
				toastType:'info',// 提示类型 有四个样式可选 info warning error success(默认info)
				width:350, // 提示框宽度,默认为auto不换行
				limit:1, // 限制提示框数量(默认值为4)
				timingFun:'linear',// 动画运动曲线(默认值为ease)
				direction:'right bottom', // 提示框滑出方向默认right bottom
				type:'click', // 触发方式(内容区域)
				//上方type属性的事件触发后的回调函数
                action: function () {
                    if(page==100){
                        window.location.assign("//"+RequestHost+"/Loginpage/?page="+page+"&to="+document.location.protocol+"//"+document.location.hostname+document.location.pathname);
                    }else{
                        window.location.assign("//"+RequestHost+"/Loginpage/?page="+page);
                    }
                }
			});
}
function SetCookie(params){
    $.ajax({
        url: "//"+RequestHost+"/SetCookie/",
        type: "POST",
        data: {"params":params},
        async: true,
        dataType: "json",
        timeout: 5000,
        success: function(data) {
            // console.log(data);
            if(data['code'] == 1){
                 $.cookie('cookieid', data['cookieid'], { expires: 7, path: '/' });
            }
        },
        error: function(e) {
            console.log(e);
        }
    });
}
function GetCookie(cid,page){
    $.ajax({
        url: "//"+RequestHost+"/GetCookie/",
        type: "POST",
        data: {"cid":cid},
        async: true,
        dataType: "json",
        timeout: 5000,
        success: function(data) {
            // console.log(data);
            if(data['code'] == 1){
                tipssuccess(data['umane']);
            }else{
                  tipsinfo();
             }
        },
        error: function(e) {
            console.log(e);
        }
    });
}
function checkCookie(page) {
    if(params==undefined&&($.cookie('cookieid')==undefined||$.cookie('cookieid')=='null')){
        tipsinfo();
    }
}
time = 5;
params=getURL('page');
if(params!=undefined){
    // console.log('params：'+params);
    SetCookie(params);
}
function Time() {
    if (time === 0) {
        time =5;
        checkCookie(page);
    } else {
        time--;
    }
    setTimeout(function () {
        Time();
    }, 1000);
}
Time();
function Time1() {
    if (time === 0) {
        time =5;
        if ($.cookie('cookieid')!=undefined&$.cookie('cookieid')!='null'){
            cid=$.cookie('cookieid');
            // console.log('cid：'+cid);
            GetCookie(cid,page);
        }
        return;
    } else {
        time--;
    }
    setTimeout(function () {
        Time1();
    }, 1000);
}
Time1();