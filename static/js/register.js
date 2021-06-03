/**
* 功能说明:		输入验证
* @author:		vivy <lizhizyan@qq.com>
* @time:		2015-9-25 16:15:30
* @version:		V1.1.0
* @使用方法:	    
* <input class="required" type="text" data-valid="isNonEmpty||isEmail" data-error="email不能为空||邮箱格式不正确" id="" />	
* 1、需要验证的元素都加上【required】样式
* 2、@data-valid		验证规则，验证多个规则中间用【||】隔开，更多验证规则，看rules和rule，后面遇到可继续增加
* 3、@data-error		规则对应的提示信息，一一对应
*
* @js调用方法：
* verifyCheck({
*  	formId:'verifyCheck',		<验证formId内class为required的元素
*	onBlur:null,				<被验证元素失去焦点的回调函数>
*	onFocus:null,				<被验证元素获得焦点的回调函数>
*	onChange: null,				<被验证元值改变的回调函数>
*	successTip: true,			<验证通过是否提示>
*	resultTips:null,			<显示提示的方法，参数obj[当前元素],isRight[是否正确提示],value[提示信息]>
*	clearTips:null,				<清除提示的方法，参数obj[当前元素]>			
*	code:true					<是否需要手机号码输入控制验证码及点击验证码倒计时,目前固定手机号码ID为phone,验证码两个标签id分别为time_box，resend,填写验证框id为code>
*	phone:true					<改变手机号时是否控制验证码>
* })
* $("#submit-botton").click(function(){		<点击提交按钮时验证>	
*  	if(!common.verify.btnClick()) return false;
* })
*
* 详细代码请看register.src.js
*/


function reg1(){
	var timeout;
	$('#error_msg1').html("");
	if(verifyCheck._click()){
		$.ajax({
			"url":"/user/register1",
			"data":$("#part1").serialize(),
			"type":"POST",
			"dataType":"json",
			"success":function(data){
				email = data.data.email;
				userName = data.data.userName;
				if(data.code==200&&email){
					$("#reg_email").val(email);  //填充邮箱
					$("#userName").html(userName);  //填充用户名
					$("#verifyYz").click();	//发送验证码
					$(".part1").hide();	//切换显示登陆步骤
					$(".part2").show();
					$(".step li").eq(1).addClass("on");
					// alert(data.data.msg);
				}else{
				   $('#error_msg1').html(data.msg);	//请求失败提示
				   timeout = setTimeout(function(){$("#error_msg1").html("")},5000);
				}
				console.log(data);
			},
		});
	}
	return false;
}


function reg2(){
	var timeout;
	$('#error_msg2').html("");
	if(verifyCheck._click()){
		$.ajax({
			"url":"/user/register2",
			"data":$("#part2").serialize(),
			"type":"POST",
			"dataType":"json",
			"success":function(data){
				if(data.code==200){
                    $(".part2").hide(); //切换显示登陆步骤
                    $(".part3").show();
                    $(".step li").eq(2).addClass("on");
				   // alert(data.data.msg);
				}else{
				   $('#error_msg2').html(data.msg);	//请求失败提示
				   timeout = setTimeout(function(){$("#error_msg2").html("")},5000);
				}
				console.log(data);
			},
		});
	}
	return false;
}

function reg3(){
	var timeout;
	var formData = new FormData($("#part3")[0]);
	$('#error_msg3').html("");
	if(verifyCheck._click()){
		$.ajax({
			"url":"/user/register3",
			"data":formData,
			"type":"POST",
			"dataType":"json",
			"async": false,
			"cache": false,
			"contentType": false,
			"processData": false,
			"success":function(data){
				if(data.code==200){
					$(".part3").hide();//切换显示登陆步骤
					$(".part4").show();
					$(".step li").eq(3).addClass("on");
					countdown({
						maxTime: 10,
						ing: function (c) {
							$("#times").text(c);
						},
						after: function () {
							window.location.href = "index.html";
						}
					});
				   // alert(data.data.msg);
				}else{
				   $('#error_msg3').html(data.msg);	//请求失败提示
				   timeout = setTimeout(function(){$("#error_msg3").html("")},5000);
				}
				console.log(data);
			},
		});
	}
	return false;
}

