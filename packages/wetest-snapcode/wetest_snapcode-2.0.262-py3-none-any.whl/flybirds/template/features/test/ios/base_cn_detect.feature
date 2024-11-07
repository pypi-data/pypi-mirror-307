# language: zh-CN
功能: flybirds功能测试-DAQ PW CAN检查

场景: 验证检查--检查DAQ
当   DAQ检查[AI0]
# 当   DAQ检查[AI0, timeout=5]

场景: 验证检查--读取PW
当   PW读取[CURR]
# 当   PW读取[CURR, timeout=5]

场景: 验证检查--写入PW
当   PW写入[CURR] 1
# 当   PW写入[CURR, timeout=5] 1

场景: 验证检查--语音检测
# 当   语音检测[cos:///car/upload/test.wav, mock=False]
当   语音检测[cos:///car/upload/test.wav]
# 等价于     语音检测[cos:///car/upload/test.wav, mock=True]

场景: 验证检查--CAN报文
# 当   CAN控制数值设置[name=LCDA_1, id=567, data=00hgyui]
# 当   CAN控制数值读取[name=LCDA_1, id=567]
当    CAN控制报文发送[00 00 01 00  00 00 01 02]
# 当   CAN控制周期报文发送开始[id=678, timer=1]
# 当    CAN控制周期报文发送结束[id=678]
