from flawlessapi.middleware.base import Middleware
from typing import Optional, List, Dict

class CORSMiddleware(Middleware):
    """
    CORS(跨域资源共享)中间件
    用于处理跨域请求的访问控制,包括:
    - 验证请求来源是否在允许列表中
    - 处理预检请求(OPTIONS)
    - 添加必要的CORS响应头
    """
    def __init__(
        self,
        allow_origins: List[str] = ["*"],  # 允许的源域名列表,*表示允许所有域
        allow_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 允许的HTTP方法
        allow_headers: List[str] = ["*"],  # 允许的请求头,*表示允许所有请求头
        allow_credentials: bool = True,  # 是否允许发送身份凭证(cookies等)
        expose_headers: List[str] = None,  # 允许前端访问的响应头
        max_age: int = 600  # 预检请求结果的缓存时间(秒)
    ):
        """
        初始化CORS中间件
        :param allow_origins: 允许的源域名列表
        :param allow_methods: 允许的HTTP方法列表
        :param allow_headers: 允许的请求头列表
        :param allow_credentials: 是否允许发送身份凭证
        :param expose_headers: 允许前端访问的响应头列表
        :param max_age: 预检请求结果的缓存时间
        """
        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers
        self.allow_credentials = allow_credentials
        self.expose_headers = expose_headers
        self.max_age = max_age

    async def process_request(self, scope, receive, send):
        """
        处理CORS预检请求和实际请求的CORS头
        :param scope: ASGI scope对象,包含请求信息
        :param receive: ASGI receive函数
        :param send: ASGI send函数
        :return: 如果是预检请求则返回True,否则返回None
        """
        headers = []  # 存储CORS响应头
        origin = self._get_header(scope, b'origin')  # 获取请求的源域名

        if origin:
            # 检查请求的源是否在允许列表中
            if "*" in self.allow_origins or origin.decode() in self.allow_origins:
                # 添加基本的CORS响应头
                headers.extend([
                    (b'Access-Control-Allow-Origin', origin),  # 允许的源
                    (b'Vary', b'Origin')  # 告诉缓存服务器按Origin字段区分缓存
                ])

                # 如果允许发送身份凭证,添加对应的响应头
                if self.allow_credentials:
                    headers.append(
                        (b'Access-Control-Allow-Credentials', b'true')
                    )

                # 处理OPTIONS预检请求
                if scope["method"] == "OPTIONS":
                    # 添加允许的方法和缓存时间
                    headers.extend([
                        (b'Access-Control-Allow-Methods', 
                         ", ".join(self.allow_methods).encode()),
                        (b'Access-Control-Max-Age',
                         str(self.max_age).encode())
                    ])

                    # 处理允许的请求头
                    if self.allow_headers:
                        if "*" in self.allow_headers:
                            # 如果允许所有请求头,使用请求中的Access-Control-Request-Headers值
                            requested_headers = self._get_header(
                                scope,
                                b'access-control-request-headers'
                            )
                            if requested_headers:
                                headers.append((
                                    b'Access-Control-Allow-Headers',
                                    requested_headers
                                ))
                        else:
                            # 使用配置的允许请求头列表
                            headers.append((
                                b'Access-Control-Allow-Headers',
                                ", ".join(self.allow_headers).encode()
                            ))

                    # 添加允许前端访问的响应头
                    if self.expose_headers:
                        headers.append((
                            b'Access-Control-Expose-Headers',
                            ", ".join(self.expose_headers).encode()
                        ))

                    # 对预检请求返回200响应
                    await send({
                        'type': 'http.response.start',
                        'status': 200,
                        'headers': headers
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': b''
                    })
                    return True

        # 将CORS头存储在scope中,供后续中间件和响应使用
        scope['cors_headers'] = headers

    async def process_response(self, scope, receive, send, response):
        """
        将CORS头添加到响应中
        :param scope: ASGI scope对象
        :param receive: ASGI receive函数
        :param send: ASGI send函数
        :param response: 响应对象
        :return: 添加了CORS头的响应对象
        """
        if 'cors_headers' in scope:
            # 如果response是http.response.start消息
            if isinstance(response, dict):
                headers = response.get('headers', [])
                headers.extend(scope['cors_headers'])
                response['headers'] = headers
            return response
        return response

    def _get_header(self, scope: Dict, key: bytes) -> Optional[bytes]:
        """
        从scope中获取指定的header值
        :param scope: ASGI scope对象
        :param key: header键名
        :return: header值,如果不存在则返回None
        """
        for k, v in scope.get('headers', []):
            if k == key:
                return v
        return None