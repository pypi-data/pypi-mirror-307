import requests

# gpt-4o的API
import requests
import logging
import time
from typing import Optional
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential

# 配置日志
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.StreamHandler(),  # 输出到控制台
#         logging.FileHandler('app.log')  # 输出到文件
#     ]
# )
logger = logging.getLogger(__name__)

class LLMAPIError(Exception):
    """自定义API异常类"""
    pass

@retry(
    stop=stop_after_attempt(3),  # 最多重试3次
    wait=wait_exponential(multiplier=1, min=4, max=10),  # 指数退避重试
    reraise=True
)
def chat_completions(messages: list, timeout: int = 30, provider="azure-openai", model="gpt-4o", temperature=1.0) -> Optional[str]:
    """
    调用GPT-4 API的函数
    
    Args:
        messages (list): 消息列表
        timeout (int): 请求超时时间（秒）
    
    Returns:
        Optional[str]: API返回的内容，如果发生错误返回None
    
    Raises:
        LLMAPIError: 当API调用出现问题时
    """
    # if not isinstance(prompt, str) or not prompt.strip():
    #     raise ValueError("Prompt must be a non-empty string")

    url = "https://dev-outside-ai-service.smzdm.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer lt_dev_test",
        "Z-PROVIDER-NAME": provider,
    }
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }

    try:
        logger.info(f"Sending request to GPT API with prompt:")
        
        response = requests.post(
            url, 
            headers=headers, 
            json=data,
            timeout=timeout
        )
        
        # 检查HTTP状态码
        response.raise_for_status()
        
        # 解析响应
        response_data = response.json()
        
        # 验证响应数据的结构
        if not response_data.get("choices"):
            raise LLMAPIError("Invalid API response format: 'choices' not found")
        
        if not response_data["choices"][0].get("message"):
            raise LLMAPIError("Invalid API response format: 'message' not found")
        
        content = response_data["choices"][0]["message"].get("content")
        
        if content is None:
            raise LLMAPIError("Invalid API response format: 'content' not found")

        logger.info("Successfully received response from GPT API")
        return content

    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        raise LLMAPIError("Request timed out")
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {str(e)}")
        raise LLMAPIError(f"HTTP error: {str(e)}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while making request: {str(e)}")
        raise LLMAPIError(f"Request error: {str(e)}")
    
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"Error parsing response: {str(e)}")
        raise LLMAPIError(f"Response parsing error: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise LLMAPIError(f"Unexpected error: {str(e)}")

# 使用示例
if __name__ == "__main__":
    try:
        prompt = "Tell me a joke"
        result = chat_completions(prompt)
        print(f"Response: {result}")
    except LLMAPIError as e:
        print(f"Error occurred: {str(e)}")