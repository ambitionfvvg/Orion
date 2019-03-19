function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // 页面加载后尝试向后端获取实名认证的信息
    // $.get("/api/v1.0/user/auth",function (resp) {
    //      // 4101代表用户未登录
    //     if ("4101" == resp.errno) {
    //         location.href = "/login.html";
    //     } else if ("0" == resp.errno) {
    //         // 如果返回的数据中real_name与id_card不为null，表示用户有填写实名信息
    //         if (resp.data.real_name && resp.data.id_card) {
    //             $("#real-name").val(resp.data.real_name);
    //             $("#id-card").val(resp.data.id_card);
    //             // 给input添加disabled属性，禁止用户修改
    //             $("#real-name").prop("disabled", true);
    //             $("#id-card").prop("disabled", true);
    //             // 隐藏提交保存按钮
    //             $("#form-auth>input[type=submit]").hide();
    //         }
    //     } else {
    //         alert(resp.errmsg);
    //     }
    // },"json");

    // 上传实名信息

    // 管理实名信息表单的提交行为
    $("#form-label").submit(function(e){
        e.preventDefault();
        // 如果用户没有填写完整，展示错误信息
		// alert($("#part_no option:selected").text());
		var lex_pn=$("#lex_pn option:selected").text();  //获取Select选择的Text
        // var part_no = $("#part_no").val();
        var qty = $("#qty").val();
		var po = $("#po").val();
		var row = $("#row").val();
		// var lex_pn = $("#lex_pn").val();
		
        // var idCard = $("#id-card").val();
        // if (realName == "" ||  idCard == "") {
        //     $(".error-msg").show();
        // }

        // 将表单的数据转换为json字符串
        var data = {
            // part_no: part_no,
            qty: qty,
			po:po,
            lex_pn:lex_pn,
            row:row,
        };
        var jsonData = JSON.stringify(data);

        // 向后端发送请求
        $.ajax({
            url:"/label",
            type:"post",
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFTOKEN": getCookie("csrf_token")
            },
            success: function (resp) {
                if (0 == resp.errno) {
                    alert("打印成功")
                    // $(".error-msg").hide();
                    // // 显示保存成功的提示信息
                    // showSuccessMsg();
                    // $("#real-name").prop("disabled", true);
                    // $("#id-card").prop("disabled", true);
                    // $("#form-auth>input[type=submit]").hide();
                }else if(1 == resp.errno){
                    alert("参数不完整")
                }
            }
        });
    });

    $("#form-reprint").submit(function(e){
        e.preventDefault();

        var posn = $("#posn").val();

        // 将表单的数据转换为json字符串
        var data = {
            posn: posn,
        };
        var jsonData = JSON.stringify(data);

        // 向后端发送请求
        $.ajax({
            url:"/reprint",
            type:"post",
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFTOKEN": getCookie("csrf_token")
            },
            success: function (resp) {
                if (0 == resp.errno) {
                    alert("打印成功")
                    // $(".error-msg").hide();
                    // // 显示保存成功的提示信息
                    // showSuccessMsg();
                    // $("#real-name").prop("disabled", true);
                    // $("#id-card").prop("disabled", true);
                    // $("#form-auth>input[type=submit]").hide();
                }else if(1 == resp.errno){
                    alert("参数不完整")
                }
            }
        });
    })
})