# language: zh-CN
功能: flybirds功能测试-android verify element

场景: 验证元素--元素文案
当  启动APP[ctrip.android.view]
而且 页面渲染完成出现元素[text=机票]
那么 [text=机票]的文案为[机票]
那么 [text=机票]的文案包含[机]


场景: 验证元素--元素属性
当  启动APP[ctrip.android.view]
而且 页面渲染完成出现元素[text=机票]
那么 元素[text=机票]的属性[text]为机票


场景: 属性断言
当 属性断言[android.view.ViewGroup -> 1孩子 android.view.ViewGroup -> 1孩子 android.widget.TextView -> 10孩子 微信, path=true]的文本属性[=][微信]


场景: 表达式断言
当 获取[text=胡萝卜]的文本属性并暂存为[res1]
当 获取[text=黄瓜]的文本属性并暂存为[res2]
当 表达式断言[res1 != res2]
#  支持+、-、*、/、==、!=、()、//
#  等于使用==，不要用=，表达式需要满足python的表达式格式
#  表达式中的空格无意义，加不加都可以

场景: 操作前后，对比页面区别
当 暂存页面图像为变量[current page]
当 点击[textMatches=鸿星尔克.*]
当 断言页面变化[current page]
当 断言页面无变化[current page]
# 图像断言的变量名 与 表达式断言的变量名 可以相同，二者不在同一个命名空间