function reg3_jump(){
	if(confirm("确认跳过么？跳过将导致系统无法更好地收集您的信息，给您更精确的推送信息，当然您也可以选择登录后在用户中心更新该信息。")) {
		var csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]")[0].value;
		$.ajax({
			"url": "/user/register3",
			"data": {"csrfmiddlewaretoken": csrfmiddlewaretoken},
			"type": "POST",
			"dataType": "json",
			"success": function (data) {
				if (data.code == 200) {
					$(".part3").hide();//切换显示登陆步骤
					$(".part4").show();
					$(".step li").eq(3).addClass("on");
					countdown({
						maxTime: 10,
						ing: function (c) {
							$("#times").text(c);
						},
						after: function () {
							window.location.href = "index.html";
						}
					});
					// alert(data.data.msg);
				} else {
					$('#error_msg3').html(data.msg);	//请求失败提示
					timeout = setTimeout(function () {
						$("#error_msg3").html("")
					}, 5000);
				}
				console.log(data);
			},
		});
	}
}

function showoutc() {
	$(".m-sPopBg,.m-sPopCon").show();
}
function closeClause() {
	$(".m-sPopBg,.m-sPopCon").hide();
}

// parent是父级编号，sid是select标签的id属性的值
function appendList(parent,sid){
	// 发送ajax请求
	$.ajax({
		"url":"api/districts",
		"data":"parent="+parent,
		"type":"get",
		"dataType":"json",
		"success":function(json) {
			// 获取列表的数组
			var list = json.data;
			if(sid!="province") {
				if (sid == "city") {
					$("#area").html("<option value=''>---- 请选择 ----</option>");
				}
				$("#" + sid).html("<option value=''>---- 请选择 ----</option>");
			}
			// 遍历数组
			for(var i=0;i<list.length;i++){
				// console.log(list[i]);
				// 每一条记录生成一个option
				var option="<option value='"+
					list[i].name+"' code='"+list[i].code+"'>"+list[i].name+"</option>";
				// var option="<option value='"+list[i].code+"'>"+list[i].name+"</option>";
				// 将option添加到select内部
				$("#"+sid).append(option);
			}
		}
	});
}

function fget1(){
	var timeout;
	$('#error_msg1').html("");
	if(verifyCheck._click()){
		$.ajax({
			"url":"/user/fget?step=1",
			"data":$("#part1").serialize(),
			"type":"POST",
			"dataType":"json",
			"success":function(data){
				email = data.data.email;
				if(data.code==200&&email){
					$("#reg_email").val(email);  //填充邮箱
					// $("#verifyYz").click();	//发送验证码
					$(".part1").hide();	//切换显示登陆步骤
					$("#part2").show();
					$(".step li").eq(1).addClass("on");
					// alert(data.data.msg);
				}else{
				   $('#error_msg1').html(data.msg);	//请求失败提示
				   timeout = setTimeout(function(){$("#error_msg1").html("")},5000);
				}
				console.log(data);
			},
		});
	}
	return false;
}


function fget2(){
	var timeout;
	$('#error_msg2').html("");
	if(verifyCheck._click()){
		$.ajax({
			"url":"/user/fget?step=2",
			"data":$("#part2").serialize(),
			"type":"POST",
			"dataType":"json",
			"success":function(data){
				if(data.code==200){
                    $("#part2").hide(); //切换显示登陆步骤
                    $("#part3").show();
                    $(".step li").eq(2).addClass("on");
				   // alert(data.data.msg);
				}else{
				   $('#error_msg2').html(data.msg);	//请求失败提示
				   timeout = setTimeout(function(){$("#error_msg2").html("")},5000);
				}
				console.log(data);
			},
		});
	}
	return false;
}

function fget3(){
	var timeout;
	$('#error_msg3').html("");
	if(verifyCheck._click()){
		$.ajax({
			"url":"/user/fget?step=3",
			"data":$("#part3").serialize(),
			"type":"POST",
			"dataType":"json",
			"success":function(data){
				if(data.code==200){
					show_tip("密码修改成功！","index.html",3);
				   // alert(data.data.msg);
				}else{
				   $('#error_msg3').html(data.msg);	//请求失败提示
				   timeout = setTimeout(function(){$("#error_msg3").html("")},5000);
				}
				console.log(data);
			},
		});
	}
	return false;
}


