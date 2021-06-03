// var UserName = $.cookie("UserName");
// $.cookie("UserName",'Zero',{"expires":365});
// console.log(UserName);
// $.removeCookie('UserName');

//获取链接后参数
function GetQueryString(name){
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);//search,查询？后面的参数，并匹配正则
    if(r!=null)return  r[2]; return "";
}

//百度搜索
function entersearch(){
    //alert(dd);
    var event = window.event || arguments.callee.caller.arguments[0];
    if (event.keyCode == 13)
    {
        keyword = $(".gn-search").val();
        window.location.href = "iframe.html?url=https://sp0.baidu.com/s?wd="+keyword+"&ie=utf-8";
    }
}

//显示提示窗口
function show_tip(contents, jump="", time=5) {
    var timeout;
    $("#info-tip-contents").html(contents+"&nbsp;&nbsp;提示窗口"+time+"s后关闭。");
    $("#info-tip").show();
    $("#info-tip")[0].setAttribute("data-url",jump);
    // if (jump!=""){
    //     time = time - 1;//提前跳转
    // }
    timeout = setTimeout(function (){close_tip()},1000*time);
}

//关闭提示窗口
function close_tip(){
    var jump = $("#info-tip")[0].getAttribute("data-url");
    if (jump == "?"){
        location.reload();
    }
    if (jump!=""){
        window.location.href = jump;
    }
    $("#info-tip").hide();
}

//刷新验证码
function re_captcha() {
    document.getElementById("imgCode").src = "api/captcha?" + Math.random();
}

//登录
function login(){
    var timeout;
    $('#login_tip').html("");
    $.ajax({
        "url":"/user/login",
        "data":$("#login_form").serialize(),
        "type":"POST",
        "dataType":"json",
        "success":function(data){
            if(data.code==200){
                $.cookie("uuid",data.data.uuid,{"expires":7});
                show_tip(data.data.msg,data.data.url,2);
            }else{
                $("#login_tip").html(data.msg);
                timeout = setTimeout(function(){$("#login_tip").html("")},5000);
            }
            console.log(data);
        },
    });
    return false;
}

// 注销
function logout() {
    $.ajax({
        "url":"/user/logout",
        "type":"GET",
        "dataType":"json",
        "success":function(data){
            if(data.code==200){
                $.cookie("uuid",data.data.uuid);
                show_tip(data.data.msg,data.data.url,2);
            }else{
                show_tip(data.msg,"/",2);
            }
            console.log(data);
        },
    });
}

// 用户信息修改
function user_info_modify(){
    var timeout;
    $('#error_msg').html("");
    var formData = new FormData($("#user_info_modify")[0]);
    if(verifyCheck._click()) {
        $.ajax({
            "url": "/user/infoModify",
            "data": formData,
            "type": "POST",
            "dataType": "json",
            "async": false,
            "cache": false,
            "contentType": false,
            "processData": false,
            "success": function (data) {
                if (data.code == 200) {
                    show_tip(data.data.msg, data.data.url, 2);
                    $("#edit_info").show();
                    $("#saveSetting").hide();
                    $("#saveSetting_cancel").hide();
                    $(".user_info .input").hide();
                    $(".user_info .info").show();
                    $("#user_type").toggleClass("forbidden");
                } else {
                    $("#error_msg").html(data.msg);
                    timeout = setTimeout(function () {
                        $("#error_msg").html("")
                    }, 5000);
                }
                console.log(data);
            },
        });
    }
    return false;
}

// 用户密码修改
function user_password_modify(){
    var timeout;
    $('#error_msg').html("");
    if(verifyCheck._click()) {
        $.ajax({
            "url": "/user/pwdModify",
            "data": $("#user_info_modify").serialize(),
            "type": "POST",
            "dataType": "json",
            "success": function (data) {
                if (data.code == 200) {
                    show_tip(data.data.msg, data.data.url, 2);
                } else {
                    $("#error_msg").html(data.msg);
                    timeout = setTimeout(function () {
                        $("#error_msg").html("")
                    }, 5000);
                }
                console.log(data);
            },
        });
    }
    return false;
}

// 用户邮箱修改
function user_email_modify(){
    $('#error_msg2').html("");
    if(verifyCheck._click()) {
        $.ajax({
            "url": "/user/emailModify",
            "data": $("#user_info_modify").serialize(),
            "type": "POST",
            "dataType": "json",
            "success": function (data) {
                if (data.code == 200) {
                    show_tip(data.data.msg, data.data.url, 2);
                } else {
                    $("#error_msg2").html(data.msg);
                    timeout = setTimeout(function () {
                        $("#error_msg2").html("")
                    }, 5000);
                }
                console.log(data);
            },
        });
    }
    return false;
}

// 字符串转Json格式
function strToJson(str1){
    let json = eval('(' + str1.replaceAll("True", "true").replaceAll("False", "false").replaceAll("None", "''") + ')');
    return json;
}

