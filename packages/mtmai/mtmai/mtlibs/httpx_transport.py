import json
import logging

import httpx

logger=logging.getLogger("llm_httpx_transport")

class LoggingTransport(httpx.HTTPTransport):
    async def handle_request(self, request):
        """Handle a request by sending it using the underlying transport."""
        try:
            content = request.content.decode('utf-8')
            content_json = json.loads(content)
            
            # Fix messages with None content
            messages_field = content_json.get("messages", None)
            if messages_field:
                for message in messages_field:
                    content = message.get("content", None) 
                    if content is None:
                        message["content"] = ""
                        
            # Fix tools format
            tool_calls_field = content_json.get("tools", None)
            if tool_calls_field:
                for tool_call in tool_calls_field:
                    fn = tool_call.get("function", None)
                    if fn:
                        parameters = fn.get("parameters", None)
                        if parameters:
                            parameters["type"] = "object"
                            properties = parameters.get("properties", None)
                            if properties:
                                action = properties.get("action", None)
                                if action:
                                    items = action.get("items", None)
                                    if items:
                                        properties = items.get("properties", None)
                                        if properties:
                                            new_properties = {}
                                            for k, v in list(properties.items()):
                                                if k == "search_google":
                                                    if "type" in v:
                                                        del v["type"]
                                                    new_properties[k] = v
                                            items["properties"] = new_properties

            # Update request content
            request.content = json.dumps(content_json).encode('utf-8')
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            
        return await super().handle_request(request)
    # 提示： 不要读取 response body，读取了会破环状态    
    async def handle_async_request(self, request):
        """自定义传输层
            解决有些第三方 openai completion 接口不完全兼容.
            比如某平台, 对 toolcall 的格式非常严格
        """
        try:
            content = request.content.decode('utf-8')
            content_json = json.loads(content)
            
            #1: 消息中 content None 的情况,应该用 空字符串替代
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
                            parameters["type"] = "object"
                            properties = parameters.get("properties", None)
                            if properties:
                                action = properties.get("action", None)
                                if action:
                                    items = action.get("items", None)
                                    if items:
                                        properties = items.get("properties", None)
                                        if properties:
                                            # 创建要保留的新属性字典
                                            new_properties = {}
                                            for k, v in list(properties.items()):
                                                # 只保留 search_google
                                                if k == "search_google":
                                                    # 修正缺少的 type 字段
                                                    # if "type" not in v:
                                                    #     v["type"] = "object"
                                                    # new_properties[k] = v
                                                    # 移除外层的 type: object
                                                    if "type" in v:
                                                        del v["type"]
                                                    # 将 anyOf 中的 null 类型改为使用 nullable
                                                    if "anyOf" in v:
                                                        # 只保留第一个非 null 的定义
                                                        non_null_schemas = [schema for schema in v["anyOf"] if schema.get("type") != "null"]
                                                        if non_null_schemas:
                                                            v = non_null_schemas[0]
                                                            v["nullable"] = True
                                                    new_properties[k] = v
                                            # 用新的属性字典替换原来的
                                            items["properties"] = new_properties            
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
        
        
        try:
            response = await super().handle_async_request(request)
            
            

            try:
                content = request.content.decode('utf-8')
                content_json = json.loads(content)
                formatted_content = json.dumps(content_json, indent=2, ensure_ascii=False)
            except (json.JSONDecodeError, UnicodeDecodeError):
                formatted_content = content
            except Exception as e:
                logger.error(f"LLM http req failed: {e}")
                
            logger.info(
                f"LLM http Response: {response.status_code},{request.url}\n>>>>>>>>>>\n{formatted_content}\n"
            )
            if response.status_code == 500:
                content = await response.aread()
                content = content.decode('utf-8')
                try:
                    content_json = json.loads(content)
                    formatted_content = json.dumps(content_json, indent=2, ensure_ascii=False)
                    logger.error(f"LLM http req failed: {formatted_content}")
                    # return new
                except json.JSONDecodeError:
                    logger.error(f"LLM http req failed: {content}")
                except Exception as e:
                    logger.error(f"LLM http req failed: {e}")
            
            return response
        except Exception as e:
            logger.error(f"LLM http req failed: {e}")
            raise e
