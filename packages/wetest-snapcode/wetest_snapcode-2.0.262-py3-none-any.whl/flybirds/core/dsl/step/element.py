# -*- coding: utf-8 -*-
"""
This module defines the steps related to the UI element.
"""
from behave import step

from flybirds.core.global_context import GlobalContext as g_Context
from flybirds.utils.dsl_helper import ele_wrap, timeout


@step("text[{selector}]property[{param2}]is {param3}")
@ele_wrap
def text_attr_equal(context, selector=None, param2=None, param3=None):
    """
    Check if the value of the attribute param2 of the text element param1 in
     the page is param3

    :param context: step context
    :param selector: locator string for text element (or None).
    :param param2: attribute Name
    :param param3: expected Value
    """
    g_Context.step.text_attr_equal(context, selector, param2, param3)


@step("element[{selector}]property[{param2}]is {param3}")
@ele_wrap
def ele_attr_equal(context, selector=None, param2=None, param3=None):
    """
    Check if the value of the attribute param2 of the selector element param1
     in the page is param3

    :param context: step context
    :param selector: locator string for selector element (or None).
    :param param2: attribute Name
    :param param3: expected Value
    """
    g_Context.step.ele_attr_equal(context, selector, param2, param3)


@step("click[{selector}]")
@ele_wrap
def click_ele(context, selector=None):
    """
    Click on the selector element
    :param context: step context
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.click_ele(context, selector)


@step("ai icon click[{name}]")
@ele_wrap
def ai_icon_click(context, name):
    g_Context.step.ai_icon_click(context, name)


@step("long click[{selector}]")
@ele_wrap
def long_click_ele(context, selector=None):
    """
    Click on the selector element
    :param context: step context
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.click_ele(context, selector, "long_click,duration=2")


@step("double click[{selector}]")
@ele_wrap
def double_click_ele(context, selector=None):
    """
    Click on the selector element
    :param context: step context
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.click_ele(context, selector, "double_click,click_count=2")


@step("click text[{selector}]")
@ele_wrap
def click_text(context, selector=None):
    """
    Click on the text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.click_text(context, selector)


@step("long click text[{selector}]")
@ele_wrap
def long_click_text(context, selector=None):
    """
    Click on the text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.click_text(context, selector, "long_click,duration=2")


@step("double click text[{selector}]")
@ele_wrap
def double_click_text(context, selector=None):
    """
    Click on the text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.click_text(context, selector, "double_click,click_count=2")


@step("click ocr text[{selector}]")
@ele_wrap
def click_ocr_text(context, selector=None):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.click_ocr_text(context, selector)


@step("long click ocr text[{selector}]")
@ele_wrap
def long_click_ocr_text(context, selector=None):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.click_ocr_text(context, selector, "long_click,duration=2")


@step("double click ocr text[{selector}]")
@ele_wrap
def double_click_ocr_text(context, selector=None):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.click_ocr_text(context, selector, "double_click,click_count=2")


@step("click ocr regional[{selector}] text[{param2}]")
@ele_wrap
def click_ocr_regional_text(context, selector, param2):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    :param2 selector: locator string for text element (or None).
    """
    g_Context.step.ocr(context)
    g_Context.step.click_regional_ocr_text(context, selector, param2)


@step("long click ocr regional[{selector}] text[{param2}]")
@ele_wrap
def long_click_ocr_regional_text(context, selector, param2):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    :param2 selector: locator string for text element (or None).
    """
    g_Context.step.ocr(context)
    g_Context.step.click_regional_ocr_text(
        context, selector, param2, "long_click,duration=2"
    )


