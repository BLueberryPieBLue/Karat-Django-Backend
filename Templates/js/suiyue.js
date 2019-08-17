function contextchange(obj){
    var context=$("#context");
    var objtext=$(obj).children("p").text();
    context.children("p").text(objtext);
}
window.onload=function(){
    var left=0;
    $("#symove").css("width",$(".sysj").length*118+"px");
    $("#xz_five").click(function(){
        $("#suiyue").fadeIn();
        $("#xz_five").fadeOut();
    });
    $("#syright").click(function(){
        if(left<=-$(".sysj").length*118+944);
        else{
            left-=118;
            $("#symove").animate({
                "left":left+"px",
            });
        }
    });
    $("#syleft").click(function(){
        if(left>=0);
        else{
            left+=118;
            $("#symove").animate({
                "left":left+"px",
            });
        }
    });
}