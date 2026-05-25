# 角色定位
您是一位python语言高级研发工程师，擅长使用python语言编写各种程序。

# 任务描述
写一个将一个或多个pdf文件逐页转换成png格式图片的fastapi web service
## 输入参数
- 图片dpi分辨率,默认为300
- 输入pdf文件路径
## 输出结果
[
    {
    "file_name": "xxx.pdf", -- 文件名
    "status": "success" | "error", -- 状态
    "message": "xxx", -- 错误信息
    "png_file_path": ["xxx_01.png", "xxx_02.png", ...] -- 输出png图片文件路径    
    },
    {
    "file_name": "xxxx.pdf", -- 文件名
    "status": "success" | "error", -- 状态
    "message": "xxx", -- 错误信息
    "png_file_path": ["xxxx_01.png", "xxxx_02.png", ...] -- 输出png图片文件路径    
    },
]
## 其它要求
- 转换过程中首先为每个PDF按照文件名（无后缀）创建一个目录，所有生成的png图片都保存在这个目录下。例如，如果输入的pdf文件名为test.pdf，则生成的png图片文件路径为test/test_01.png，test/test_02.png，...