//修改用户头像
// 获取本地上传的照片路径
function getPath(obj) {
	if (obj) {
		//ie
		if (window.navigator.userAgent.indexOf("MSIE") >= 1) {
			obj.select();
			// IE下取得图片的本地路径
			return document.selection.createRange().text;
		}
		//firefox
		else if (window.navigator.userAgent.indexOf("Firefox") >= 1) {
			if (obj.files) {
				// Firefox下取得的是图片的数据
				return obj.files.item(0).getAsDataURL();
			}
			return obj.value;
		}
		return obj.value;
	}
}
//显示图片
function previewPhoto() {
	var picsrc = getPath(document.all.fileid);
	var picpreview = document.getElementById("preview");
	if (!picsrc) {
		return
	}
	if (window.navigator.userAgent.indexOf("MSIE") >= 1) {
		if (picpreview) {
			try {
				picpreview.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = picsrc;
			} catch (ex) {
				alert("文件路径非法，请重新选择！");
				return false;
			}
		} else {
			// var imgNode=document.createElement('img');
			// imgNode.src = picsrc;
			// picpreview.appendChild(imgNode);
			picpreview.src = picsrc;
		}
	}
}
function preImg(fileid, imgid) {
	if (typeof FileReader == 'undefined') {
		var picsrc = getPath(document.all.fileid)
		$("#imgid").attr({
			src: picsrc
		});
		previewPhoto();
	} else {
		var reader = new FileReader();
		var name = $("#fileid").val();
		var picpreview = document.getElementById("preview");
		reader.onload = function (e) {
			// var img = document.getElementById(imgid);
			// var imgNode=document.createElement('img');
			// imgNode.src = this.result;
			// //img.src = this.result;
			// picpreview.appendChild(imgNode);
			picpreview.src = this.result;
		}
		reader.readAsDataURL(document.getElementById(fileid).files[0]);
	}
}

