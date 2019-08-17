window.onload=function(){
    var kj_imgs=$(".kj_img");
    var img_w=[],img_l=[],img_t=[];
    var i=0;
    var j;
    var tf=true;
    function ifrepeat(i){
        var r;
        for(j=0;j<i;j++){
            r=Math.sqrt(Math.pow(img_l[i]-img_l[j],2)+Math.pow(img_t[i]-img_t[j],2));
            if(img_w[i]/2+img_w[j]/2>r){
                return false;
            }
        }
        return true;
    }
    for(i=0;i<kj_imgs.length;i++){
        while(tf){
            img_l[i]=300+($(window).width()-600)*Math.random();
            img_w[i]=80+150*Math.random();
            img_t[i]=60+($(window).height()-380)*Math.random();
            tf=!ifrepeat(i);
        };
        tf=true;
    }
    for(i=0;i<kj_imgs.length;i++){
        kj_imgs.eq(i).css({
            "left":img_l[i]+"px",
            "width":img_w[i]+"px",
            "top":img_t[i]+"px"
        });
    }
}