@step("double click ocr regional[{selector}] text[{param2}]")
@ele_wrap
def double_click_ocr_regional_text(context, selector, param2):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    :param2 selector: locator string for text element (or None).
    """
    g_Context.step.ocr(context)
    g_Context.step.click_regional_ocr_text(
        context, selector, param2, "double_click,click_count=2"
    )


@step("click ocr regional[{selector}]")
@ele_wrap
def click_regional_ocr(context, selector):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.ocr(context)
    g_Context.step.click_regional_ocr(context, selector)


@step("long click ocr regional[{selector}]")
@ele_wrap
def long_click_regional_ocr(context, selector):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.ocr(context)
    g_Context.step.click_regional_ocr(context, selector, "long_click,duration=2")


@step("double click ocr regional[{selector}]")
@ele_wrap
def double_click_regional_ocr(context, selector):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.ocr(context)
    g_Context.step.click_regional_ocr(context, selector, "double_click,click_count=2")


@step("click image[{selector}]")
@ele_wrap
def click_image(context, selector=None):
    """
    Click on the image
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.click_image(context, selector)


@step("long click image[{selector}]")
@ele_wrap
def long_click_image(context, selector=None):
    """
    Click on the image
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.click_image(context, selector, "long_click,duration=2")


@step("double click image[{selector}]")
@ele_wrap
def double_click_image(context, selector=None):
    """
    Click on the image
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.click_image(context, selector, "double_click,click_count=2")


@step("click position[{pos}]")
@ele_wrap
def click_coordinates(context, pos):
    """
    Click on the screen coordinates
    :param context: step context
    :param x: Coordinate x-axis
    :param y: Coordinate y-axis.
    """
    g_Context.step.click_coordinates_pos(context, pos)


@step("long click position[{x},{y}]")
@ele_wrap
def long_click_coordinates(context, x=None, y=None):
    """
    Click on the screen coordinates
    :param context: step context
    :param x: Coordinate x-axis
    :param y: Coordinate y-axis.
    """
    g_Context.step.click_coordinates(context, x, y, "long_click,duration=2")


@step("long click position[{x},{y}],duration={duration}")
@ele_wrap
def long_click_coordinates(context, x=None, y=None, duration=0):
    """
    Click on the screen coordinates
    :param context: step context
    :param x: Coordinate x-axis
    :param y: Coordinate y-axis.
    :param duration: Click duration.
    """
    g_Context.step.click_coordinates(
        context, x, y, "long_click,duration=" + str(duration)
    )


@step("double click position[{x},{y}]")
@ele_wrap
def double_click_coordinates(context, x=None, y=None):
    """
    Click on the screen coordinates
    :param context: step context
    :param x: Coordinate x-axis
    :param y: Coordinate y-axis.
    :param duration: Click duration.
    """
    g_Context.step.click_coordinates(context, x, y, "double_click,click_count=2")


@step("input[{param1}]")
@ele_wrap
def only_input(context, param1=None):
    """
    Input text on the target device. Text input widget must be active first.
    :param context: step context
    :param param1: string to be input
    :return:
    """
    g_Context.step.only_input(context, param1)


@step("in[{selector}]input[{param2}]")
@ele_wrap
def ele_input(context, selector=None, param2=None):
    """
    Enter the value param2 in the selector element param1
    :param context: step context
    :param selector: locator string for selector element (or None).
    :param param2: string to be input
    """
    g_Context.step.ele_input(context, selector, param2)


@step("in ocr[{selector}]input[{param2}]")
@ele_wrap
def ocr_text_input(context, selector=None, param2=None):
    """
    Enter the value param2 in the selector element param1
    :param context: step context
    :param selector: locator string for selector element (or None).
    :param param2: string to be input
    """
    g_Context.step.ocr(context)
    g_Context.step.ocr_text_input(context, selector, param2)


@step("element[{selector}]position not change in[{param2}]seconds")
@ele_wrap
def position_not_change(context, selector=None, param2=None):
    """
    Check that the position of the selector element param1 has not changed
    within param2 seconds
    :param context: step context
    :param selector: locator string for selector element (or None).
    :param param2:
    """
    g_Context.step.position_not_change(context, selector, param2)


