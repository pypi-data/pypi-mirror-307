 # language: en
 Feature: flybirds test feature-android click

   Scenario: test click--long click position
     When start app[ctrip.android.view]
     And  long click position[580,1200]
     And  wait[5]seconds
     Then screenshot
     Then close app


   Scenario: test click--long click text
     When start app[ctrip.android.view]
     And page rendering complete appears element[text=机票]
     And long click[text=机票]
     Then screenshot

