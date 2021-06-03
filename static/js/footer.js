

movie_show(user_5_brow,"user_5_brow");
movie_show(user_5_like,"user_5_like");
movie_show(user_5_cai,"user_5_cai");


movie_show(movie_nav_tag[0]["data"],"movie_nav_tag_1");
movie_show(movie_nav_tag[1]["data"],"movie_nav_tag_2");
movie_show(movie_nav_tag[2]["data"],"movie_nav_tag_3");
movie_show(movie_nav_tag[3]["data"],"movie_nav_tag_4");


$(".movie_like").click(function () {
    var movieId = this.getAttribute("movieId");
    var th = $("[movieId="+movieId+"]");
    $.ajax({
        "url": "/movie/movie_like",
        "data": {"movieId":movieId},
        "type": "GET",
        "dataType": "json",
        "success": function (data) {
            if (data.code == 200) {
                show_tip(data.data.msg, "", 2);
                th.toggleClass('movie_like_cs');
            } else {
                show_tip(data.msg, "", 2);
            }
            console.log(data);
        },
    });
})

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

}

