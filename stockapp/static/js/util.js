/**
 * �ַ�����
 * @type {{init, isNotEmpty, isEmpty}}
 */
var StringUtil = function () {
    var value;

    var init = function (value) {
        this.value = value;
    };

    var isNotEmpty = function () {
        var flag = true;
        if (this.value == null || this.value == "") {
            return false;
        }
        return flag;
    };

    var isEmpty = function () {
        var flag = false;
        if (this.value == null || this.value == "") {
            flag = true;
        }
        return flag;
    };

    return {
        init: function (value) {
            init(value);
        },
        isNotEmpty: function (value) {
            init(value);
            return isNotEmpty();
        },
        isEmpty: function (value) {
            init(value);
            return isEmpty();
        }
    }
}();

/**
 * ���鹤����
 * @returns {{init: Function, isNotEmpty: Function}}
 * @constructor
 */
var CollectionUtil = function () {
    var collection;

    var init = function (collection) {
        this.collection = collection;
    };

    var isNotEmpty = function () {
        var b = false;
        if (this.collection != null) {
            var length = this.collection.length;
            if (length > 0) {
                b = true;
            }
        }
        return b;
    };

    return {
        init: function (collection) {
            init(collection);
        },
        isNotEmpty: function (collection) {
            init(collection);
            return isNotEmpty();
        }
    };
}();

/**
 * url parse param
 * @type {{paramStr: string, getParam: Function}}
 */
var UrlUtil = {
    paramStr: window.location.search.substr(1),
    getParam: function (param) {
        var reg = new RegExp("(^|&)" + param + "=([^&]*)(&|$)", "i");
        var r = this.paramStr.match(reg);
        if (null == r) {
            return null;
        }
        return r[2];
    }
};

/**
 * msg tip
 * @param config
 * @constructor
 */
var Toast = function (config) {
    this.context = config.context == null ? $('body') : config.context;// 上下文
    this.message = config.message;// 显示内容
    this.time = config.time == null ? 3000 : config.time;// 持续时间
    this.left = config.left;// 距容器左边的距离
    this.top = config.top;// 距容器上方的距离
    this.msgEntity = null;
    this.init();
};
Toast.prototype = {
    // 初始化显示的位置内容等
    init: function () {
        $("#toastMessage").remove();
        // 设置消息体
        var msgDIV = new Array();
        msgDIV.push('<div id="toastMessage">');
        msgDIV.push('<span>' + this.message + '</span>');
        msgDIV.push('</div>');
        this.msgEntity = $(msgDIV.join('')).appendTo(this.context);
        // 设置消息样式
        var left = this.left == null ? this.context.width() / 2
            - this.msgEntity.find('span').width() / 2 : this.left;
        var top = this.top == null ? (document.body.clientHeight / 2 + 'px')
            : this.top;
        this.msgEntity.css({
            position: 'absolute',
            top: top,
            'z-index': '99',
            left: left,
            'background-color': 'black',
            color: 'white',
            'font-size': '18px',
            padding: '10px',
            'border-radius': '4px',
            margin: '10px'
        });
        this.msgEntity.hide();
    },
    // 显示动画
    show: function () {
        this.msgEntity.fadeIn(this.time / 2);
        this.msgEntity.fadeOut(this.time / 2);
    }
};

var Cmd = {
    SAVE: 1,
    GET: 2,
    LIST: 3,
    SIGN_UP: 4,
    SIGN_IN: 5,
    MODIFY_PWD: 6,
    DELETE: 7,
    RESET_PWD: 8,
    APPLY: 9,
    APPROVER: 10,
    REJECT: 11,
    DOWNLOAD: 12,
    FEEDBACK: 13,
    UPLOAD: 14,
    EXPORT: 15,
    ADD: 16,
    UPDATE: 17,
    GET_ID: 18,
    ALL: 19,
    PUSH: 20,
    SAVE_OPERATE_IMG: 21,
    QUERY_OPERATE_IMG: 22,
    STATISTIC: 24,
    PUSH_SMS: 25,
    PUSH_LC: 26,
    PUSH_EMAIL: 27,
    PUSH_TIPS: 28,
    PUSH_LOG: 29,
    LOOK_PSN_DETAIL: 33,
    EXPORT_PSN_EXCEL: 34,
    EXPORT_PSN_BIN: 35,

};

var Role = {
    1: 2147483647, // admin, 1+2+4+8+16+32+64+128+256+512+1024+2048+4096+8192+16384+32768+65536+131072+262144+524288+1048576+2097152+4194304+8388608+16777216+33554432+67108864+134217728+268435456+536870912+1073741824
    2: 85975055, // normal, 1+2+4+8+8192+16384+32768+65536+131072+262144+524288+1048576+16777216+67108864
    3: 903880689, // factory, 1+16+32+64+128+256+512+1024+2048+4096+2097152+4194304+8388608+16777216+67108864+268435456+536870912+1073741824
    4: 2147483647 // super
};

