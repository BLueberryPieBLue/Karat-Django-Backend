window.onload=function(){
    $("#browser").css("left",($(document).width()-750)/2+"px");
    //alert($(document).width());
    //成员
    var timer;
    var left=$("#m6_c1_button .left");
    var right=$("#m6_c1_button .right");
    var porTop=[100,80,60,50,40,35,30,0,30,35,40,50,60,80,100];
    var porLeft=[8,64,120,176,232,288,344,450,615,671,727,783,839,895,951];
    var porSon=$("#m6_c1_list .all_num");
    var activeNum=7;
    var active={
        width: "100px",
        height: "100px",
        border_radius: "50px",
        margin: "0"
    };
    var notActive={
        width: "40px",
        height: "40px",
        border_radius: "20px",
        margin: "0 8px"
    };
    var name=$("#hidden .name");
    var zhiwu=$("#hidden .zhiwu");
    var photoLink=$("#hidden .link");
    var kuang=$(".all_num");
    for(var i=0;i<kuang.length;i++){
        if(name.eq(i)&&zhiwu.eq(i)&&photoLink.eq(i).text()){
            kuang.eq(i).children("img")[0].src=photoLink.eq(i).text();
        }
    }
    $("#navigation_b").mouseover(function(){
        $(".dis_none").fadeIn(700);
    });
    $("#navigation_b").mouseleave(function(){
            $(".dis_none").stop().fadeOut(200);
    });
    left.click(function(){
        var i,j;
        activeNum++;
        activeNum%=15;
        for(i=activeNum-7,j=0;j<7;i++,j++){
            //alert(j);
            porSon.eq(i%15).animate({
                "width": notActive.width,
                "height": notActive.height,
                "border-radius": notActive.border_radius,
                "margin": notActive.margin,
                "top": porTop[j]+"px",
                "left": porLeft[j]+"px"
            },1000);
            porSon.eq(i%15).removeClass("anima");
        }
        porSon.eq(i%15).animate({
            "width": active.width,
            "height": active.height,
            "border-radius": active.border_radius,
            "margin": active.margin,
            "top": porTop[j]+"px",
            "left": porLeft[j]+"px"
        },1000);
        porSon.eq(i%15).addClass("anima");
        for(i++,j++;j<15;i++,j++){
            porSon.eq(i%15).animate({
                "width": notActive.width,
                "height": notActive.height,
                "border-radius": notActive.border_radius,
                "margin": notActive.margin,
                "top": porTop[j]+"px",
                "left": porLeft[j]+"px"
            },1000);
            porSon.eq(i%15).removeClass("anima");
        }
        if(name.eq(activeNum).text()){
            $("#name .xingming").text(name.eq(activeNum).text());
        }
        if(zhiwu.eq(activeNum).text()){
            $("#name .zhiwu").text(zhiwu.eq(activeNum).text());
        }
    });
    right.click(function(){
        var i,j;
        activeNum--;
        activeNum%=15;
        for(i=activeNum-7,j=0;j<7;i++,j++){
            //alert(j);
            porSon.eq(i%15).animate({
                "width": notActive.width,
                "height": notActive.height,
                "border-radius": notActive.border_radius,
                "margin": notActive.margin,
                "top": porTop[j]+"px",
                "left": porLeft[j]+"px"
            },1000);
            porSon.eq(i%15).removeClass("anima");
        }
        porSon.eq(i%15).animate({
            "width": active.width,
            "height": active.height,
            "border-radius": active.border_radius,
            "margin": active.margin,
            "top": porTop[j]+"px",
            "left": porLeft[j]+"px"
        },1000);
        porSon.eq(i%15).addClass("anima");
        for(i++,j++;j<15;i++,j++){
            porSon.eq(i%15).animate({
                "width": notActive.width,
                "height": notActive.height,
                "border-radius": notActive.border_radius,
                "margin": notActive.margin,
                "top": porTop[j]+"px",
                "left": porLeft[j]+"px"
            },1000);
            porSon.eq(i%15).removeClass("anima");
        }
        if(name.eq(activeNum).text()){
            $("#name .xingming").text(name.eq(activeNum).text());
        }
        if(zhiwu.eq(activeNum).text()){
            $("#name .zhiwu").text(zhiwu.eq(activeNum).text());
        }
    });
    //纳士
    var bumen=[];
    var temp;
    var bgurl;
    var text=$(".text");
    var textNum=[0,1,2,3,4];
    var last=0,tempNum;
    text.eq(0).css("display","block");
    bumen[0]=$("#m7_c1_lt img");        //cb
    bumen[1]=$("#m7_c1_lbl img");       //sy
    bumen[2]=$("#m7_c1_lbr img");       //cx
    bumen[3]=$("#m7_c1_rt img");        //zh
    bumen[4]=$("#m7_c1_rb img");        //mb
    function change(Number){
        bgurl=bumen[0][0].src;
        temp=bumen[Number][0].src;
        bumen[Number].attr("src",bgurl);
        bumen[0].attr("src",temp);
        text.eq(last).css("display","none");
        text.eq(textNum[Number]).css("display","block");
        tempNum=textNum[0];
        textNum[0]=last=textNum[Number];
        textNum[Number]=tempNum;
    }
    $("#m7_c1_lbl").click(function(){change(1)});
    $("#m7_c1_lbr img").click(function(){change(2)});
    $("#m7_c1_rt img").click(function(){change(3)});
    $("#m7_c1_rb img").click(function(){change(4)});
}