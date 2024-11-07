 # language: en
 Feature: flybirds test feature-android click

   Scenario: exist text true--
      Then set env check_exist_text 0
      When exist text[机票1,timeout=5]
      Then set env check_exist_text 1
      And click[text=火车票]
      And set env finish_condition_1 1

    Scenario: exist text failed--
      When check env check_exist_text 0
      And click[text=机票]
      And set env finish_condition_1 1

   Scenario: test end--
     When check env finish_condition_1 1
     Then click[text=查 询]