"""示例插件 — 展示如何创建自定义操作插件"""

def register():
    """注册插件，返回插件元数据"""
    return {
        "name": "example_plugin",
        "display_name": "示例插件",
        "version": "1.0.0",
        "description": "一个示例插件，展示如何创建自定义操作",
        "category": "custom",
        "author": "AutoFlow",
        "operations": [
            {
                "id": "custom_hello",
                "name": "自定义问候",
                "description": "输出自定义问候语",
                "params": [
                    {"name": "message", "type": "string", "label": "问候消息", "default": "Hello"},
                    {"name": "name", "type": "string", "label": "姓名", "default": "World"}
                ],
                "execute": execute_custom_hello
            }
        ]
    }

def execute_custom_hello(params):
    """执行自定义问候操作"""
    message = params.get("message", "Hello")
    name = params.get("name", "World")
    print(f"{message}, {name}!")
    return True