function efRequest(_this, url, method, params, func, async) {
    if (undefined == async) {
        async = true;
    }
    $.ajaxSetup({
        dataFilter: function (response) {
            if (response.indexOf('传世未来登陆页面') !== -1) {
                //如果返回的文本包含"登陆页面"，就跳转到登陆页面
                top.location.href = '/html/index.html';
                //一定要返回一个字符串不能不返回或者不给返回值，否则会进入success方法
                return "";
            } else {
                //如果没有超时直接返回
                return response;
            }
        }
    });
    $.ajax({
        url: url,
        type: method,
        async: async,
        data: params,
        dataType: "json",
        success: function (result) {
            console.log(result);
            func(_this, result);
        },
        error: function (msg) {
            if (301 == msg.status || 302 == msg.status) {
                window.location.href = "index.html";
            } else {
                new Toast({
                    context: $("body"),
                    message: "服务器回老家了，操作失败~"
                }).show();
            }
        }
    });
}

function pageBar(currentPage, pageCount) {
    var firstPage = 1;
    var maxPage = pageCount;
    var html = [];
    if (maxPage > 10) {
        if (currentPage + 5 < maxPage) {
            if (currentPage + 5 < 10) {
                maxPage = 10;
            } else {
                maxPage = currentPage + 5;
            }
        }
        if (currentPage - 5 > 1) {
            firstPage = currentPage - 5;
            if (maxPage - firstPage < 10) {
                firstPage -= (firstPage - (maxPage - 10));
            }
        }
    }
    if (1 == currentPage) {
        html.push('<li class="disabled"><span>&laquo;<span class="sr-only">(current)</span></span></li>');
    } else {
        html.push('<li><a href="#' + (currentPage - 1) + '">&laquo;</a></li>');
    }
    for (var i = firstPage; i <= maxPage; ++i) {
        if (i == currentPage) {
            html.push('<li class="active"><span>' + i + ' <span class="sr-only">(current)</span></span></li>');
        } else {
            html.push('<li><a href="#' + i + '">' + i + '</a></li>');
        }
    }
    if (currentPage != maxPage) {
        html.push('<li><a href="#' + (currentPage + 1) + '">&raquo;</a></li>');
    } else {
        html.push('<li class="disabled"><span>&raquo;<span class="sr-only">(current)</span></span></li>');
    }
    if (pageCount > currentPage + 5) {
        html.push('<p style="float:right;margin:8px"><a href="#' + pageCount + '">共' + pageCount + '页</a></p>');
    }
    html.push('<input type="text" size="3" id="targetPageNo"/><button type="submit" id="pageGoto">GO</button>');
    $('.pagination').html(html.join(''));
}

function uploadEfFile(fileId, fileType, bussinessType, callback) {
    var jwtToken = undefined;
    efRequest(this, "/upload/uploadAction.do", "get", {}, function (_this, result) {
        jwtToken = result['jwtToken'];
    }, false);
    console.log("jwt=" + jwtToken);
    $.ajaxFileUpload({
        url: "/upload?t=" + fileType + "&b=" + bussinessType + "&jwt=" + jwtToken,
        secureuri: false,
        fileElementId: fileId,
        dataType: 'json',
        success: function (data, status) {
            console.log("success");
            console.log(data);
            new Toast({
                message: 0 == data['ret'] ? "上传成功" : "上传失败"
            }).show();
            callback(data);
        },
        error: function (data, status, e)//服务器响应失败处理函数
        {
            console.log(data);
            console.log(status);
            console.log(e);
        }
    });
}

/**
 * 日期格式化函数
 * @param timestamp
 * @param chinese
 * @returns {*}
 */
function dateformat(timestamp, chinese) {
    if (!timestamp) {
        datetime = new Date().toLocaleString();
    } else {
        datetime = new Date(parseInt(timestamp)).toLocaleString();
    }
    if (!chinese) {
        return datetime.replace(/年|月/g, '-').replace(/日/g, '');
    }
    return datetime;
}

/**
 * 校验手机号是否合法
 *
 * @param $poneInput
 * @returns {boolean}
 */
function isPoneAvailable(phone) {
    var reg = /^[1][3,4,5,7,8][0-9]{9}$/;
    if (!reg.test(phone)) {
        return false;
    } else {
        return true;
    }
}

/**
 * 扩展日期格式化参数
 * @param fmt 格式 "yyyy-MM-dd HH:mm:ss"
 * @returns {*}
 */
Date.prototype.format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
