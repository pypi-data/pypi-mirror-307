from setuptools import setup, Extension, find_packages

ext_modules = [
    Extension('simplestart.server', sources=['sub1/server.c']),
    Extension('simplestart.streamsync', sources=['sub1/streamsync.c']),
]

##vercel 上build有250M的限制，制作vercel版是，install_requires暂时去除matplotlib
##vercel, render 不支持websocket， 所以不能用。放放静态资源还不错。纯粹的http webservice, fastapi, starlette也可以
#但不能涉及到websocket

setup(
    name='simplestart',
    version='0.0.1.33',
    
    install_requires=[
        'uvicorn[standard]',
        'starlette', 'pandas', 'matplotlib', 'pyyaml', 'easydict', 'itsdangerous', 'send2trash', 'python-multipart', 'watchdog'
    ],
    
    #py_modules 适用于包含单个模块的简单脚本。
    #py_modules=['module1', 'module2', 'module3'],
    
    packages=find_packages(),
    
    #packages=['simplestream','simplestream.sub2'],
    
    package_data={'simplestart': ['static/*', 'static/**/*', 'system/*', 'demo/*', 'demo/**/*']},
    
    ext_modules=ext_modules,

    entry_points={
        "console_scripts": [
            "ss = simplestart.launch:start",
            "myss = simplestart.launch:start",
            "simplestart = simplestart.launch:start"
        ]
    }
)