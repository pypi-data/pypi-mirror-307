# language: zh-CN
功能:  flybirds功能测试-ios click

场景: 验证点击--点击屏幕位置
当   启动APP[com.ctrip.inner.wireless]
而且 点击屏幕位置[580,1200]
而且 等待[5]秒
那么 全屏截图
那么 关闭App


场景: 验证点击--点击元素
当  启动APP[com.ctrip.inner.wireless]
而且 页面渲染完成出现元素[label=机票]
而且 点击[label=机票]
那么 全屏截图


场景: 验证点击--点击并输入
当  启动APP[com.ctrip.inner.wireless]
而且 页面渲染完成出现元素[label=搜索]
而且 在[label=搜索]中输入[flybirds]
而且 等待[10]秒
那么 全屏截图

场景: 验证点击--在已经聚焦情况下直接输入文本
当  启动APP[ctrip.android.view]
而且 页面渲染完成出现元素[label=搜索]
而且 点击[label=搜索]
那么 输入[上海]
那么 全屏截图

场景: 验证点击--点击元素上/下/左/右元素
当  启动APP[ctrip.android.view]
而且 页面渲染完成出现元素[label=机票]
那么 点击 [label=机票] 右 [label=火车票]
而且 等待[5]秒
那么 全屏截图
那么 关闭App

场景: 验证点击--点击元素上/下/左/右元素
当  启动APP[ctrip.android.view]
而且 页面渲染完成出现元素[label=机票]
# 那么 点击 [label=微信] 右 [label=已开启]
# 那么 点击 图片[img/2.jpg] 左 图片[img/3.jpg]
那么 点击 文本[火车票] 下 文本[租车]
# 那么 点击 图片[img/3.jpg] 上 文本[酒店]
# 那么 点击 文本[酒店] 下 图片[img/3.jpg]
# 那么 点击 图片[img/3.jpg] 上 [text=酒店]
# 那么 点击 [label=酒店] 下 图片[img/3.jpg]
# 那么 点击 文本[旅游] 左 [label=机票]
# 那么 点击 [label=微信] 右 文本[已开启]
而且 等待[5]秒
那么 全屏截图
那么 关闭App


