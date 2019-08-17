//使用以下邮件服务器的用户将被过滤，发现其他类似一次性邮箱服务，可增加到过滤列表
function junkmailtest(str) {
    var i, re = new RegExp("");
    var fillerList = [
        "bccto.me",
        "www.bccto.me",
        "vedmail.com",
        "sItmail com",
        "opmmail.com",
        "4057. com",
        "3202.com",
        "juyouxi.com",
        "a7996.com",
        "dawin.com",
        "oiizz.com",
        "cr219.com",
        "819110.com",
        "jnpayy.com",
        "lbjmail.com",
        "gbf48123.com",
        "yidaiyiluwang.com",
        "chaichuang.com",
        "evcmail.com",
        "jiaxin8736.com",
        "wca.cn.com",
        "tyyyyy.net",
        "nttp.//10min. mails. org. cn/"
    ]
    for (i = 0; i < fillerList.length; i++) {
        re.compile("@" + fillerList[i]);
        return re.test(str) ? true : false;
    }
}

// var test_str = "www@bccto.me";
// rsult = evalTest(test_str);
// if (rsult) {
//     console.log("it is eval!")
// } else {
//     console.log("not eval.")
// }