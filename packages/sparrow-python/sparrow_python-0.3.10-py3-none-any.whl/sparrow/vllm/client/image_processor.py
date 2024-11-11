import base64
import os
from io import BytesIO
from PIL import Image
import asyncio
import aiohttp
import requests


def encode_base64_from_local_path(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


async def encode_base64_from_url(url, session: aiohttp.ClientSession):
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        return base64.b64encode(content).decode("utf-8")

def encode_base64_from_url_slow(url):
    response = requests.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")

def encode_base64_from_pil(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


async def encode_image_to_base64(image_url, session):
    if isinstance(image_url, str):
        # 处理 "file://" 前缀的本地路径
        if image_url.startswith("file://"):
            file_path = image_url[7:]  # 去掉 "file://"
            if os.path.exists(file_path):
                return encode_base64_from_local_path(file_path)
            else:
                raise ValueError("本地文件未找到。")
        elif os.path.exists(image_url):
            # 本地文件路径，无需 "file://"
            return encode_base64_from_local_path(image_url)
        elif image_url.startswith("http"):
            # 网络 URL - 异步下载
            return await encode_base64_from_url(image_url, session)
        else:
            raise ValueError("不支持的图像来源类型。")
    elif isinstance(image_url, Image.Image):
        # PIL 图像
        return encode_base64_from_pil(image_url)
    else:
        raise ValueError("不支持的图像来源类型。")


async def messages_preprocess(messages):
    async def process_image_content(content, session):
        image_url = content["image_url"].get("url")
        image_base64 = await encode_image_to_base64(image_url, session)
        content["image_url"]["url"] = f"data:image/jpeg;base64,{image_base64}"

    async with aiohttp.ClientSession() as session:
        tasks = []

        for message in messages:
            if message["role"] == "user" and "content" in message:
                for content in message["content"]:
                    if content.get("type") == "image_url":
                        tasks.append(process_image_content(content, session))

        # Concurrently process all image URLs
        await asyncio.gather(*tasks)

    return messages


if __name__ == "__main__":
    from sparrow import relp
    # Example usage:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请描述这几张图片"},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}},
                {"type": "image_url", "image_url": {"url": f"{relp('./test_img.jpg')}"}},
            ],
        }
    ]
    from rich import print
    from sparrow import MeasureTime
    mt = MeasureTime()

    processed_messages = asyncio.run(messages_preprocess(messages))
    message = processed_messages[0]
    print(message)
    mt.show_interval()
