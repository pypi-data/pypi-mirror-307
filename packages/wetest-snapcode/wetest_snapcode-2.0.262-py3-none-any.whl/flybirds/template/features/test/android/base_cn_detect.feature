# language: zh-CN
功能: flybirds功能测试-DAQ PW CAN检查

场景: 验证检查--音频检测
当   DAQ检查[chsname=左喇叭检测, channel=AI0]

场景: 验证检查--程控电源
当   PW读取[cmd=CURR]
当   PW写入[cmd=CURR, value=1]

场景: 验证检查--CAN报文
当  CAN信号设置[id=301, msg_name=Cockpit_Ctrl, sig_name=[power_gear,lock_status], value=[7,1], mode=1, period=1, speed=1, times=1]
当  CAN信号读取[id=301, msg_name=Cockpit_Ctrl, sig_name=[power_gear,lock_status]]
当  CAN信号停止[id=301, msg_name=Cockpit_Ctrl, sub_id=[]]
