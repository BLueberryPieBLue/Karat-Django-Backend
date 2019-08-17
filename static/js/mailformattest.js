function mailformattest(mail) {
    var reg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    if (!reg.test(mail)) {
        alert('提示\n\n请输入有效的E_mail！');
        return false;
    } else {
        return true;
    }
}