// 循环显示电影列表
function movie_show(show_movie_data, show_movie_id) {

    let movie_search_show_text = "<ul>";
    let movie_id = "";
    let image = "";
    let title = "";
    let year = "";
    let rating = "";
    let actor = "";
    let actors = "";
    let countries = "";
    let language = "";
    let tag = "";

    for (let j = 0; j < show_movie_data.length; j++) {

        movie_id = show_movie_data[j].movie_id;

        let movie_like = "";
        if(user_like.includes(movie_id)){
            movie_like = "movie_like_cs";
        }

        image = strToJson(show_movie_data[j].images).small;
        title = show_movie_data[j].title;
        year = show_movie_data[j].year;
        countries = strToJson(show_movie_data[j].countries)[0];
        language = strToJson(show_movie_data[j].languages)[0];
        tag = strToJson(show_movie_data[j].tags)[0];
        rating = strToJson(show_movie_data[j].rating).average;
        actor = strToJson(show_movie_data[j].actor.replaceAll("None", "''"));
        actors = "";
        for (let k = 0; k < actor.length; k++) {
            actors = actors + actor[k].name + "，";
        }

        movie_search_show_text = movie_search_show_text + '<li>';
        movie_search_show_text = movie_search_show_text + '<a href="movie.html?id=' + movie_id + '" target="_blank">';
        movie_search_show_text = movie_search_show_text + '<img class="thumb lazy" src="' + image + '" alt="' + title + '"style="display: inline;"> <span class="zoom-icon glyph-icon flaticon-media23"></span>';
        movie_search_show_text = movie_search_show_text + '</a><div class="hdinfo"> ';
        if(year) {
            movie_search_show_text = movie_search_show_text + '<span class="qb">' + year + '</span>';
        }
        if(language) {
            movie_search_show_text = movie_search_show_text + '<span class="furk">' + language + '</span>';
        }
        if(countries) {
            movie_search_show_text = movie_search_show_text + '<span class="qb">' + countries + '</span>';
        }
        if(tag) {
            movie_search_show_text = movie_search_show_text + '<span class="furk">' + tag + '</span>';
        }
        movie_search_show_text = movie_search_show_text + '</div>';
        if(rating) {
            movie_search_show_text = movie_search_show_text + '<div class="rating">' + rating + '</div>';
        }
        movie_search_show_text = movie_search_show_text + '<p class="movie_like '+movie_like+'" movieId="' + movie_id + '">&#10084;</p>';
        movie_search_show_text = movie_search_show_text + '<h3 class="dytit"><a target="_blank" href="movie.html?id=' + movie_id + '" title="' + title + '">' + title + '</a></h3>';
        movie_search_show_text = movie_search_show_text + '<p class="inzhuy" title="' + actors + '">主演：' + actors + '</p>';
        movie_search_show_text = movie_search_show_text + '</li>';
    }
    movie_search_show_text = movie_search_show_text + '</ul>';

    $("#"+show_movie_id).html(movie_search_show_text);
}

// 统计评论长度
function content_length(){
    var current_len = $("#content_text").val().length;
    var maxlimit=500;
    if ( current_len > maxlimit){
        $("#content_tip").html('可输入字符超出限制！');
        // field.value = field.value.substring(0, maxlimit);
    }else {
        $("#content_tip").html('你还可以输入<span class="cf30 abc">'+ (maxlimit - current_len )+'</span> 个字符');
    }
}

// 添加评论
function comments() {
    $('#content_tip').html("");
    if(!($("#content_text").val()&&$("#content_title").val())){
        show_tip("评论失败，标题和内容不能为空", "", 2);
        return false;
    }
    $.ajax({
        "url": "/movie/movie_comment",
        "data": $("#comments").serialize(),
        "type": "POST",
        "dataType": "json",
        "success": function (data) {
            if (data.code == 200) {
                show_tip(data.data.msg, data.data.url, 2);
                $("#content_text").val("");
                $("#content_title").val("");
                user_movie_comment_id.push(data.data.comment["id"])
                addComments(data.data.comment);
            } else {
                $("#content_tip").html('<span style="color: red;">'+data.msg+'</span>');
                timeout = setTimeout(function () {
                    $("#content_tip").html("");
                }, 5000);
            }
            console.log(data);
        },
    });
    return false;
}

let commentI = 1;
// 显示评论
function addComments(commentData, user=0) {
    let commentID = commentData["id"];
    let commentDelete = "";
    let movieTitle = "";
    if(user||user_movie_comment_id.includes(commentID)){
        commentDelete = '&nbsp;&nbsp;&nbsp;&nbsp;<a style="cursor: pointer;" onclick="deleteComment(' + commentID + ');">删除</a>';
    }
    if(user){
        movieTitle = " —— <a href='/movie.html?id=" + commentData["movie"] + "'>" + commentData["movieName"] + "</a>";
    }
    var commentLi = "";
    commentLi = commentLi + '<li class="comment byuser comment-author-suxuemin even thread-even depth-1" id="commentID-'+commentID+'">\n' +
        '                            <div class="comment-body">\n' +
        '                                <div class="comment-author"><img src="/user/user_img/' + commentData["user"] + '/"></div>\n' +
        '                                <div class="comment-head"><span class="title">' + commentData["title"] + movieTitle + '</span>'+
        '                                    <span class="name">' + commentData["userName"] + ' &nbsp;&nbsp;&nbsp;<em>' + commentData["comment_time"] + '&nbsp;</em>' + commentDelete + '</span>\n' +
        '                                    <span class="num"> #'+commentI+'</span>\n' +
        '                                    <p> </p><p>' + commentData["content"] + '</p>\n' +
        '                                    <p></p>\n' +
        '                                </div>\n' +
        '                            </div>\n' +
        '                        </li>';
    $("#commentlist").append(commentLi);
    $("#commentI").html(commentI);
    commentI++;
}

// 删除评论
function deleteComment(id) {
    $.ajax({
        "url": "/movie/delete_movie_comment",
        "data": {"comment_id": id},
        "type": "GET",
        "dataType": "json",
        "success": function (data) {
            if (data.code == 200) {
                show_tip(data.data.msg, data.data.url, 2);
                $("#commentID-"+id).remove();
                commentI--;
                $("#commentI").html(commentI-1);
            } else {
                show_tip(data.msg, "", 2);
            }
            console.log(data);
        },
    });
}