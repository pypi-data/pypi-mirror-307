# -*- coding: utf-8 -*-
globalization = {
    "en": {
        "rerun failed scenario": "rerun failed scenario",
        "information association of failed operation": "information association of failed operation, run the {} time"
        " :[{}]",
        "start record": "start record",
        "stop record": "stop record",
        "rank": "rank",
        "parent": "parent",
        "children": "children",
        "sibling": "sibling",
        "offsprings": "offsprings",
        "and": "and",
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right",
        "modal_list": [
            "同意",
            "同意并继续",
            "同意并接受",
            "同意并进入应用",
            "允许",
            "始终允许",
            "使用App时允许",
            "立即开启",
            "好的",
            "下一步",
            "我知道了",
            "ok",
            "common update X",
            "Agree",
            "Allow",
            "DONG",
            "Accept All Cookies",
            "Wait",
            "接受所有Cookie",
            "跳过",
            "停止显示此广告",
            "暂时不用",
            "取消",
            "关闭",
            "放弃",
            "残忍拒绝",
            "ignore",
            "skip",
            "DONT ASK AGAIN",
            "禁止",
            "Deny",
        ],
        "break_list": [
            "text=System UI isn't responding",
            "text=Pixel Launcher isn't responding",
        ],
        "set_env": "set env",
        "check_env": "check env",
    },
    "zh-CN": {
        "rerun failed scenario": "\u5931\u8d25\u91cd\u65b0\u8fd0\u884c",
        "information association of failed operation": "失败运行的信息关联,运行第{}次:[{}]",
        "start record": "开始录屏",
        "stop record": "结束录屏",
        "rank": "第",
        "parent": "父节点",
        "children": "孩子",
        "sibling": "兄弟",
        "offsprings": "后代",
        "and": "并且",
        "up": "上",
        "down": "下",
        "left": "左",
        "right": "右",
        "modal_list": [
            "同意",
            "同意并继续",
            "同意并接受",
            "同意并进入应用",
            "允许",
            "始终允许",
            "使用App时允许",
            "立即开启",
            "好的",
            "下一步",
            "我知道了",
            "ok",
            "common update X",
            "Agree",
            "Allow",
            "DONG",
            "Accept All Cookies",
            "Wait",
            "接受所有Cookie",
            "跳过",
            "停止显示此广告",
            "暂时不用",
            "取消",
            "关闭",
            "放弃",
            "残忍拒绝",
            "ignore",
            "skip",
            "DONT ASK AGAIN",
            "禁止",
            "Deny",
        ],
        "break_list": [
            "text=System UI isn't responding",
            "text=Pixel Launcher isn't responding",
        ],
        "set_env": "设置条件",
        "check_env": "检查条件",
    },
}