@step("[{selector}]slide to {param2} distance[{param3}]")
@ele_wrap
def ele_swipe(context, selector=None, param2=None, param3=None):
    """
    Selector element param1 slides in the specified direction param2 and
    slides the specified distance param3
    :param context: step context
    :param selector: locator string for selector element (or None).
    :param param2: slide direction (top/bottom/left/right)
    :param param3: slide distance
    """
    g_Context.step.ele_swipe(context, selector, param2, param3)


@step("from [{param1}] slide to [{param2}]")
@ele_wrap
def coord_swipe(context, param1, param2):
    g_Context.step.coord_swipe(context, param1, param2)


@step("img [{selector}]slide to {param2} distance[{param3}]")
@ele_wrap
def img_swipe(context, selector=None, param2=None, param3=None):
    g_Context.step.img_swipe(context, selector, param2, param3)


@step("slide to {param1} distance[{param2}]")
@ele_wrap
def full_screen_swipe(context, param1=None, param2=None):
    """
    Slide the full screen in the specified direction for the specified distance
    :param context: step context
    :param param1: slide direction (top/bottom/left/right)
    :param param2: slide distance
    """
    g_Context.step.full_screen_swipe(context, param1, param2)


@step("drag [{param1}] to [{param2}]")
@ele_wrap
def ele_drag(context, param1, param2):
    g_Context.step.ele_drag(context, param1, param2)


@step("exist text[{selector}]")
@ele_wrap
def wait_text_exist(context, selector=None):
    """
    The specified text element string exists in the page
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.wait_text_exist(context, selector)


@step("ocr exist text[{selector}]")
@ele_wrap
def ocr_text_exist(context, selector=None):
    """
    The specified text element string exists in the page
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.ocr_text_exist(context, selector)


@step("ocr regional[{selector}] exist text[{param2}]")
@ele_wrap
def ocr_regional_text_exist(context, selector, param2):
    """
    The specified text element string exists in the page
    :param context: step context
    :param selector: locator string for text element (or None).
    :param param2: locator string for text element (or None).
    """
    g_Context.step.ocr_regional_text_exist(context, selector, param2)


@step("ocr contain text[{selector}]")
@ele_wrap
def ocr_text_contain(context, selector=None):
    """
    The specified text element string exists in the page
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.ocr_text_contain(context, selector)


@step("ocr regional[{selector}] contain text[{param2}]")
@ele_wrap
def ocr_regional_text_contain(context, selector, param2):
    """
    The specified text element string exists in the page
    :param context: step context
    :param selector: locator string for text element (or None).
    :param param2: locator string for text element (or None).
    """
    g_Context.step.ocr_regional_text_contain(context, selector, param2)


@step("page ocr complete find text[{selector}]")
@ele_wrap
def wait_ocr_text_appear(context, selector=None):
    """
    Wait for the page to finish rendering and the selector element param1
     to appear
    :param context: step context
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.wait_ocr_text_appear(context, selector)


@step("not exist text[{selector}]")
@ele_wrap
def text_not_exist(context, selector=None):
    """
    The specified text element string does not exist in the page
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.text_not_exist(context, selector)


@step("ocr not exist text[{selector}]")
@ele_wrap
def ocr_text_not_exist(context, selector=None):
    """
    The specified text string does not exist in the page
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.ocr_text_not_exist(context, selector)


@step("text[{selector}]disappear")
@ele_wrap
def wait_text_disappear(context, selector=None):
    """
    The specified text element string disappears from the page within
     a specified period of time
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.wait_text_disappear(context, selector)


@step("exist [{p_selector}] subNode [{c_selector}] element")
@ele_wrap
def find_child_from_parent(context, p_selector=None, c_selector=None):
    """
    The specified child selector element of the specified parent selector
    element exists in the page.
    :param context: step context
    :param p_selector: locator string for parent selector element (or None).
    :param c_selector: locator string for selector child element (or None).
    """
    g_Context.step.find_child_from_parent(context, p_selector, c_selector)


@step("exist[{selector}]element")
@ele_wrap
def wait_ele_exit(context, selector=None):
    """
    The specified selector element string exists in the page
    :param context: step context
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.wait_ele_exit(context, selector)


