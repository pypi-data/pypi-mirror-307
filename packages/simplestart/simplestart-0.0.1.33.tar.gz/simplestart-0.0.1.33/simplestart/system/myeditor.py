'''
这可能是一个比较大的文件，代码编辑器。尽量写小点，控制在500行内
'''
import simplestart as ss


def onsaved(event):
    print("xyz保存", event.value)
    filepath = ss.store["codePage"]
    file_path = f"./pages/{filepath}.py"  # 文件路径
    
    if filepath == "AppMainPage":
        file_path = f"./{ss.config.appmainfile}.py"
        
    with open(file_path, 'w') as file:
        file.write(event.value) # 向文件写入内容

def preview(event):
    data = {"apiname":"page_preview"}
    ss.send_message("system_api", data)


def save():
    myeditor.save()
    

#ui
ss.button("Save", onclick=save)
ss.button("Preview", onclick = preview)
ss.space()

style = 'border:1px solid lightgray;'
myeditor = ss.editor(handlers = {"saved":onsaved}, style=style)


def onPageEnter():
    filepath = ss.store["codePage"]
    if filepath == None:
        return

    file_path = f"./pages/{filepath}.py"  # 文件路径
    if filepath == "AppMainPage":
        file_path = f"./{ss.config.appmainfile}.py"
        
    with open(file_path, 'r') as file:
        file_content = file.read()
        myeditor.loadText(file_content)
        
def event_handle():
    ss.message(333)