(function($) {
	var h, timerC = 60,
		opt;
	var j = function(a) {
			a = $.extend(require.defaults, a || {});
			opt = a;
			return (new require())._init(a)
		};

	function require(f) {
		var g = {
			phone: /^1(3\d|5[0-35-9]|8[025-9]|47)\d{8}$/,
			company: /^[\u4E00-\u9FA5a-zA-Z][\u4E00-\u9FA5a-zA-Z0-9\s-,-.]*$/,
			uname: /^[\u4E00-\u9FA5a-zA-Z][\u4E00-\u9FA5a-zA-Z0-9_]*$/,
			email: /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$/,
			zh: /^[\u4e00-\u9fa5]+$/,
			card: /^((1[1-5])|(2[1-3])|(3[1-7])|(4[1-6])|(5[0-4])|(6[1-5])|71|(8[12])|91)\d{4}(((((19|20)((\d{2}(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(\d{2}(0[13578]|1[02])31)|(\d{2}02(0[1-9]|1\d|2[0-8]))|(([13579][26]|[2468][048]|0[48])0229)))|20000229)\d{3}(\d|X|x))|(((\d{2}(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(\d{2}(0[13578]|1[02])31)|(\d{2}02(0[1-9]|1\d|2[0-8]))|(([13579][26]|[2468][048]|0[48])0229))\d{3}))$/,
			int: /^\d{6}$/,
			ranCode: /^[A-Za-z\d]{4}$/,
			s: ''
		};
		this.rules = {
			isNonEmpty: function(a, b) {
				b = b || " ";
				if (!a.length) return b
			},
			minLength: function(a, b, c) {
				c = c || " ";
				if (a.length < b) return c
			},
			maxLength: function(a, b, c) {
				c = c || " ";
				if (a.length > b) return c
			},
			isRepeat: function(a, b, c) {
				c = c || " ";
				if (a !== $("#" + b).val()) return c
			},
			between: function(a, b, c) {
				c = c || " ";
				var d = parseInt(b.split('-')[0]);
				var e = parseInt(b.split('-')[1]);
				if (a.length < d || a.length > e) return c
			},
			level: function(a, b, c) {
				c = c || " ";
				var r = j.pwdStrong(a);
				if (b > 4) b = 3;
				if (r < b) return c
			},
			isPhone: function(a, b) {
				b = b || " ";
				if (!g.phone.test(a)) return b
			},
			isEmail: function(a, b) {
				b = b || " ";
				if (!g.email.test(a)) return b
			},
			isCompany: function(a, b) {
				b = b || " ";
				if (!g.company.test(a)) return b
			},
			isInt: function(a, b) {
				b = b || " ";
				if (!g.int.test(a)) return b
			},
			isUname: function(a, b) {
				b = b || " ";
				if (!g.uname.test(a)) return b
			},
			isZh: function(a, b) {
				b = b || " ";
				if (!g.zh.test(a)) return b
			},
			isCard: function(a, b) {
				b = b || " ";
				if (!g.card.test(a)) return b
			},
			isNonRandCode: function(a, b) {
				b = b || " ";
				if (!g.ranCode.test(a)) return b
			},
			isChecked: function(c, d, e) {
				d = d || " ";
				var a = $(e).find('input:checked').length,
					b = $(e).find('.on').length;
				if (!a && !b) return d
			}
		}
	};
	require.prototype = {
		_init: function(b) {
			this.config = b;
			this.getInputs = $('#' + b.formId).find('.required:visible');
			var c = false;
			var d = this;
			if (b.code) {
				$("#verifyYz").click(function() {
					var timeout;
					var timeout2;
					$("#error_msg2").html("");
					var email_type = $("#verifyYz")[0].getAttribute("data-set");
					var csrfmiddlewaretoken = $("[name=csrfmiddlewaretoken]")[0].value;
					if(email_type==3){
						data = {"email":$("#reg_email").val(),"randCode":$("#randCode").val(), "csrfmiddlewaretoken": csrfmiddlewaretoken}
					}else{
						data = {"email":$("#reg_email").val(), "csrfmiddlewaretoken": csrfmiddlewaretoken}
					}
					$.ajax({
						"url":"/api/email_vail?type="+email_type,
						"data":data,
						"type":"POST",
						"dataType":"json",
						"success":function(data){
							if(data.code==200){
								$("#time_box").text("60 s后可重发");
								d._sendVerify()
								$('#error_msg2').html(data.data.msg);
								timeout2 = setTimeout(function(){$("#verifyYz").show();$("#time_box").hide();clearTimeout(h);},60000);
							}else{
								$('#error_msg2').html(data.msg);	//请求失败提示
								$("#verifyYz").show();
								$("#time_box").hide();
							}
							timeout = setTimeout(function(){$("#error_msg2").html("")},5000);
							console.log(data);
						},
					});
				})
			}
			$('body').on({
				blur: function(a) {
					d.formValidator($(this));
					if (b.phone && $(this).attr("id") === "phone") d._change($(this));
					b.onBlur ? b.onBlur($(this)) : ''
				},
				focus: function(a) {
					b.onFocus ? b.onFocus($(this)) : $(this).parent().find("label.focus").not(".valid").removeClass("hide").siblings(".valid").addClass("hide") && $(this).parent().find(".blank").addClass("hide") && $(this).parent().find(".close").addClass("hide")
				},
				keyup: function(a) {
					if (b.phone && $(this).attr("id") === "phone") d._change($(this))
				},
				change: function(a) {
					b.onChange ? b.onChange($(this)) : ''
				}
			}, "#" + b.formId + " .required:visible");
			$('body').on("click", ".close", function() {
				var p = $(this).parent(),
					input = p.find("input");
				input.val("").focus()
			})
		},
		formValidator: function(a) {
			var b = a.attr('data-valid');
			if (b === undefined) return false;
			var c = b.split('||');
			var d = a.attr('data-error');
			if (d === undefined) d = "";
			var e = d.split("||");
			var f = [];
			for (var i = 0; i < c.length; i++) {
				f.push({
					strategy: c[i],
					errorMsg: e[i]
				})
			};
			return this._add(a, f)
		},
		_add: function(a, b) {
			var d = this;
			for (var i = 0, rule; rule = b[i++];) {
				var e = rule.strategy.split(':');
				var f = rule.errorMsg;
				var g = e.shift();
				e.unshift(a.val());
				e.push(f);
				e.push(a);
				var c = d.rules[g].apply(a, e);
				if (c) {
					opt.resultTips ? opt.resultTips(a, false, c) : j._resultTips(a, false, c);
					return false
				}
			}
			opt.successTip ? (opt.resultTips ? opt.resultTips(a, true) : j._resultTips(a, true)) : j._clearTips(a);
			return true
		},
		_sendVerify: function() {
			var a = this;
			$("#verifyYz").text("发送验证码").hide();
			$("#time_box").text("10 s后可重发").show();
			if (timerC === 0) {
				clearTimeout(h);
				timerC = 60;
				var b = /^1([^01269])\d{9}$/;
				if (!b.test($("#phone").val())) {
					$("#time_box").text("发送验证码")
				} else {
					$("#verifyYz").show();
					$("#time_box").hide()
				}
				return
			}
			$("#time_box").text(timerC + " s后可重发");
			timerC--;
			h = setTimeout(function() {
				a._sendVerify()
			}, 1000)
		},
		_change: function(a) {
			var b = this;
			if (a.val().length != 11) {
				$("#verifyYz").hide();
				$("#time_box").show();
				if (timerC === 60) $("#time_box").text("发送验证码");
				$("#verifyNo").val("");
				this.config.clearTips ? this.config.clearTips($("#verifyNo")) : j._clearTips($("#verifyNo"));
				return
			}
			var c = /^1([^01269])\d{9}$/;
			if (!c.test(a.val())) return false;
			if (timerC === 60) {
				$("#verifyYz").show();
				$("#time_box").hide()
			} else {
				$("#verifyYz").hide();
				$("#time_box").show()
			}
		}
	};
	j._click = function(c) {
		c = c || opt.formId;
		var d = $("#" + c).find('.required:visible'),
			self = this,
			result = true,
			t = new require(),
			r = [];
		$.each(d, function(a, b) {
			result = t.formValidator($(b));
			if (result) r.push(result)
		});
		if (d.length !== r.length) result = false;
		return result
	};
	j._clearTips = function(a) {
		a.parent().find(".blank").addClass("hide");
		a.parent().find(".valid").addClass("hide");
		a.removeClass("v_error")
	};
	j._resultTips = function(a, b, c) {
		a.parent().find("label.focus").not(".valid").addClass("hide").siblings(".focus").removeClass("hide");
		a.parent().find(".close").addClass("hide");
		a.removeClass("v_error");
		c = c || "";
		if (c.length > 21) c = "<span>" + c + "</span>";
		var o = a.parent().find("label.valid");
		if (!b) {
			o.addClass("error");
			a.addClass("v_error");
			if ($.trim(a.val()).length > 0) a.parent().find(".close").removeClass("hide")
		} else {
			a.parent().find(".blank").removeClass("hide")
		}
		o.text("").append(c)
	};
	j.textChineseLength = function(a) {
		var b = /[\u4E00-\u9FA5]|[\u3001-\u3002]|[\uFF1A-\uFF1F]|[\u300A-\u300F]|[\u3010-\u3015]|[\u2013-\u201D]|[\uFF01-\uFF0E]|[\u3008-\u3009]|[\u2026]|[\uffe5]/g;
		if (b.test(a)) return a.match(b).length;
		else return 0
	};
	j.pwdStrong = function(a) {
		var b = 0;
		if (a.match(/[a-z]/g)) {
			b++
		}
		if (a.match(/[A-Z]/g)) {
			b++
		}
		if (a.match(/[0-9]/g)) {
			b++
		}
		if (a.match(/(.[^a-z0-9A-Z])/g)) {
			b++
		}
		if (b > 4) {
			b = 4
		}
		if (b === 0) return false;
		return b
	};
	require.defaults = {
		formId: 'verifyCheck',
		onBlur: null,
		onFocus: null,
		onChange: null,
		successTip: true,
		resultTips: null,
		clearTips: null,
		code: true,
		phone: false
	};
	window.verifyCheck = $.verifyCheck = j
})(jQuery);
(function($) {
	var f;
	var g = function() {
			return (new require())._init()
		};

	function require(a) {};
	require.prototype = {
		_init: function() {
			var b = this;
			$('body').on({
				click: function(a) {
					b._click($(this))
				}
			}, ".showpwd:visible")
		},
		_click: function(a) {
			var c = a.attr('data-eye');
			if (c === undefined) return false;
			var d = $("#" + c),
				cls = !d.attr("class") ? "" : d.attr("class"),
				value = !d.val() ? "" : d.val(),
				type = d.attr("type") === "password" ? "text" : "password",
				b = d.parent().find("b.placeTextB"),
				isB = b.length === 0 ? false : true;
			var s = d.attr("name") ? " name='" + d.attr("name") + "'" : "";
			s += d.attr("data-valid") ? " data-valid='" + d.attr("data-valid") + "'" : "";
			s += d.attr("data-error") ? " data-error='" + d.attr("data-error") + "'" : "";
			s += d.attr("placeholder") ? " placeholder='" + d.attr("placeholder") + "'" : "";
			var e = '<input readonly type="' + type + '" class="' + cls + '" value="' + value + '" id="' + c + '"' + s + ' />';
			if (type === "text") {
				if (isB) b.hide();
				d.parent().find(".icon-close.close").addClass("hide");
				d.removeAttr("id").hide();
				d.after(e);
				a.addClass("hidepwd")
			} else {
				d.prev("input").attr("id", c).val(value).show();
				if (isB && $.trim(value) === "") {
					d.prev("input").hide();
					b.show()
				}
				d.remove();
				a.removeClass("hidepwd")
			};
			$('body').on("click", "#" + c, function() {
				$(this).parent().find(".hidepwd").click();
				if (isB && $.trim($(this).val()) === "") {
					d.show();
					b.hide()
				}
				d.focus()
			})
		}
	};
	require.defaults = {};
	window.togglePwd = $.togglePwd = g
})(jQuery);
(function($) {
	var b, timerC, opt;
	var d = function(a) {
			a = $.extend(require.defaults, a || {});
			opt = a;
			d._clear();
			return (new require())._init()
		};

	function require(a) {};
	require.prototype = {
		_init: function() {
			timerC = opt.maxTime;
			this._sendVerify()
		},
		_sendVerify: function() {
			var a = this;
			if (timerC === 0) {
				d._clear();
				opt.after();
				timerC = opt.maxTime;
				return
			}
			timerC--;
			opt.ing(timerC);
			b = setTimeout(function() {
				a._sendVerify()
			}, 1000)
		}
	};
	d._clear = function() {
		clearTimeout(b)
	};
	require.defaults = {
		maxTime: 60,
		minTime: 0,
		ing: function(c) {},
		after: function() {}
	};
	window.countdown = $.countdown = d
})(jQuery);
$(function() {
	togglePwd();
	verifyCheck();
	$('body').on("keyup", "#password", function() {
		var t = $(this).val(),
			o = $(this).parent().find(".strength");
		if (t.length >= 6) {
			o.show();
			var l = verifyCheck.pwdStrong(t);
			o.find("b i").removeClass("on");
			for (var i = 0; i < l; i++) {
				o.find("b i").eq(i).addClass("on")
			}
		} else {
			o.hide()
		}
	})
});


/* 兴趣标签选择 */
; + function($) {
    "use strict";
    var defaults = {
        itemWidth: null,
        skin: '',
        multi: false,
        active: 'selected',
        full: false,
        colNum: null,
        dataKey: 'ui-choose',
        change: null,
        click: null
    };
    $.fn.ui_choose = function(options) {
        var _this = $(this),
            _num = _this.length;
        if (_num === 1) {
            return new UI_choose(_this, options);
        };
        if (_num > 1) {
            _this.each(function(index, el) {
                new UI_choose($(el), options);
            })
        }
    };

    function UI_choose(el, opt) {
        this.el = el;
        this._tag = this.el.prop('tagName').toLowerCase();
        this._opt = $.extend({}, defaults, opt);
        return this._init();
    }
    UI_choose.prototype = {
        _init: function() {
            var _data = this.el.data(this._opt.dataKey);
            if (_data)
                return _data;
            else
                this.el.data(this._opt.dataKey, this); if (this._tag == 'select') {
                this.multi = this.el.prop('multiple');
            } else {
                this.multi = this.el.attr('multiple') ? !! this.el.attr('multiple') : this._opt.multi;
            }
            var _setFunc = this['_setHtml_' + this._tag];
            if (_setFunc) {
                _setFunc.call(this);
            }
            if (this._opt.full) {
                this._wrap.addClass('choose-flex');
            }
            this._wrap.addClass(this._opt.skin);
            if (this.multi && !this._opt.skin)
                this._wrap.addClass('choose-type-right');
            this._bindEvent();
        },
        _setHtml_ul: function() {
            this._wrap = this.el;
            this._items = this.el.children('li');
            if (this._opt.itemWidth) {
                this._items.css('width', this._opt.itemWidth);
            }
        },
        _setHtml_select: function() {
            var _ohtml = '<ul class="ui-choose">';
            this.el.find('option').each(function(index, el) {
                var _this = $(el),
                    _text = _this.text(),
                    _value = _this.prop('value'),
                    _selected = _this.prop('selected') ? 'selected' : '',
                    _disabled = _this.prop('disabled') ? ' disabled' : '';
                _ohtml += '<li title="' + _text + '" data-value="' + _value + '" class="' + _selected + _disabled + '">' + _text + '</li> ';
            });
            _ohtml += '</ul>';
            this.el.after(_ohtml);
            this._wrap = this.el.next('ul.ui-choose');
            this._items = this._wrap.children('li');
            if (this._opt.itemWidth) {
                this._items.css('width', this._opt.itemWidth);
            }
            this.el.hide();
        },
        _bindEvent: function() {
            var _this = this;
            _this._wrap.on('click', 'li', function() {
                var _self = $(this);
                if (_self.hasClass('disabled'))
                    return;
                if (!_this.multi) {
                    var _val = _self.attr('data-value') || _self.index();
                    _this.val(_val);
                    _this._triggerClick(_val, _self);
                } else {
                    _self.toggleClass(_this._opt.active);
                    var _val = [];
                    _this._items.each(function(index, el) {
                        var _el = $(this);
                        if (_el.hasClass(_this._opt.active)) {
                            var _valOrIndex = _this._tag == 'select' ? _el.attr('data-value') : _el.index();
                            _val.push(_valOrIndex);
                        }
                    });
                    _this.val(_val);
                    _this._triggerClick(_val, _self);
                }
            });
            return _this;
        },
        _triggerChange: function(value, item) {
            item = item || this._wrap;
            this.change(value, item);
            if (typeof this._opt.change == 'function')
                this._opt.change.call(this, value, item);
        },
        _triggerClick: function(value, item) {
            this.click(value, item);
            if (typeof this._opt.click == 'function')
                this._opt.click.call(this, value, item);
        },
        _val_select: function(value) {
            if (arguments.length === 0) {
                return this.el.val();
            }
            var _oValue = this.el.val();
            if (!this.multi) {
                var _selectedItem = this._wrap.children('li[data-value="' + value + '"]');
                if (!_selectedItem.length)
                    return this;
                this.el.val(value);
                _selectedItem.addClass(this._opt.active).siblings('li').removeClass(this._opt.active);
                if (value !== _oValue) {
                    this._triggerChange(value);
                }
            } else {
                if (value == null || value == '' || value == []) {
                    this.el.val(null);
                    this._items.removeClass(this._opt.active);
                } else {
                    value = typeof value == 'object' ? value : [value];
                    this.el.val(value);
                    this._items.removeClass(this._opt.active);
                    for (var i in value) {
                        var _v = value[i];
                        this._wrap.children('li[data-value="' + _v + '"]').addClass(this._opt.active);
                    }
                }
                if (value !== _oValue) {
                    this._triggerChange(value);
                }
            }
            return this;
        },
        _val_ul: function(index) {
            if (arguments.length === 0) {
                var _oActive = this._wrap.children('li.' + this._opt.active);
                if (!this.multi) {
                    return _oActive.index() == -1 ? null : _oActive.index();
                } else {
                    if (_oActive.length == 0) {
                        return null;
                    }
                    var _this = this,
                        _val = [];
                    _oActive.each(function(index, el) {
                        var _el = $(el);
                        if (_el.hasClass(_this._opt.active)) {
                            _val.push(_el.index());
                        }
                    });
                    return _val;
                }
            }
            var _oIndex = this._val_ul();
            if (!this.multi) {
                var _selectedItem = this._wrap.children('li').eq(index);
                if (!_selectedItem.length)
                    return this;
                _selectedItem.addClass(this._opt.active).siblings('li').removeClass(this._opt.active);
                if (index !== _oIndex) {
                    this._triggerChange(index, _selectedItem);
                }
            } else {
                if (index == null || index == '' || index == []) {
                    this._items.removeClass(this._opt.active);
                } else {
                    index = typeof index == 'object' ? index : [index];
                    this._items.removeClass(this._opt.active);
                    for (var i in index) {
                        var _no = index[i];
                        this._wrap.children('li').eq(_no).addClass(this._opt.active);
                    }
                }
                if (index !== _oIndex) {
                    this._triggerChange(index);
                }
            }
            return this;
        },
        val: function() {
            return this['_val_' + this._tag].apply(this, arguments);
        },
        change: function(value, item) {},
        click: function(value, item) {},
        hide: function() {
            this._wrap.hide();
            return this;
        },
        show: function() {
            this._wrap.show();
            return this;
        }
    };
}(jQuery);