@step("not exist element[{selector}]")
@ele_wrap
def ele_not_exit(context, selector=None):
    """
    The specified selector element string does not exists in the page
    :param context: step context
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.ele_not_exit(context, selector)


@step("element[{selector}]disappear")
@ele_wrap
def wait_ele_disappear(context, selector=None):
    """
    The specified selector element string disappears from the page within
     a specified period of time
    :param context: step context
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.wait_ele_disappear(context, selector)


@step("the text of element[{selector}]is[{param2}]")
@ele_wrap
def ele_text_equal(context, selector=None, param2=None):
    """
    Check if the value of the text of the selector element param1 is param2
    :param context: step context
    :param selector: locator string for selector element (or None).
    :param param2: expected value
    """
    g_Context.step.ele_text_equal(context, selector, param2)


@step("the text of element[{selector}]include[{param2}]")
@ele_wrap
def ele_text_container(context, selector=None, param2=None):
    """
    Check if the value of the text of the selector element param1 include param2
     :param context: step context
     :param selector: locator string for selector element (or None).
     :param param2: expected value
    """
    g_Context.step.ele_text_container(context, selector, param2)


@step("page rendering complete appears element[{selector}]")
@ele_wrap
def wait_ele_appear(context, selector=None):
    """
    Wait for the page to finish rendering and the selector element param1
     to appear
    :param context: step context
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.wait_ele_appear(context, selector)


@step("existing element[{selector}]")
@ele_wrap
def exist_ele(context, selector=None):
    """
    The specified selector element string exists in the page
    :param context: step context
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.exist_ele(context, selector)


@step("in[{p_selector}]from {param2} find[{c_selector}]element")
@ele_wrap
def swipe_to_ele(context, p_selector=None, param2=None, c_selector=None):
    """
    Within the specified selector element Slide in the specified direction
     to find the selector element
    :param context: step context
    :param p_selector: locator string for parent selector element (or None).
    :param param2: slide direction (top/bottom/left/right)
    :param c_selector: locator string for selector child element (or None).
    """
    g_Context.step.swipe_to_ele(context, p_selector, param2, c_selector)


@step("from {param1} find[{selector}]element")
@ele_wrap
def full_screen_swipe_to_ele_aaa(context, param1=None, selector=None):
    """
    Full screen swipe in the specified direction to find the specified
     selector element
     :param context: step context
    :param param1: slide direction (top/bottom/left/right)
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.full_screen_swipe_to_ele_aaa(context, param1, selector)


@step("from {param1} find[{selector}]text")
@ele_wrap
def full_screen_swipe_to_ocr_txt(context, param1=None, selector=None):
    """
    Full screen swipe in the specified direction to find the specified
     selector element
     :param context: step context
    :param param1: slide direction (top/bottom/left/right)
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.full_screen_swipe_to_ocr_txt(context, param1, selector)


@step("from {param1} find[{selector}]image")
@ele_wrap
def full_screen_swipe_to_img(context, param1=None, selector=None):
    """
    Full screen swipe in the specified direction to find the specified
     selector element
     :param context: step context
    :param param1: slide direction (top/bottom/left/right)
    :param selector: locator string for selector element (or None).
    """
    g_Context.step.full_screen_swipe_to_img(context, param1, selector)


@step("clear [{selector}] and input[{param2}]")
@ele_wrap
def ele_clear_input(context, selector=None, param2=None):
    """
    Empty the selector element param1 and enter the value param2
    :param context: step context
    :param selector: locator string for selector element (or None).
    :param param2: string to be input
    """
    g_Context.step.ele_clear_input(context, selector, param2)


