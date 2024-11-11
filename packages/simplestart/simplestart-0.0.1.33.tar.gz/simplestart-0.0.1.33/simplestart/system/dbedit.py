import simplestart as ss
import pandas as pd
import random

ss.write("### Sqlite Database")
ss.write("---")

ss.session.dbfile = ""
ss.session.db = ""

tables = [""]

def sel_change(event):
    tablename = event.value
    ss.message(tablename)
    ss.session.table.data = ss.session.db.loadTable(tablename)
    mylink.visible = False


select1 = ss.selectbox(tables, label="请选择数据表格", onchange=sel_change)

def SaveCSV(event):
    if len(select1.items) == 0:
        ss.message("No data")
        return
    
    res = ss.session.db.commit()
    ss.message("已保存")

def myclose(state, value):
    ss.message("dialog close with result " + value)
    if value == "1":
        tablename = select1.value
        ss.session.db.dropTable(tablename) 
        
        #
        index = select1.items.index(tablename)
        select1.items.pop(index)        

        select1.items = select1.items
        
        if len(select1.items) > 0:
            select1.index = 0
            tablename = select1.items[0]
            ss.session.table.data = ss.session.db.loadTable(tablename)
            mylink.visible = False
        else:
            ss.session.table.data = pd.DataFrame()
            select1.value = ""

        
def DropTable():
    if len(select1.items) == 0:
        ss.message("No data")
        return
    
    dialog.show()
    
    #tablename = select1.value
    #ss.session.db.dropTable(tablename)

def onsucess(event):
    filename = event.value
    path = f'{ss.baseinfo["package_path"]}/uploads/{filename}'
    
    ss.session.db.read_csv(path)
    tables = ss.session.db.fetchTableNames()
    select1.items = tables
    
    ss.message("已加载数据")
    
def Export():
    if len(select1.items) == 0:
        ss.message("No data")
        return
    
    tablename = select1.value
    url = f"/ss/res/sqlite?file=./data/ss_data.db&table='{tablename}'" #加单引号，防止Tablename名字中有空格
    mylink.url = url
    mylink.file = tablename + ".csv"
    mylink.visible = True
    

    
dialog = ss.dialog(title="Are you sure to delete?", onclose=myclose)
    
ss.button("保存更新", onclick=SaveCSV)
ss.upload("test", onsucess = onsucess)
ss.button("删除表格", onclick=DropTable)
ss.button("导出表格", onclick = Export)

def sslink(label, url, **kwargs):
    id = "id_" + str(random.randint(100000, 999999))
    data = {"id":id, "label":label, "file":label, "visible":False}
    data["url"] = url
    
    test = "222"
    data["downloadItem"] = '''
        var url = data.url;
        axios.get(url, { responseType: 'blob' })
            .then(response => {
                const blob = new Blob([response.data], { type: 'text/csv' })
                const link = document.createElement('a')
                link.href = URL.createObjectURL(blob)
                link.download = data.file
                link.click()
                URL.revokeObjectURL(link.href)
        }).catch(console.error)
    '''
    
    visible = kwargs.get("visible", True)
    

    res = ss.template('''
    <v-btn
    :style="data.visible?'':'display:none'"
    size = "small" variant = "text" prepend-icon="mdi-arrow-down-bold" color="info"
    :href="data.url" \@click.prevent='var xxx=123;evaljs("downloadItem")'>{{data.label}}
    </v-btn>
    ''', data = data)
    return res

mylink = sslink("Download", "http://xxx.pdf", visible = False)

ss.space()


 
#没有逗号，括号被解释为普通的括号，而不是元组构造器。

def default_syncData(event):
    item = event.value
    if item["type"] == "edit":
        editedIndex = item["editedIndex"]
        editItem = item["editItem"]
        #data[editedIndex].update(item["editItem"])
        params = list(editItem.values())

        # 构建 SQL 更新语句
        # 移除 _id 键用于更新字段，它作为 where 条件
        row_id = editItem.pop('rowid')  ###ROWID是系统的，从1开始
        _id = editItem.pop("_id") ## _id是自己加的
        
        fields = ', '.join([f"{key} = ?" for key in editItem.keys()])
        table_name = select1.value
        sql = f"UPDATE {table_name} SET {fields} WHERE rowid = ?"

        # 字段值列表加上行号
        params = list(editItem.values())
        if len(params) == 1:
            params = (params[0],)
        elif len(params) == 0:
            param = None
        else:
            params = tuple(params)

        # 执行更新操作
        res = ss.session.db.execute(f"UPDATE {table_name} SET {fields} WHERE rowid = {row_id}", params)

    elif item["type"] == "del":
        editedIndex = item["editedIndex"]
        editItem = item["editItem"]

        row_id = editItem.pop('rowid')  ###ROWID是系统的，从1开始
        
        table_name = select1.value
        sql = f'DELETE FROM {table_name} WHERE rowid = ?'
        res = ss.session.db.execute(sql, (row_id,))

    elif item["type"] == "add":
        editItem = item["editItem"]
        # 从 editItem 中移除不必要的键
        editItem.pop('rowid', None)  # 移除 'rowid'，如果存在的话
        _id = editItem.pop("_id", None)  # '_id' 是自定义的，添加操作中可能不需要

        # 构建 SQL 插入语句
        table_name = select1.value
        columns = ', '.join(editItem.keys())
        placeholders = ', '.join(['?' for _ in editItem])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # 字段值列表转换为元组
        params = list(editItem.values())
        if len(params) == 1:
            params = (params[0],)
        elif len(params) == 0:
            param = None
        else:
            params = tuple(params)

        # 执行插入操作
        res = ss.session.db.execute(sql, params)
    
    
def loadDb(filepath):
    global tables
    ss.session.db = ss.sqlite("./data/ss_data.db")
    tables = ss.session.db.fetchTableNames()
    select1.items = tables
    
    if len(tables) > 0:
        select1.index = 0 
        tablename = tables[0]
        df = ss.session.db.pd_query(f"select ROWID, * from '{tablename}'") #加单引号，防止Tablename名字中有空格
        ss.session.table = ss.table(df, editable = True, handlers = {"sync_data" : default_syncData})
    else:
        ss.session.table = ss.table(data = None, editable = True, handlers = {"sync_data" : default_syncData})
            

def onPageEnter():
    if ss.session.dbfile == "":
        filepath = ss.store["codeDb"]
        if filepath == None:
            return

        loadDb(filepath)
        ss.session.dbfile = filepath

