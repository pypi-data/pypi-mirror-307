# language: zh-CN
功能: flybirds功能测试-control statements

场景: 验证流程控制--嵌套if
IF   存在[label=机票]的元素
那么  点击[label=机票]
IF   存在[label=北京]的元素
那么  点击[label=北京]
IF  存在[label=昆明]的元素
那么   点击[label=昆明]
ENDIF
ENDIF
ENDIF
那么   点击屏幕位置[580,1200]

场景:验证流程控制--分支if
IF   存在[label=机票]的元素
那么  点击[label=机票]
ELIF 存在[label=微信]的元素
那么  点击[label=微信]
ELSE
那么  点击屏幕位置[580,1200]
ENDIF
那么   全屏向下滑动[600]

场景: 验证流程控制--循环，break跳出
循环  存在[label=搜索]的元素
那么 点击[label=搜索]
那么  全屏向下滑动[600]
IF 存在[label=微信]的元素
那么   点击[label=微信]
BREAK
ENDIF
那么  全屏向下滑动[600]
ENDFOR
当 点击[label=登录]

场景: 验证流程控制--循环次数
循环  [3]次
而且 存在[label=搜索]的元素
那么 点击[label=搜索]
那么  全屏向下滑动[600]
IF 存在[label=微信]的元素
那么   点击[label=微信]
BREAK
ENDIF
那么  全屏向下滑动[600]
ENDFOR
当 点击[label=上海]