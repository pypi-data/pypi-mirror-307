from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from server import *
import server
import io

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=["*"])
]


async def media_handler(request):
    return await server.media_handler(request)

routes = [
    Mount('/media', app=Starlette(routes=[
        Route("/{filename:path}", endpoint=media_handler),
    ])),
]

app = Starlette(middleware=middleware, routes=routes)

def is_directory_exists(directory_path):
    return os.path.exists(directory_path) and os.path.isdir(directory_path)

# 创建一个静态文件实例
if is_directory_exists("components"):
    static_files = StaticFiles(directory='components')
    # 将静态文件实例挂载到路径上
    app.mount('/components', static_files)

#
@app.route('/hello')
async def _home(request):
    return await server.home(request)


# Serve static files
@app.route("/")
async def _static_root(request):
    return await server.send_static(request)

@app.route("/{basepath}/")
async def _static_root(request):
    return await server.send_static(request)

'''
@app.route("/{path}")
async def _send_static(request):
    return await server.send_static(request)
'''

#这个对于发布后的版本刷新 /pages/...有用
#@app.route("/pages/{path}")
@app.route("/pages/{path:path}")
async def _send_static(request):
    print("static root for /pages/...")
    return await server.send_static(request)

#支持basepath了
@app.route("/{basepath}/pages/{path:path}")
async def _send_static(request):
    print("static root for /basepath/pages/...")
    return await server.send_static(request)

@app.route("/assets/{path}")
async def _send_static_resource(request):
    return await server.send_static_resource(request)

#这里不能带子目录，否则不能映射到这里。通过ss.config["videopath"]实现真正的子目录
@app.route("/video/{filename}")
async def _serve_video(request):
    return await server.serve_video(request)

#测试
@app.route("/image/{filename}")
async def image(request):
    print("图片")
    
    image_path = request.path_params['filename']
    #hard coded for now
    image_path = "./media/images/" + image_path
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")

#动态生成各种资源
#e.g. /ss/res/db_table?file=....&table=...
#浏览器输入http://localhost:3000/ss/res/test?=1
@app.route("/ss/res/{url}")
async def resource(request):
    return await server.resource(request)

    #测试
    type = request.path_params['url']
    file_param = request.query_params.get('file')
    res = f"type:{type}, param:{request.query_params}"
    return PlainTextResponse(res)
    
    ##return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")

#end 静态文件处理， for host:8000 server

#start other handlers
@app.route("/api/init")
async def _init_system(request):
    return await server.init_system(request)

@app.route("/api/init/{pre_clientid}")
async def _init_system2(request):
    return await server.init_system(request)

@app.route("/api/page/main/{clientid}")
async def _init_main(request):   
    return await server.init_main(request)


@app.route("/api/page/more/{pagename}/{clientid}")
async def _page_init(request):      
    return await server.page_init(request)

@app.route("/api/page/more/{sub}/{pagename}/{clientid}")
async def _page_init(request):      
    return await server.page_init(request)

@app.websocket_route('/api/stream') 
async def _websocket_endpoint(websocket):   
    await server.websocket_endpoint(websocket)
    
@app.route('/upload', methods=['POST'])
async def _upload_file(request: Request):
    return await server.upload_file(request)
    
@app.on_event("startup")
async def _startup():
    '''
    host = os.environ['host']
    port = os.environ['port']
    protocol = os.environ['protocol']
    print("开机参数", host, port )
    '''
    print("start up")
    await server.startup()
    
@app.on_event("shutdown")
async def shutdown_event():
    #print("应用正在关闭...")
    await server.shutdown()
    
@app.route('/users', methods=['GET'])
async def _get_users(request):
    pass

#end others

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)