@step("from [{selector}] select [{param2}]")
@ele_wrap
def ele_select(context, selector=None, param2=None):
    """
    Select the value param2 from the dropdown box element param1
    :param context: step context
    :param selector: locator string for selector element (or None).
    :param param2: text or value of select option
    """
    g_Context.step.ele_select(context, selector, param2)


@step("the text of element [{p_selector}] subNode [{c_selector}] is [{param3}]")
@ele_wrap
def find_text_from_parent(context, p_selector=None, c_selector=None, param3=None):
    """
    check the text of the child element in the parent element is param3
    :param context: step context
    :param p_selector: locator string for parent selector element (or None).
    :param c_selector: locator string for selector child element (or None).
    :param param3: expected value.
    """
    g_Context.step.find_text_from_parent(context, p_selector, c_selector, param3)


@step("exist image [{param}]")
def img_exist(context, param):
    g_Context.step.img_exist(context, param)


@step("not exist image [{param}]")
def img_not_exist(context, param):
    g_Context.step.img_not_exist(context, param)


@step("click home")
def click_home(context):
    g_Context.step.to_device_home(context)


@step("click anywhere")
def click_anywhere(context):
    g_Context.step.click_coordinates(context, 0, 0, "random_click,random_count=1")


@step("click [{param1}] {selector} [{param2}]")
@ele_wrap
def click_to_ele_with_direction(context, param1, selector, param2):
    """
    Click ele in the specified direction to find the specified
     selector element
     :param context: step context
    :param param1: locator string for search element.
    :param selector: slide direction (top/bottom/left/right)
    :param param2: target locator string for selector element.
    """
    g_Context.step.click_to_ele_with_direction(context, param1, param2, selector)


@step("click img[{param1}] {selector} img[{param2}]")
@ele_wrap
def click_to_image_with_direction(context, param1, selector, param2):
    g_Context.step.click_to_image_with_direction(context, param1, param2, selector)


@step("click ocr_text [{param1}] {selector} ocr_text[{param2}]")
@ele_wrap
def click_to_ocr_with_direction(context, param1, selector, param2):
    """
    Click on the ocr text element
    :param context: step context
    :param selector: locator string for text element (or None).
    """
    g_Context.step.ocr(context)
    g_Context.step.click_to_ocr_with_direction(context, param1, param2, selector)


@step("click img[{param1}] {selector} ocr_text[{param2}]")
@ele_wrap
def click_to_img_ocr_with_direction(context, param1, selector, param2):
    g_Context.step.ocr(context)
    g_Context.step.click_to_img_ocr_with_direction(context, param1, param2, selector)


@step("click ocr_text[{param1}] {selector} img[{param2}]")
@ele_wrap
def click_to_ocr_img_with_direction(context, param1, selector, param2):
    g_Context.step.ocr(context)
    g_Context.step.click_to_ocr_img_with_direction(context, param1, param2, selector)


@step("click img[{param1}] {selector} [{param2}]")
@ele_wrap
def click_to_img_ele_with_direction(context, param1, selector, param2):
    g_Context.step.click_to_img_ele_with_direction(context, param1, param2, selector)


@step("click poco[{param1}] {selector} img[{param2}]")
@ele_wrap
def click_to_ele_img_with_direction(context, param1, selector, param2):
    g_Context.step.click_to_ele_img_with_direction(context, param1, param2, selector)


@step("click ocr_text[{param1}] {selector} [{param2}]")
@ele_wrap
def click_to_ocr_ele_with_direction(context, param1, selector, param2):
    g_Context.step.ocr(context)
    g_Context.step.click_to_ocr_ele_with_direction(context, param1, param2, selector)


@step("click poco[{param1}] {selector} ocr_text[{param2}]")
@ele_wrap
def click_to_ele_ocr_with_direction(context, param1, selector, param2):
    g_Context.step.ocr(context)
    g_Context.step.click_to_ele_ocr_with_direction(context, param1, param2, selector)
