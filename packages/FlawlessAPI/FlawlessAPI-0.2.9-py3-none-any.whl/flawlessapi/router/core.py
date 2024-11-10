import asyncio
from inspect import Parameter, signature
import json
import time
from typing import Callable, List, Optional, Dict, Any, Type, get_type_hints

import docstring_parser

from flawlessapi.cache.factory import CacheFactory
from flawlessapi.cache.redis_cache import RedisCache
from flawlessapi.circuit_breaker import CircuitBreaker
from flawlessapi.config.cache_config import CacheConfig
from flawlessapi.config.settings import APIConfig
from flawlessapi.connection_pool import ConnectionPool
from flawlessapi.database.manager import DatabaseManager
from flawlessapi.docs.auto_docs import AutoAPIEndpoint, AutoDocGenerator
from flawlessapi.docs.generator import APIDocGenerator
from flawlessapi.errors import ErrorHandler
from flawlessapi.handlers.file_upload import FileUploadHandler
from flawlessapi.handlers.websocket import WebSocketHandler
from flawlessapi.i18n.translator import I18nSupport
from flawlessapi.logger import logger
from flawlessapi.middleware.base import Middleware
from flawlessapi.middleware.rate_limit import RateLimiter
from flawlessapi.monitoring.monitoring import PerformanceMonitor, PerformanceMonitorMiddleware
from flawlessapi.monitoring.tracer import DistributedTracer, TracerMiddleware
from flawlessapi.task_queue.task_queue import TaskQueue
from flawlessapi.requests import AsyncRequest
from flawlessapi.response import ApiResponse, AsyncResponse, error_response, health_response, info_response, metrics_response, success_response, traces_response
from flawlessapi.router.decorators import Route
from flawlessapi.service.registry import ServiceRegistry
from flawlessapi.template.engine import TemplateEngine
from flawlessapi.router.patterns import TrieNode
from flawlessapi.router.cache import RouteCache
import traceback

