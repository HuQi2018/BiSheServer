// var UserName = $.cookie("UserName");
// $.cookie("UserName",'Zero',{"expires":365});
// console.log(UserName);
// $.removeCookie('UserName');


window.onload=function(){
    
        /**置顶功能**/
	showScroll();
	function showScroll(){
		$(window).scroll( function() { 
		    scrollValue=$(window).scrollTop();
			scrollValue > 100 ? $('div[id=btn_top]').fadeIn():$('div[id=btn_top]').fadeOut();
		} );
		$('#btn_top').click(function(){	
			var value=scrollValue/8;
// 			console.log(Math.round(value));
			$("html,body").animate({scrollTop:0},Math.round(value));	
		});	
	}
	
	function GetQueryString(name){
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);//search,查询？后面的参数，并匹配正则
         if(r!=null)return  r[2]; return null;
    }
    
    function entersearch(){
         //alert(dd);
        var event = window.event || arguments.callee.caller.arguments[0];
        if (event.keyCode == 13)
        {
            keyword = $(".gn-search").val();
            window.location.href = "iframe.html?url=https://sp0.baidu.com/s?wd="+keyword+"&ie=utf-8";
        }
    }
    
}