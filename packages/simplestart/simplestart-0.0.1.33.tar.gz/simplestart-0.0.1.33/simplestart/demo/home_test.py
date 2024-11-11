import streamsync as ss
import time

g_count = 1

#y = 1x
ss.text("一些重要功能的测试")

ss.text("1. 按钮@counter测试")
ss.markdown("---")
def click1(state, value=None):
    ss.message("hi, you clicked")
    ss.button("新增", onclick=temp)

def temp():
    ss.message("demo_a01")
    ss.openpage("demo_a01")

ss.button("click1", onclick=click1)
'''
ss.text("2. 按钮改变值")
ss.markdown("---")
txt = ss.text("text")
def click2(state, value=None):
    txt.text = txt.text + "!"
    
ss.button("click2", onclick=click2)

ss.text("3. section测试")
ss.markdown("---")

with ss.section():
    ss.text("this is a section")

ss.text("4. 系统sidebar测试")
ss.markdown("---")
ss.text("这里不会出现，将出现在左侧的sidebar上")

'''
with ss.sidebar:
    ss.text("text in sidebar")
'''

ss.text("5. 按钮改变文本值 @counter")
ss.markdown("---")

ss.init_state({
    "counter": 1112
})

def testme(state, value=None):
    state["counter"] = state["counter"] + 1
  
ss.button("click", "danger", onclick=testme)

ss.text("6. onload")
ss.markdown("---")

def onloadx():
    global g_count
    ss.message("你执行了onload")
    g_count = 0
    #with ss.sidebar:
    #    ss.text("onload in sidebar@counter")
        
        
ss.text("7. 打开新的页面")
ss.markdown("---")

def openpage(path):
    ###ss.openpage("learn_单词")
    ss.session_state.path = path
    ss.cp = "second_demo_section"
    ss.openpage("demo_section", "section test")
  
ss.button("open1", "danger", onclick=(openpage, "path1"))
ss.button("open2", "danger", onclick=(openpage, "path2"))
'''