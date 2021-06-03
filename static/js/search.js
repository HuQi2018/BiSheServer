


movie_show(movie_data['Rows'],"movie_search_show");

//页码显示


var dqPage = movie_data['Page'];//得到当前页数
dqPage = parseInt(dqPage);//得到的文本转成int
var Type = movie_data['Type'];
var Key = movie_data['Key'];
var Limit = movie_data['Limit'];
if(!Limit) Limit=20;
var total_page = movie_data['Total'];
$("#movie_total").html(total_page);
$("#movie_key").html(decodeURI(Key));
var pageCount = parseInt(total_page/Limit)+1;//得到总页数
var jumpParmeter = "?type="+Type+"&s="+Key+"&limit="+Limit+"&page=";
pageCount = parseInt(pageCount);
var i = 1;
i = parseInt(i);
var item="";
var href = jumpParmeter;
if (pageCount <= 5 ) {//总页数小于五页，则加载所有页

    for (i; i <= pageCount; i++) {
        if (i == dqPage) {
            item += "<a class='page-numbers current'>"+i+"</a>";
        }else{
            item += "<a class='page-numbers' href='"+href+i+"' >"+i+"</a>";
        }
    };
    $('#pageBtn_pre').append(item);
    $('#pageBtn_bef').append(item);
}else if (pageCount > 5) {//总页数大于五页，则加载五页
    if (dqPage < 5) {//当前页小于5，加载1-5页
        for (i; i <= 5; i++) {
            if (i == dqPage) {
                item += "<a class='page-numbers current'>"+i+"</a>";
            }else{
                item += "<a class='page-numbers' href='"+href+i+"' >"+i+"</a>";
            }
        };
        if (dqPage <= pageCount-2) {//最后一页追加“...”代表省略的页
            item += "<a href='"+jumpParmeter+pageCount+"'>»</a>";
        }
        $('#pageBtn_pre').append(item);
        $('#pageBtn_bef').append(item);
    }else if (dqPage >= 5) {//当前页大于5页
        for (i; i <= 2; i++) {//1,2页码始终显示
            item += "<a class='page-numbers' href='"+href+i+"' >"+i+"</a>";
        }
        item += "<span class=\"page-numbers dots\">...</span>";//2页码后面用...代替部分未显示的页码
        if (dqPage+1 == pageCount) {//当前页+1等于总页码
            for(i = dqPage-1; i <= pageCount; i++){//“...”后面跟三个页码当前页居中显示
                if (i == dqPage) {
                    item += "<a class='page-numbers current'>"+i+"</a>";
                }else{
                    item += "<a class='page-numbers' href='"+href+i+"' >"+i+"</a>";
                }
            }
        }else if (dqPage == pageCount) {//当前页数等于总页数则是最后一页页码显示在最后
            for(i = dqPage-2; i <= pageCount; i++){//...后面跟三个页码当前页居中显示
                if (i == dqPage) {
                    item += "<a class='page-numbers current'>"+i+"</a>";
                }else{
                    item += "<a class='page-numbers' href='"+href+i+"' >"+i+"</a>";
                }
            }
        }else{//当前页小于总页数，则最后一页后面跟...
            for(i = dqPage-1; i <= dqPage+1; i++){//dqPage+1页后面...
                if (i == dqPage) {
                    item += "<a class='page-numbers current'>"+i+"</a>";
                }else{
                    item += "<a class='page-numbers' href='"+href+i+"' >"+i+"</a>";
                }
            }
            item += "<a href='"+jumpParmeter+pageCount+"'>»</a>";
        }
        $('#pageBtn_pre').append(item);
        $('#pageBtn_bef').append(item);
    }
}

