#language:zh-CN

 功能: flybirds 检测 条件

   场景: exist text true--
      当 设置条件 <check exist text> <0>
      当 存在[机票1,timeout=5]的文案
      那么 设置条件 <check exist text> <1>
      那么 点击[text=火车票]
      那么 设置条件 <finish_condition_1> <1>

   场景: exist text failed--
      当 检查条件 <check exist text> <0>
      那么 点击[text=机票]
      那么 设置条件 <finish_condition_1> <1>

   场景: test end--
     当 检查条件 <finish_condition_1> <1>
     那么 点击[text=查 询]