# 主要API框架类
class FlawlessAPI:
    def __init__(self, cache_config: Optional[CacheConfig] = None, api_config: Optional[APIConfig] = None, **kwargs):
        # 基础配置初始化
        self.cache_config = cache_config or CacheConfig()  # 初始化缓存配置
        self.api_config = api_config or APIConfig()  # 初始化API配置
        self._start_time = time.time()  # 记录服务启动时间
        self.debug = False  # 调试模式开关
        # 添加路由存储
        self._routes = {}  # 存储所有注册的路由信息
        
        # 初始化核心组件
        self.cache = CacheFactory.create_cache(self.cache_config)  # 创建缓存实例
        self.root = TrieNode()  # 创建路由树根节点
        self.middleware_stack = []  # 存储中间件的列表
        self.async_response = AsyncResponse()  # 创建异步响应处理器
        self.route_cache = RouteCache(2000)  # 创建路由缓存,设置容量为2000
        self.connection_pool = ConnectionPool(1000)  # 创建连接池,设置容量为1000

        # 初始化日志管理器
        self.logger_manager = logger.LoggerManager(
            name="flawless_api",
            log_dir="logs",
            level=kwargs.get("log_level", "INFO"),
            format_json=True
        )
        self.logger = self.logger_manager.get_logger()
        self.request_logger = logger.RequestLogger(self.logger)

        # 初始化自动文档生成器
        self.auto_docs = AutoDocGenerator(
            title=self.api_config.api_title,
            version=self.api_config.api_version
        )
        
        # 初始化监控组件
        self.monitor = PerformanceMonitor()  # 创建性能监控器实例
        self.tracer = DistributedTracer()  # 创建分布式追踪器实例
        
        # 初始化错误处理器
        self.error_handler = ErrorHandler()  # 创建错误处理器实例
        
        # 初始化安全组件
        self.rate_limiter = RateLimiter(1000)  # 创建限流器,设置阈值为1000
        self.circuit_breaker = CircuitBreaker()  # 创建熔断器实例

        # 初始化性能监控中间件
        self.performance_monitor_middleware = PerformanceMonitorMiddleware(self.monitor)
        
        # 初始化分布式追踪中间件
        self.tracer_middleware = TracerMiddleware(self.tracer)
        
        # 初始化事件处理器
        self._event_handlers = {
            "startup": [],  # 存储启动事件的处理函数列表
            "shutdown": []  # 存储关闭事件的处理函数列表
        }
        
        # 初始化Redis缓存
        self.redis_cache = RedisCache()  # 创建Redis缓存实例
        
        # 添加默认中间件
        self._init_default_middlewares()  # 初始化默认的中间件
        
        # 注册内置路由
        if self.api_config.enable_builtin_routes:  # 如果启用了内置路由
            self._register_builtin_routes()  # 注册内置的路由
            

        # 添加新组件的初始化
        self.template_engine = None
        self.file_handler = None
        self.websocket_handler = None
        self.static_handler = None
        self.db_manager = None
        self.i18n = None
        self.task_queue = None
        self.service_registry = None
        self.api_docs = None
        
        # 初始化新组件
        self._init_components()
        
    def _init_components(self):
        """初始化所有组件"""
        # 初始化模板引擎
        if self.api_config.enable_templates:
            self.template_engine = TemplateEngine(
                template_dir=self.api_config.template_dir,
                cache_size=self.api_config.template_cache_size
            )
            
        # 初始化文件上传处理器
        if self.api_config.enable_file_uploads:
            self.file_handler = FileUploadHandler(
                upload_path=self.api_config.upload_dir,
                max_size=self.api_config.max_upload_size
            )
            
        # 初始化WebSocket处理器
        if self.api_config.enable_websocket:
            self.websocket_handler = WebSocketHandler()
            
        # 初始化数据库管理器
        if self.api_config.database_url:
            self.db_manager = DatabaseManager(
                url=self.api_config.database_url
            )
            
        # 初始化国际化支持
        if self.api_config.enable_i18n:
            self.i18n = I18nSupport(
                locale_dir=self.api_config.locale_dir,
                default_locale=self.api_config.default_locale
            )
            
        # 初始化任务队列
        if self.api_config.enable_task_queue:
            self.task_queue = TaskQueue(
                max_workers=self.api_config.task_queue_workers
            )
            
        # 初始化服务注册
        if self.api_config.enable_service_registry:
            self.service_registry = ServiceRegistry(
                registry_url=self.api_config.registry_url,
                service_name=self.api_config.service_name,
                service_url=self.api_config.service_url
            )
            
        # 初始化API文档
        if self.api_config.enable_api_docs:
            self.api_docs = APIDocGenerator(
                title=self.api_config.api_title,
                version=self.api_config.api_version
            )
    
    # 初始化默认中间件
    def _init_default_middlewares(self):
        """
        初始化并配置默认的中间件栈
        按照重要性和执行顺序对中间件进行排序和组织
        """
        # 关键中间件(优先级最高)
        critical_middlewares = [
            self.circuit_breaker,  # 熔断器中间件,用于故障隔离
            self.rate_limiter  # 限流器中间件,用于流量控制
        ]
        
        # 监控类中间件
        monitoring_middlewares = [
            self.performance_monitor_middleware,  # 使用新的性能监控中间件
            self.tracer_middleware  # 分布式追踪中间件
        ]
        
        # 组合所有中间件
        self.middleware_stack = critical_middlewares + monitoring_middlewares
        
    # 处理中间件链
    async def process_middlewares(self, scope, receive, send):
        """
        处理整个中间件链的执行流程
        :param scope: ASGI作用域
        :param receive: 接收消息的异步函数
        :param send: 发送消息的异步函数
        :return: 中间件链执行的结果
        """
        try:
            middleware_chain = self._compile_middleware_chain()
            await middleware_chain(scope, receive, send)
        except Exception as e:
            self.logger.error(f"Error processing middlewares: {traceback.format_exc()}")
            await self._handle_system_error(e, send)
        
    # 事件处理装饰器
    def on_event(self, event_type: str):
        """
        用于注册事件处理函数的装饰器
        :param event_type: 事件类型,可以是 "startup" 或 "shutdown"
        :return: 装饰器函数
        """
        def decorator(func):
            # 验证事件类型是否有效
            if event_type not in self._event_handlers:
                raise ValueError(f"不支持的事件类型: {event_type}")
            # 将处理函数添加到对应的事件列表中
            self._event_handlers[event_type].append(func)
            return func
        return decorator

    # 运行事件处理器
    async def _run_event_handlers(self, event_type: str):
        """
        执行指定类型的所有事件处理器
        :param event_type: 要执行的事件类型
        """
        # 遍历并执行该类型的所有处理器
        for handler in self._event_handlers.get(event_type, []):
            await handler()

    def route(self, path: str, methods: List[str] = None, tags: List[str] = None):
        """路由装饰器工厂方法"""
        return Route(path, methods, tags)

    # 应用启动处理
    async def startup(self):
        """
        应用启动时的初始化流程
        执行所有必要的启动任务
        """
        # 初始化各种缓存系统
        await self.route_cache.start()  # 启动路由缓存
        await self.redis_cache.connect()  # 连接Redis缓存
        
        # 初始化HTTP连接池
        await self.connection_pool.create_http_pool('default')  # 创建默认连接池
        await self.connection_pool.warmup('default', 10)  # 预热连接池
        
        # 启动性能监控
        asyncio.create_task(self.monitor.start_collection())  # 异步启动数据收集
        
        # 执行用户定义的启动处理器
        await self._run_event_handlers("startup")

        # 启动新组件
        if self.db_manager:
            await self.db_manager.connect()

        if self.task_queue:
            await self.task_queue.start()
            
        if self.service_registry:
            await self.service_registry.start()
        
    # 应用关闭处理
    async def shutdown(self):
        """
        应用关闭时的清理流程
        确保所有资源被正确释放
        """
        await self.connection_pool.close()  # 关闭连接池
        await self.redis_cache.close()  # 关闭Redis连接
        await self._run_event_handlers("shutdown")  # 执行关闭事件处理器

        # 关闭新组件
        if self.db_manager:
            await self.db_manager.disconnect()
            
        if self.task_queue:
            await self.task_queue.stop()
            
        if self.service_registry:
            await self.service_registry.stop()

    # 获取性能指标
    async def get_metrics(self):
        """
        获取系统各项性能指标
        :return: 包含监控数据、缓存状态和路由模式统计的字典
        """
        return {
            'monitor': await self.monitor.get_stats(),  # 获取监控统计数据
            'cache': await self.route_cache.get_stats(),  # 获取路由缓存统计
            'route_patterns': await self.route_cache.get_pattern_stats()  # 获取路由模式统计
        }
    
    # 处理请求(带缓存)
    async def _handle_request(self, request):
        """
        处理HTTP请求,使用Redis缓存优化响应速度
        :param request: HTTP请求对象
        :return: HTTP响应对象
        """
        # 根据请求路径和方法生成缓存键
        cache_key = f"route:{request.path}:{request.method}"
        
        # 尝试从Redis缓存获取已缓存的响应
        cached_response = await self.redis_cache.get(cache_key)
        if cached_response:
            return cached_response  # 如果存在缓存则直接返回
            
        # 无缓存时调用父类方法处理请求
        response = await super()._handle_request(request)
        
        # 将新的响应结果存入Redis缓存
        await self.redis_cache.set(cache_key, response)
        return response

    # ASGI生命周期处理
    async def __call__(self, scope, receive, send):
        """
        ASGI应用入口点,处理生命周期事件和HTTP请求
        :param scope: ASGI作用域信息
        :param receive: 接收消息的异步函数
        :param send: 发送消息的异步函数
        """
        if scope["type"] == "lifespan":
            # 处理应用生命周期事件
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    # 处理启动事件
                    await self._run_event_handlers("startup")
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    # 处理关闭事件
                    await self._run_event_handlers("shutdown")
                    await send({"type": "lifespan.shutdown.complete"})
                    break
        else:
            # 处理HTTP请求
            assert scope["type"] == "http"
            if not hasattr(self, '_startup_complete'):
                await self.startup()  # 执行启动流程
                self._startup_complete = True  # 标记启动完成
            await self.process_middlewares(scope, receive, send)
        
    # 添加路由
    def add_route(self, path: str, handler: Callable, methods: List[str] = None, tags: List[str] = None):
        """
        向路由树中添加新的路由并自动生成API文档
        """
        # 获取路由元数据
        route_info = getattr(handler, '_route_info', None)
        if route_info:
            path = route_info["path"]
            methods = route_info["methods"]
            tags = route_info["tags"]
            parameters = route_info["parameters"]
        else:
            parameters = []
            
        methods = methods or ["GET"]
        
        # 存储路由信息
        self._routes[path] = (handler, methods, tags)
        
        # 1. 添加路由到路由树
        current = self.root
        parts = path.lstrip('/').split('/')
        
        for part in parts:
            if part.startswith('{') and part.endswith('}'): 
                param_name = part[1:-1]
                if '*' not in current.children:
                    current.children['*'] = TrieNode()
                current = current.children['*']
                current.param_name = param_name
                current.is_wildcard = True
            else:
                if part not in current.children:
                    current.children[part] = TrieNode()
                current = current.children[part]
                
        current.handler = handler
        current.methods = methods
        current.is_endpoint = True

        # 2. 自动生成API文档
        try:
            # 获取函数签名
            sig = signature(handler)
            # 获取类型注解
            type_hints = get_type_hints(handler) or {}
            # 解析docstring
            docstring = docstring_parser.parse(handler.__doc__ or "")
            
            # 提取参数信息
            parameters = []
            request_body = None
            
            for param_name, param in sig.parameters.items():
                if param_name == "request":
                    continue
                param_type = type_hints.get(param_name)
                if param_type:
                    if hasattr(param_type, '__pydantic_model__'):  # 检查是否为Pydantic模型
                        # Pydantic模型作为请求体
                        request_body = {
                            "content": {
                                "application/json": {
                                    "schema": param_type.schema()
                                }
                            },
                            "required": True,
                            "description": self._get_param_description(docstring, param_name) or f"{param_name} request body"
                        }
                    # 检查路径中是否包含参数名
                    elif '{' + param_name + '}' in path:  # 路径参数
                        param_schema = self._get_parameter_schema(param_type)
                        parameters.append({
                            "name": param_name,
                            "in": "path",
                            "required": True,
                            "schema": param_schema,
                            "description": self._get_param_description(docstring, param_name) or f"{param_name} parameter"
                        })
                    else:
                        # 其他参数默认作为请求体的一部分
                        if not request_body:
                            request_body = {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {}
                                        }
                                    }
                                },
                                "required": True
                            }
                        request_body["content"]["application/json"]["schema"]["properties"][param_name] = self._get_parameter_schema(param_type)
            
            # 提取响应信息
            return_type = type_hints.get("return", Any)
            responses = self._get_response_schema(return_type, docstring)
            
            # 创建API端点文档
            endpoint = AutoAPIEndpoint(
                path=path,
                method=methods[0],  # 主要方法
                summary=docstring.short_description or handler.__name__,
                description=docstring.long_description or f"Handler for {path}",
                parameters=parameters or None,  # 如果为空列表则设为None
                request_body=request_body,
                responses=responses,
                tags=tags or ["default"]  # 提供默认标签
            )
            
            # 添加到文档生成器
            self.auto_docs.add_endpoint(endpoint)
            
        except Exception as e:
            # 记录更详细的错误信息
            self.logger.error(f"Error adding route: {traceback.format_exc()}")

    def _get_parameter_schema(self, param_type: Type) -> Dict:
        """获取参数的JSON Schema"""
        # 基本类型映射
        type_map = {
            str: {"type": "string"},
            int: {"type": "integer"},
            float: {"type": "number"},
            bool: {"type": "boolean"},
            list: {"type": "array"},
            dict: {"type": "object"},
            Any: {"type": "object"}
        }
        
        # 处理基本类型
        if param_type in type_map:
            return type_map[param_type]
            
        # 处理泛型类型
        origin = getattr(param_type, "__origin__", None)
        if origin is not None:
            if origin == list or origin == List:
                args = getattr(param_type, "__args__", [Any])
                return {
                    "type": "array",
                    "items": self._get_parameter_schema(args[0])
                }
            elif origin == dict or origin == Dict:
                args = getattr(param_type, "__args__", [str, Any])
                return {
                    "type": "object",
                    "additionalProperties": self._get_parameter_schema(args[1])
                }
                
        # 处理枚举类型
        if hasattr(param_type, "__members__"):
            return {
                "type": "string",
                "enum": list(param_type.__members__.keys())
            }
            
        # 处理Pydantic模型
        if hasattr(param_type, "schema"):
            return param_type.schema()
            
        # 默认返回object类型
        return {"type": "object"}

    def _get_response_schema(self, return_type: Type, docstring) -> Dict:
        """获取响应的JSON Schema"""
        schema = {
            "200": {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "schema": self._get_parameter_schema(return_type)
                    }
                }
            },
            "400": {
                "description": "Bad Request",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "integer"},
                                "message": {"type": "string"},
                                "timestamp": {"type": "number"}
                            }
                        }
                    }
                }
            },
            "500": {
                "description": "Internal Server Error",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "integer"},
                                "message": {"type": "string"},
                                "timestamp": {"type": "number"}
                            }
                        }
                    }
                }
            }
        }
        
        # 修改这部分代码，处理单个returns对象
        if docstring and docstring.returns:
            # docstring.returns可能是单个对象而不是列表
            return_doc = docstring.returns
            if hasattr(return_doc, 'type_name') and str(return_doc.type_name).isdigit():
                schema[str(return_doc.type_name)] = {
                    "description": return_doc.description or "No description"
                }
                
        return schema

    def _get_param_description(self, docstring, param_name: str) -> Optional[str]:
        """从docstring中获取参数描述"""
        for param in docstring.params:
            if param.arg_name == param_name:
                return param.description
        return None

    # 获取路由模式
    def _get_route_pattern(self, path: str) -> str:
        """
        将URL路径转换为路由模式
        :param path: URL路径
        :return: 标准化的路由模式
        """
        parts = []
        for part in path.split('/'):
            if not part:
                continue
            # 将参数部分替换为通配符
            if part.startswith('{') and part.endswith('}'):
                parts.append('*')
            else:
                parts.append(part)
        return '/'.join(parts)  # 拼接路由模式

    # 查找路由
    async def find_route(self, path: str) -> tuple[Optional[Callable], Optional[List[str]], dict]:
        """
        根据请求路径查找对应的路由处理函数
        :param path: 请求路径
        :return: 返回一个元组,包含(处理函数,HTTP方法列表,路径参数字典)
        """
        # 尝试从缓存获取路由,提高查找效率
        cache_key = f"route:{path}"
        cached_route = await self.route_cache.get(cache_key)
        if cached_route:
            return cached_route
        
        current = self.root  # 从根节点开始查找
        params = {}  # 存储路径参数
        path_parts = path.lstrip('/').split('/')  # 分割路径
        
        for part in path_parts:
            if not part:
                continue
                
            # 优先检查是否有精确匹配的节点
            if part in current.children:
                current = current.children[part]
            # 如果没有精确匹配,检查是否有通配符节点
            elif '*' in current.children:
                current = current.children['*']
                if current.param_name:  # 如果是参数节点,保存参数值
                    params[current.param_name] = part
            else:
                return None, None, {}  # 未找到匹配的路由
        
        # 如果找到终点节点,缓存并返回结果
        if current.is_endpoint:
            result = (current.handler, current.methods, params)
            await self.route_cache.set(cache_key, result)
            return result
            
        return None, None, {}  # 未找到匹配的路由

    # 查找静态路由
    def _find_static_route(self, path: str) -> tuple[Optional[Callable], Optional[List[str]]]:
        """
        查找静态路由(不包含动态参数的路由)
        :param path: 请求路径
        :return: 返回一个元组,包含(处理函数,HTTP方法列表)
        """
        current = self.root  # 从根节点开始查找
        path_parts = path.split('/')  # 分割路径
        
        for part in path_parts:
            if not part:
                continue
            if part not in current.children:
                return None, None  # 未找到匹配的静态路由
            current = current.children[part]
            
        if current.is_endpoint:
            return current.handler, current.methods
            
        return None, None

    # 添加中间件
    def add_middleware(self, middleware_class, **options):
        """
        添加中间件到中间件栈
        :param middleware: 中间件函数
        """
        if not issubclass(middleware_class, Middleware):
            raise TypeError("Middleware must inherit from Middleware base class")
            
        middleware = middleware_class(**options)
        self.middleware_stack.append(middleware)
        self._compiled_chain = None  # 清除已编译的中间件缓存

    # 处理请求
    async def handle_request(self, scope, receive, send):
        """
        处理ASGI请求
        :param scope: ASGI scope对象
        :param receive: ASGI receive函数
        :param send: ASGI send函数
        """
        try:
            request_path = scope['path']
            request_method = scope['method']
            
            # 查找匹配的路由
            handler, methods, params = await self.find_route(request_path)
            
            if not handler or request_method not in methods:
                scope['status_code'] = 404
                await self.async_response.send_not_found_response(send, scope)
                return
                
            # 创建请求对象
            request = AsyncRequest(scope, receive, send)
            request.path_params = params
            
            # 获取处理函数的参数签名
            sig = signature(handler)
            handler_kwargs = {}
            
            # 修改这里的参数处理逻辑
            for param_name, param in sig.parameters.items():
                if param_name == 'request':
                    handler_kwargs['request'] = request
                elif param_name in params:  # 路径参数
                    # 转换参数类型
                    param_type = param.annotation if param.annotation != Parameter.empty else str
                    try:
                        handler_kwargs[param_name] = param_type(params[param_name])
                    except ValueError:
                        handler_kwargs[param_name] = params[param_name]
                else:  # 请求体参数
                    if request_method in ['POST', 'PUT', 'PATCH']:
                        body = await request.json()
                        if (hasattr(param.annotation, '__pydantic_model__') or  
                            str(type(param.annotation)).startswith("<class 'pydantic")):
                            try:
                                # 检查是否有嵌套的数据结构
                                if param_name in body:
                                    data = body[param_name]
                                else:
                                    data = body
                                # 创建 Pydantic 模型实例
                                handler_kwargs[param_name] = param.annotation(**data)
                            except Exception as e:
                                raise ValueError(f"Invalid request data: {str(e)}")
                        else:
                            handler_kwargs[param_name] = body.get(param_name)

            try:
                response = await handler(**handler_kwargs)
                scope['status_code'] = 200
                await self._send_response(response, send, scope)
            except Exception as e:
                scope['status_code'] = 500
                self.logger.error(f"Error processing route: {traceback.format_exc()}")
                error_response = await self.error_handler.handle(e)
                await self.async_response.send_json_response(send, error_response['code'], error_response, scope)
                
        except Exception as e:
            self.logger.error(f"Error processing route: {traceback.format_exc()}")
            scope['status_code'] = 500
            error_response = await self.error_handler.handle(e)
            await self.async_response.send_json_response(send, error_response['code'], error_response, scope)

    async def json(self):
        """获取JSON格式的请求体数据"""
        if not hasattr(self, '_json'):
            body = await self.body()
            content_type = dict(self.headers).get(b'content-type', b'').decode()
            
            if body and 'application/json' in content_type:
                try:
                    self._json = json.loads(body.decode())
                except json.JSONDecodeError:
                    self._json = {}
            else:
                self._json = {}
                
        return self._json

    async def _handle_system_error(self, error: Exception, send) -> None:
        """处理系统级错误"""
        try:
            # 1. 先发送错误响应头
            await send({
                'type': 'http.response.start',
                'status': 500,
                'headers': [
                    (b'content-type', b'application/json; charset=utf-8')
                ]
            })

            # 2. 构造错误响应数据
            error_data = {
                "error_type": error.__class__.__name__,
                "details": str(error)
            }
            
            # 3. 发送错误响应体
            await send({
                'type': 'http.response.body',
                'body': json.dumps(error_data).encode('utf-8'),
                'more_body': False
            })

        except Exception as e:
            # 如果发送错误响应时出错,记录日志但不再尝试发送
            self.logger.error(f"Error sending error response: {str(e)}\nOriginal error: {str(error)}")
            try:
                # 尝试发送一个简单的错误响应
                await send({
                    'type': 'http.response.start',
                    'status': 500,
                    'headers': [(b'content-type', b'text/plain')]
                })
                await send({
                    'type': 'http.response.body',
                    'body': b'Internal Server Error',
                    'more_body': False
                })
            except:
                # 如果还是失败,放弃发送响应
                pass

    # 发送响应
    async def _send_response(self, response, send, scope: dict) -> None:
        """
        发送响应数据
        :param response: 响应数据
        :param send: ASGI send函数
        """
        if isinstance(response, dict) and "headers" in response and "body" in response:
            # 直接发送原始响应（用于HTML等特殊内容）
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": response["headers"]
            })
            await send({
                "type": "http.response.body",
                "body": response["body"].encode('utf-8')
            })
        elif isinstance(response, ApiResponse):
            # 处理ApiResponse类型
            await self.async_response.send_json_response(
                send, 
                response.code,
                response,
                scope
            )
        elif isinstance(response, dict):
            # 标准JSON响应
            code = response.get('code', 200)
            await self.async_response.send_json_response(send, code, response, scope)
        else:
            # 其他类型响应
            await self.async_response.send_json_response(
                send,
                200,
                response,
                scope
            )

    # 注册内置路由
    def _register_builtin_routes(self):
        """注册框架内置的路由"""
        # 添加标签,便于文档分类
        system_tags = ["system"]
        
        # 性能指标路由
        self.add_route("/_metrics", self._handle_metrics, ["GET"], tags=system_tags)
        # 追踪信息路由
        self.add_route("/_traces", self._handle_traces, ["GET"], tags=system_tags)
        # 健康检查路由
        self.add_route("/_health", self._handle_health, ["GET"], tags=system_tags)
        # 系统信息路由
        self.add_route("/_info", self._handle_info, ["GET"], tags=system_tags)

        # API文档路由
        self.add_route("/docs", self.auto_docs.generate_swagger_ui, ["GET"])
        self.add_route("/api/docs/spec", self.auto_docs.generate_openapi_spec, ["GET"])

        
    # 处理性能指标请求
    async def _handle_metrics(self, request: AsyncRequest) -> Dict[str, Any]:
        """
        获取系统性能指标
        
        Returns:
            dict: 包含系统性能指标的响应
                - msg: 响应消息
                - code: 状态码
                - data: 性能指标数据
        """
        metrics_data = await self.get_metrics()
        return await metrics_response(data=metrics_data)
        
    # 处理追踪信息请求
    async def _handle_traces(self, request: AsyncRequest) -> Dict[str, Any]:
        """
        获取系统追踪信息
        
        Returns:
            dict: 包含追踪信息的响应
                - msg: 响应消息
                - code: 状态码
                - data: 追踪数据列表
        """
        traces_data = [
            {
                "trace_id": span.trace_id,
                "name": span.name,
                "duration": span.end_time - span.start_time if span.end_time else None,
                "tags": span.tags,
                "start_time": span.start_time,
                "end_time": span.end_time
            }
            for span in self.tracer.get_traces()
        ]
        return await traces_response(data=traces_data)
        
    # 处理健康检查请求
    async def _handle_health(self, request: AsyncRequest) -> Dict[str, Any]:
        """
        获取系统健康状态
        
        Returns:
            dict: 包含健康状态信息的响应
                - msg: 响应消息
                - code: 状态码
                - data: 健康状态数据
        """
        health_data = {
            "status": "healthy",
            "timestamp": time.time(),
            "version": getattr(self, 'version', '1.0.0'),
            "uptime": time.time() - self._start_time
        }
        return await health_response(data=health_data)
    
    def get_routes(self) -> List[Dict[str, Any]]:
        """
        获取所有注册的路由信息
        
        Returns:
            List[Dict]: 路由信息列表
        """
        routes = []
        for path, (handler, methods, tags) in self._routes.items():
            routes.append({
                "path": path,
                "methods": methods,
                "tags": tags or [],
                "handler": handler.__name__ if hasattr(handler, '__name__') else str(handler)
            })
        return routes
        
    # 处理系统信息请求
    async def _handle_info(self, request: AsyncRequest) -> Dict[str, Any]:
        """
        获取系统配置信息
        
        Returns:
            dict: 包含系统配置的响应
                - msg: 响应消息
                - code: 状态码
                - data: 系统配置数据
        """
        # 获取路由信息
        routes_info = [
            {
                "path": path,
                "methods": methods,
                "handler": handler.__name__ if hasattr(handler, '__name__') else str(handler)
            }
            for path, (handler, methods, _) in self._routes.items()
        ]
        
        info_data = {
            "routes": routes_info,
            "middleware_count": len(self.middleware_stack),
            "debug_mode": self.debug,
            "cache_config": {
                "type": getattr(self.cache_config, 'type', 'unknown'),
                "capacity": getattr(self.cache_config, 'capacity', 0),
                "ttl": getattr(self.cache_config, 'ttl', 0)
            },
            "api_config": {
                "title": self.api_config.api_title,
                "version": self.api_config.api_version,
                "enable_docs": self.api_config.enable_api_docs
            },
            "uptime": time.time() - self._start_time,
            "components": {
                "websocket": self.websocket_handler is not None,
                "database": self.db_manager is not None,
                "task_queue": self.task_queue is not None,
                "service_registry": self.service_registry is not None
            }
        }
        return await info_response(data=info_data)
    
    # 处理中间件错误
    async def _handle_middleware_error(self, error: Exception, send, scope: dict) -> None:
        """
        处理中间件执行过程中的错误
        :param error: 异常对象
        :param send: ASGI send函数
        :param scope: 请求上下文
        """
        error_info = {
            "code": getattr(error, "status_code", 500),
            "message": str(error),
        }
        
        try:
            error_resp = await error_response(**error_info)
            await self.async_response.send_json_response(
                send,
                error_resp.code,
                await error_resp.dict(),
                scope
            )
        except Exception as e:
            self.logger.error(f"Error sending middleware error response: {traceback.format_exc()}")
            
            # 如果错误处理失败,发送简单的错误消息
            await self.async_response._send_response(
                send,
                500,
                str(error).encode("utf-8"),
                [(b"content-type", b"text/plain")]
            )

    # 处理中间件
    async def process_middlewares(self, scope, receive, send):
        """
        处理中间件执行流程
        :param scope: ASGI scope对象,包含请求信息
        :param receive: ASGI receive函数,用于接收消息
        :param send: ASGI send函数,用于发送响应
        """
        try:
            # 使用更高效的中间件链式调用
            middleware_chain = self._compile_middleware_chain()
            await middleware_chain(scope, receive, send)
        except Exception as e:
            self.logger.error(f"Error processing middlewares: {traceback.format_exc()}")
            # 发生异常时进行错误处理
            await self._handle_system_error(e, send)

    # 编译中间件链
    def _compile_middleware_chain(self):
        """
        编译并缓存中间件调用链
        :return: 编译后的中间件链函数
        """

        async def middleware_chain(scope, receive, send):
            # 创建一个新的send函数来捕获响应
            response = None
            original_send = send
            
            async def send_wrapper(message):
                nonlocal response
                if message["type"] == "http.response.start":
                    response = message
                await original_send(message)
                
            try:
                # 1. 执行请求前的中间件
                for middleware in self.middleware_stack:
                    try:
                        await middleware.process_request(scope, receive, send_wrapper)
                    except Exception as e:
                        self.logger.error(f"中间件{middleware}执行失败: {traceback.format_exc()}")
                        return await self._handle_middleware_error(e, send)

                # 2. 处理主要请求
                await self.handle_request(scope, receive, send_wrapper)

                # 3. 执行响应后的中间件(反向顺序)
                for middleware in reversed(self.middleware_stack):
                    try:
                        if response:
                            response = await middleware.process_response(
                                scope, receive, send_wrapper, response
                            )
                    except Exception as e:
                        self.logger.error(f"中间件{middleware}执行失败: {traceback.format_exc()}")
                        return await self._handle_middleware_error(e, send)

            except Exception as e:
                self.logger.error(f"Error processing middlewares: {traceback.format_exc()}")
                return await self._handle_system_error(e, send)

        # 缓存编译后的调用链
        self._compiled_chain = middleware_chain
        return middleware_chain

