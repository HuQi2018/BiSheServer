let moviedteail_list = "";
let movie_id = movie_data.movie_id;
let genres = strToJson(movie_data.genres);  //类别
let countries = strToJson(movie_data.countries);   //国家
let year = movie_data.year;         //年份
let title = movie_data.title;         //标题
let original_title = movie_data.original_title;  //原始标题
if( title ==  original_title){
    original_title = "";
}
let aka = strToJson(movie_data.aka); //又名
let tags = strToJson(movie_data.tags);  //标签
let durations = strToJson(movie_data.durations); //片长
let pubdates = strToJson(movie_data.pubdates);  //上映
let photos = strToJson(movie_data.photos);  //剧照
let languages = strToJson(movie_data.languages);  //语言
let actor = strToJson(movie_data.actor);  //主演
let directors = strToJson(movie_data.directors);  //导演
let writers = strToJson(movie_data.writers);  //编剧
let summary = movie_data.summary;  //简介
let videos = strToJson(movie_data.videos);  //短视频
let images = strToJson(movie_data.images);  //封面
let rating = strToJson(movie_data.rating);  //评分
let ratings_count = movie_data.ratings_count;  //评分人数

function For1(for_name,for_type, for_list) {
    var for_txt = "";
    if(for_list.length!=0) {
        for_txt = "<li><span class='li_name'>" + for_name + "</span>：";
        for (let i = 0; i < for_list.length; i++) {
            for_txt = for_txt + '<a href="search.html?type=' + for_type + '&s=' + for_list[i] + '" rel="tag">' + for_list[i] + '</a> ';
        }
        for_txt = for_txt + "</li>";
    }
    return for_txt;
}
function For2(for_name,for_type, for_list) {
    var for_txt = "";
    if(for_list.length!=0) {
        for_txt = "<li><span class='li_name'>" + for_name + "</span>：";
        for (let i = 0; i < for_list.length; i++) {
            for_txt = for_txt + '<span title="' + for_list[i] + '">' + for_list[i] + '</span> ';
        }
        for_txt = for_txt + "</li>";
    }
    return for_txt;
}
function For3(for_name,for_type, for_list) {
    var for_txt = "";
    if(for_list.length!=0) {
        for_txt = "<li><span class='li_name'>" + for_name + "</span>：";
        for (let i = 0; i < for_list.length; i++) {
            for_txt = for_txt + '<a target="_blank" href="'+for_list[i]["alt"]+'" ><span title="' + for_list[i]["name"] + '">' + for_list[i]["name"] + '</span> <span title="' + for_list[i]["name_en"] + '">' + for_list[i]["name_en"] + '</span></a> ';
        }
        for_txt = for_txt + "</li>";
    }
    return for_txt;
}

var videos_txt = "";
if(videos.length!=0) {
    videos_txt = "<li><span class='li_name'>视频</span>：<div class=\"movie_video\">";
    for (let i = 0; i < videos.length; i++) {
        videos_txt = videos_txt + '<a target="_blank" title="'+videos[i]["source"]["name"]+'" href="'+videos[i]["sample_link"]+'" ><img alt="'+videos[i]["source"]["name"]+'" src="'+videos[i]["source"]["pic"]+'" ></a>';
    }
    videos_txt = videos_txt + "</div></li>";
}

let genres_txt = For1("类型","genres",genres);
let tags_txt = For1("标签","tag",tags);
let languages_txt = For1("语言","languages",languages);
let countries_txt = For1("地区","countries",countries);

let aka_txt = For2("又名","aka",aka);
let pubdates_txt = For2("上映","pubdates",pubdates);
let durations_txt = For2("片长","durations",durations);

let directors_txt = For3("导演","directors",directors);
let writers_txt = For3("编剧","writers",writers);
let actor_txt = For3("主演","actor",actor);

