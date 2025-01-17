import json
import logging

import httpx

logger=logging.getLogger("llm_httpx_transport")

class LoggingTransport(httpx.AsyncHTTPTransport):
    # 提示： 不要读取 response body，读取了会破环状态    
    async def handle_async_request(self, request):
        """自定义传输层
            解决有些第三方 openai completion 接口不完全兼容.
            比如某平台, 对 toolcall 的格式非常严格
        """
        try:
            content = request.content.decode('utf-8')
            content_json = json.loads(content)
            
            #1: 修正 tool_calls 字段
            messages_field=content_json.get("messages", None)
            if messages_field:
                for message in messages_field:
                    content = message.get("content", None)
                    if content is None:
                        message["content"] = ""
            
            tool_calls_field=content_json.get("tools", None)
            if tool_calls_field:
                # 确保 tools 字段严格遵守 openapi 格式
                for tool_call in tool_calls_field:
                    fn = tool_call.get("function", None)
                    if fn:
                        parameters=fn.get("parameters", None)
                        if parameters:
                            properties = parameters.get("properties", None)
                            if properties:
                                action = properties.get("action", None)
                                if action:
                                    items = action.get("items", None)
                                    if items:
                                        properties = items.get("properties", None)
                                        if properties:
                                            for k, v in properties.items():
                                                # 修正缺少的 type 字段
                                                _type=v.get("type", None)
                                                if not _type:
                                                    v["type"] = "object"
                                                _any_of=v.get("anyOf", None)
                                                if _any_of:
                                                    for _any_of_item in _any_of:
                                                        _any_of_item["type"] = "object"
                                                        any_of_properties=_any_of_item.get("properties", None)
                                                        if any_of_properties:
                                                            for any_of_property_k, any_of_property_v in any_of_properties.items():
                                                                _any_of_property_type=any_of_property_v.get("type", None)
                                                                if not _any_of_property_type:
                                                                    any_of_property_v["type"] = "object"
                                        action["items"] = items
                    
                
                content_json["tool_calls"]=tool_calls_field            
            
            modified_content = json.dumps(content_json).encode('utf-8')
            new_headers = dict(request.headers)
            new_headers["content-length"] = str(len(modified_content))
            
            request = httpx.Request(
                method=request.method,
                url=request.url,
                headers=new_headers,
                content=modified_content,
            )
            
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            raise e
        response = await super().handle_async_request(request)
        

        try:
            content = request.content.decode('utf-8')
            content_json = json.loads(content)
            formatted_content = json.dumps(content_json, indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, UnicodeDecodeError):
            formatted_content = content
            
        logger.info(
            f"LLM http req: {request.url}>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
            f"{formatted_content}\n"
            f"Response {response.status_code}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n"
            # f"{formatted_response_content}\n"
            
        )
        
        return response