step_language = {
    "en": {
        "install app[{param}]": ["install app[{param}]"],
        "start app[{param}]": ["start app[{param}]"],
    },
    "zh-CN": {
        "install app[{selector}]": ["安装APP[{selector}]"],
        "delete app[{selector}]": ["删除APP[{selector}]"],
        "start app[{selector}]": ["启动APP[{selector}]"],
        "clear app[{selector}]": ["清理APP[{selector}]"],
        "restart app": ["重启App"],
        "restart app[{selector}]": ["重启app[{selector}]"],
        "close app": ["关闭App"],
        "close app[{selector}]": ["关闭app[{selector}]"],
        "init device[{selector}]": ["设备初始化[{selector}]"],
        "connect device[{selector}]": ["连接设备[{selector}]"],
        "set current device[{selector}]": ["使用设备[{selector}]"],
        "start recording timeout[{param}]": ["开始录屏超时[{param}]"],
        "start record": ["开始录屏"],
        "stop record": ["结束录屏"],
        "go to url[{param}]": ["跳转到[{param}]", "跳转页面到[{param}]"],
        "set cookie name[{name}] value[{value}] url[{url}]": [
            "设置cookie 名称[{name}] 值[{value}] 网址[{url}]"
        ],
        "get cookie": ["获取cookie"],
        "get local storage": ["获取local storage"],
        "get session storage": ["获取session storage"],
        "return to previous page": ["返回上一页"],
        "go to home page": ["回到首页"],
        "logon account[{selector1}]password[{selector2}]": [
            "登录账号[{selector1}]密码[{selector2}]",
            "登陆账号[{selector1}]密码[{selector2}]",
        ],
        "logout": ["退出登陆", "退出登录"],
        "wait[{param}]seconds": ["等待[{param}]秒"],
        "screenshot": ["全屏截图"],
        "ocr [{selector}]": ["全屏扫描[{selector}]"],
        "ocr": ["全屏扫描"],
        "change ocr lang [{param}]": ["切换OCR语言[{param}]"],
        "exist image [{param}]": ["存在图像[{param}]"],
        "not exist image [{param}]": ["不存在图像[{param}]"],
        "information association of failed operation, run the {param1} time"
        " :[{param2}]": ["失败运行的信息关联,运行第{param1}次:[{param2}]"],
        "text[{selector}]property[{param2}]is {param3}": [
            "文案[{selector}]的属性[{param2}]为{param3}"
        ],
        "element[{selector}]property[{param2}]is {param3}": [
            "元素[{selector}]的属性[{param2}]为{param3}"
        ],
        "click[{selector}]": ["点击[{selector}]"],
        "ai icon click[{name}]": ["AI图标点击[{name}]"],
        "click text[{selector}]": ["点击文案[{selector}]"],
        "click ocr text[{selector}]": ["点击扫描文案[{selector}]"],
        "click ocr regional[{selector}] text[{param2}]": [
            "点击区域[{selector}]中扫描文案[{param2}]"
        ],
        "click ocr regional[{selector}]": ["点击区域[{selector}]"],
        "click image[{selector}]": ["点击图像[{selector}]"],
        "click position[{pos}]": ["点击屏幕位置[{pos}]"],
        "long click[{selector}]": ["长按[{selector}]"],
        "long click text[{selector}]": ["长按文案[{selector}]"],
        "long click ocr text[{selector}]": ["长按扫描文案[{selector}]"],
        "long click ocr regional[{selector}] text[{param2}]": [
            "长按区域[{selector}]中扫描文案[{param2}]"
        ],
        "long click ocr regional[{selector}]": ["长按区域[{selector}]"],
        "long click image[{selector}]": ["长按图像[{selector}]"],
        "long click position[{x},{y}]": ["长按屏幕位置[{x},{y}]"],
        "long click position[{x},{y}],duration={duration}": [
            "长按屏幕位置[{x},{y}],duration={duration}"
        ],
        "double click[{selector}]": ["双击[{selector}]"],
        "double click text[{selector}]": ["双击文案[{selector}]"],
        "double click ocr text[{selector}]": ["双击扫描文案[{selector}]"],
        "double click ocr regional[{selector}] text[{param2}]": [
            "双击区域[{selector}]中扫描文案[{param2}]"
        ],
        "double click ocr regional[{selector}]": ["双击区域[{selector}]"],
        "double click image[{selector}]": ["双击图像[{selector}]"],
        "double click position[{x},{y}]": ["双击屏幕位置[{x},{y}]"],
        "click home": ["点击HOME键"],
        "click anywhere": ["点击屏幕任意位置"],
        "input[{param1}]": ["输入[{param1}]"],
        "in[{selector}]input[{param2}]": ["在[{selector}]中输入[{param2}]"],
        "in ocr[{selector}]input[{param2}]": ["在扫描文字[{selector}]中输入[{param2}]"],
        "clear [{selector}] and input[{param2}]": ["在[{selector}]中清空并输入[{param2}]"],
        "element[{selector}]position not change in[{param2}]seconds": [
            "元素[{selector}]位置[{param2}]秒内未变动"
        ],
        "[{selector}]slide to {param2} distance[{param3}]": [
            "[{selector}]向{param2}滑动[{param3}]",
        ],
        "slide to {param1} distance[{param2}]": [
            "全屏向{param1}滑动[{param2}]",
            "向{param1}滑动[{param2}]",
        ],
        "from [{param1}] slide to [{param2}]": ["从[{param1}]向[{param2}]滑动"],
        "drag [{param1}] to [{param2}]": ["拖动[{param1}]到[{param2}]"],
        "click [{param1}] {selector} [{param2}]": [
            "点击 [{param1}] {selector} [{param2}]"
        ],
        "click img[{param1}] {selector} img[{param2}]": [
            "点击 图片[{param1}] {selector} 图片[{param2}]"
        ],
        "click ocr_text [{param1}] {selector} ocr_text[{param2}]": [
            "点击 文本[{param1}] {selector} 文本[{param2}]"
        ],
        "click img[{param1}] {selector} ocr_text[{param2}]": [
            "点击 图片[{param1}] {selector} 文本[{param2}]"
        ],
        "click ocr_text[{param1}] {selector} img[{param2}]": [
            "点击 文本[{param1}] {selector} 图片[{param2}]"
        ],
        "click img[{param1}] {selector} [{param2}]": [
            "点击 图片[{param1}] {selector} [{param2}]"
        ],
        "click poco[{param1}] {selector} img[{param2}]": [
            "点击 [{param1}] {selector} 图片[{param2}]"
        ],
        "click ocr_text[{param1}] {selector} [{param2}]": [
            "点击 文本[{param1}] {selector} [{param2}]"
        ],
        "click poco[{param1}] {selector} ocr_text[{param2}]": [
            "点击 [{param1}] {selector} 文本[{param2}]"
        ],
        "exist text[{selector}]": ["存在[{selector}]的文案"],
        "ocr exist text[{selector}]": ["扫描存在[{selector}]的文案"],
        "ocr regional[{selector}] exist text[{param2}]": [
            "扫描区域[{selector}]中存在[{param2}]的文案"
        ],
        "ocr contain text[{selector}]": ["扫描包含[{selector}]的文案"],
        "ocr regional[{selector}] contain text[{param2}]": [
            "扫描区域[{selector}]中包含[{param2}]的文案"
        ],
        "not exist text[{selector}]": ["不存在[{selector}]的文案"],
        "ocr not exist text[{selector}]": ["扫描不存在[{selector}]的文案"],
        "text[{selector}]disappear": ["文案[{selector}]消失"],
        "exist[{selector}]element": ["存在[{selector}]的元素"],
        "not exist element[{selector}]": ["不存在[{selector}]的元素"],
        "element[{selector}]disappear": ["元素[{selector}]消失"],
        "the text of element[{selector}]is[{param2}]": ["[{selector}]的文案为[{param2}]"],
        "the text of element[{selector}]include[{param2}]": [
            "[{selector}]的文案包含[{param2}]"
        ],
        "page rendering complete appears element[{selector}]": [
            "页面渲染完成出现元素[{selector}]"
        ],
        "page ocr complete find text[{selector}]": ["页面扫描完成出现文字[{selector}]"],
        "existing element[{selector}]": ["存在元素[{selector}]"],
        "in[{p_selector}]from {param2} find[{c_selector}]element": [
            "在[{p_selector}]中向{param2}查找[{c_selector}]的元素"
        ],
        "from {param1} find[{selector}]element": ["向{param1}查找[{selector}]的元素"],
        "from {param1} find[{selector}]text": ["向{param1}扫描[{selector}]的文案"],
        "from {param1} find[{selector}]image": ["向{param1}查找[{selector}]的图像"],
        "unblock the current page": ["解除当前页面限制"],
        "current page is [{param}]": ["当前页面是[{param}]"],
        "current page is not last page": ["当前页面已不是上一个指定页面"],
        "from [{selector}] select [{param2}]": ["在[{selector}]中选择[{param2}]"],
        "exist [{p_selector}] subNode [{c_selector}] element": [
            "存在[{p_selector}]的[{c_selector}]的元素"
        ],
        "the text of element [{p_selector}] subNode [{c_selector}] is "
        "[{param3}]": ["[{p_selector}]的[{c_selector}]文案为[{param3}]"],
        "cache service request [{service}]": ["缓存服务请求[{service}]"],
        "remove service request cache [{service}]": ["移除请求缓存[{service}]"],
        "remove all service request caches": ["移除所有请求缓存"],
        "listening service [{service}] bind mockCase[{mock_case_id}]": [
            "监听服务[{service}]绑定MockCase[{mock_case_id}]"
        ],
        "remove service listener [{service}]": ["移除服务监听[{service}]"],
        "remove all service listeners": ["移除所有服务监听"],
        "compare service request [{service}] with json file "
        "[{target_data_path}]": ["验证服务请求[{service}]与[{target_data_path}]一致"],
        "compare service non-json request [{service}] with non-json file "
        "[{target_data_path}]": ["验证服务非json请求[{service}]与[{target_data_path}]一致"],
        "service request [{service}] request parameter [{target_json_path}] "
        "is [{expect_value}]": [
            "验证服务[{service}]的请求参数[{target_json_path}]" "与[{expect_value}]一致"
        ],
        "set env {key} {param}": ["设置条件{key} {param}"],
        "check env {key} {param}": ["检查条件{key} {param}"],
        "can set [{key}]": ["CAN信号设置[{key}]"],
        "can get [{key}]": ["CAN信号读取[{key}]"],
        "can stop [{key}]": ["CAN信号停止[{key}]"],
        "DAQ check[{key}]": ["DAQ检查[{key}]"],
        "PW read[{key}]": ["PW读取[{key}]"],
        "PW write[{key}]": ["PW写入[{key}]"],
        "[{key}] times": ["[{key:int}]次"],
        "attribute assert [{xpath}] text [{operator}] [{key}]": [
            "属性断言[{xpath}]的文本属性[{operator}][{key}]"
        ],
        "get [{xpath}] text and save as [{param}]": ["获取[{xpath}]的文本属性并暂存为[{param}]"],
        "expression assert [{param}]": ["表达式断言[{param}]"],
        "img [{selector}]slide to {param2} distance[{param3}]": [
            "图片[{selector}]向{param2}滑动[{param3}]",
        ],
        "save page as [{param}]": ["暂存页面图像为变量[{param}]"],
        "image assert [{param}]": ["断言页面变化[{param}]"],
        "image assert not [{param}]": ["断言页面无变化[{param}]"],
        "ai icon assert[{name}]": ["AI图标断言[{name}]"],
        "continue monitor": ["继续系统框监控"],
        "resume monitor": ["暂停系统框监控"],
        "var assign[{name}={content}]": ["变量赋值[{name}={content}]"],
        "var func assign[{name}={func}]": ["函数变量赋值[{name}={func}]"],
        "var operate[{name}.{func}]": ["变量处理[{name}.{func}]"],
        "var fundamental rules": ["变量四则运算[{name}={expression}]"],
    },
}