let rating_txt = '<li><span class=\'li_name\'>豆瓣</span>：<a class="dbpingfen" rel="nofollow" href="https://movie.douban.com/subject/'+ movie_id +'/" title="在豆瓣查看评分" target="_blank">'+rating['average']+'分</a> from '+ratings_count+' users </li>';
let summary_txt = '<li><span class=\'li_name\'>简介</span>：'+summary+ "</li>";
let year_txt = '<li><span class=\'li_name\'>年份</span>：<a href="search.html?type=year&s='+ year +'">'+year+ "</a></li>";

let photos_txt = '<li style="margin-top:20px;"><span class=\'li_name\'>剧照</span>：<div style="width:100%;" class="movie_photos">';
for (let i = 0; i < photos.length; i++) {
    photos_txt  = photos_txt + '<a target="_blank" href="'+ photos[i]["alt"] +'"><img src="' + photos[i]["thumb"] + '" noreferer="" /></a> ';
}
photos_txt  = photos_txt + "</div></li>";

moviedteail_list = moviedteail_list + genres_txt + countries_txt + year_txt + languages_txt +aka_txt + tags_txt + pubdates_txt+ durations_txt + directors_txt +
    writers_txt + actor_txt + rating_txt + videos_txt +  '<li><span class="li_name">评分</span>：' +
    '<div id="movie_star_wrapper">\n' +
    '<input type="radio" id="star1" name="star" value="1"/>\n' +
    '<label for="star1"></label>\n' +
    '<input type="radio" id="star2" name="star" value="2"/>\n' +
    '<label for="star2"></label>\n' +
    '<input type="radio" id="star3" name="star" value="3"/>\n' +
    '<label for="star3"></label>\n' +
    '<input type="radio" id="star4" name="star" value="4"/>\n' +
    '<label for="star4"></label>\n' +
    '<input type="radio" id="star5" name="star" value="5"/>\n' +
    '<label for="star5"></label>\n' +
    '</div></li>';

let movie_like = "";
if(user_movie_like[0]&&user_movie_like[0]==movie_id){
    movie_like = "movie_like_cs";
}


var moviedteail_list2 = summary_txt + photos_txt;
var movie_detail = '<div class="dyxingq"><div class="mi_ne_kd dypre">' +
    '<div class="dyimg fl"><img src="'+images["small"]+'"><div style="bottom: 2px; right: -8px; position: absolute;"><p class="movie_like '+movie_like+'" movieId="'+movie_id+'">&#10084;</p></div>';
if (rating['average']!=0){
    movie_detail = movie_detail + '<div class="rating">'+rating['average']+'</div>';
}
movie_detail = movie_detail + '</div><div class="dytext fl"><div class="moviedteail_tt"><h1>'+ title + '</h1>' +
    '                                <span>' + original_title + '</span>' +
    '                            </div><ul class="moviedteail_list" id="moviedteail_list">';
movie_detail = movie_detail + moviedteail_list;
movie_detail = movie_detail + '</div><div class="clear"></div></div>';

movie_detail = movie_detail + '<div id="movie_detail2" style="margin: 20px 40px;">' + moviedteail_list2 + '</div>';
$("#movie_detail").html(movie_detail);


movie_show(movie_5_cai,"cai_list");

if(user_movie_rating[0]){
    $("#star"+user_movie_rating[0]).attr("checked", true);
}

$("#movie_id").val(movie_id);
$("#movie_title").val(title);


$('input[type=radio][name=star]').change(function() {
    let th = this;
    let rating = this.value;
    $.ajax({
        "url": "/movie/movie_rating",
        "data": {"rating":rating,"movieId":movie_id},
        "type": "GET",
        "dataType": "json",
        "success": function (data) {
            if (data.code == 200) {
                show_tip(data.data.msg, data.data.url, 2);
            } else {
                show_tip(data.msg, "", 2);
                th.checked=false
            }
            console.log(data);
        },
    });
})


if(commentData.length!=0) {
    for (let i = 0; i < commentData.length; i++) {
        addComments(commentData[i]);
    }
}
