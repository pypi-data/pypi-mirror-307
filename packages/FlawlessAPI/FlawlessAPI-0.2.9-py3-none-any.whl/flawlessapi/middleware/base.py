class Middleware:
    """中间件基类"""
    async def process_request(self, scope, receive, send):
        """处理请求前"""
        pass
        
    async def process_response(self, scope, receive, send, response):
        """处理响应后"""
        return response