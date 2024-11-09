# sparrow-python
[![image](https://img.shields.io/badge/Pypi-0.1.7-green.svg)](https://pypi.org/project/sparrow-python)
[![image](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-kunyuan-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)


-------------------------
## TODO
- [ ]  from mod_base.cv.image.image_processor import messages_preprocess 添加是否对网络url替换为base64的控制；添加对video切帧的支持



parse code

```python
import ast
import asyncio
import re
from functools import wraps

import json5
import yaml
from loguru import logger
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def extract_code_snippets(text, strict=True):
    """Extract code snippets"""
    # 首先处理带有 ``` 标志的代码块
    pattern = r"```(\w+)?\s*([\s\S]*?)```"
    matches = re.findall(pattern, text)

    code_snippets = []
    for lang, code in matches:
        code_snippets.append({
            "language": lang.strip() if lang else "unknown",
            "code": code.strip(),
        })

    if not strict:
        # 查找并排除已经被处理过的 ``` ... ``` 内的代码块
        text = re.sub(pattern, "", text)

        # 处理剩下的 { ... } 格式的代码块
        pattern = r"\{[\s\S]*?\}"
        matches = re.findall(pattern, text)

        for code in matches:
            code_snippets.append({
                "language": "unknown",
                "code": code.strip(),
            })

    return code_snippets


def parse_to_obj(text: str, strict=False):
    """Parse to obj"""
    code_snippets = extract_code_snippets(text, strict=strict)
    code_snippets = [code_snippet["code"] for code_snippet in code_snippets]
    code_snippets = [code_snippet.strip() for code_snippet in code_snippets if code_snippet.strip()]
    if not code_snippets:
        return None
    code_str = code_snippets[-1]
    try:
        return ast.literal_eval(code_str)
    except:
        return json5.loads(code_str)


def parse_to_code(text: str, strict=False) -> str | None:
    """Parse to code"""
    code_snippets = extract_code_snippets(text, strict=strict)
    code_snippets = [code_snippet["code"] for code_snippet in code_snippets]
    code_snippets = [code_snippet.strip() for code_snippet in code_snippets if code_snippet.strip()]
    if not code_snippets:
        return None
    code_str = code_snippets[-1]
    return code_str


def print_markdown(md: str):
    """Display markdown in console"""
    console.print(Markdown(md))


# 自定义多行字符串的显示方式，去除行尾空格
def str_presenter(dumper, data):
    """
    """
    # 去除每一行的行尾空格
    data = "\n".join([line.rstrip() for line in data.splitlines()])
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


# 添加自定义表示器
yaml.add_representer(str, str_presenter)


def yaml_dump(abs_path, data, mode="w"):
    """Yaml dump"""
    with open(abs_path, mode=mode, encoding="utf-8") as fw:
        yaml.dump(data, fw, allow_unicode=True, indent=4, sort_keys=False, default_flow_style=False)


def async_retry(
        max_retries=3,
        delay=1,
        backoff=2,
):
    """An asynchronous decorator for automatically retrying an async function upon encountering specified exceptions.

    Args:
        max_retries (int): The maximum number of times to retry the function.
        delay (float): The initial delay between retries in seconds.
        backoff (float): The multiplier by which the delay should increase after each retry.

    Returns:
        The return value of the wrapped function, if it succeeds.
        Raises the last encountered exception if the function never succeeds.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            while retries <= max_retries:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:

                    if retries == max_retries:
                        raise

                    retries += 1
                    logger.warning(
                        f"Error:{type(e)}\n"
                        f"Retrying `{func.__name__}` after {current_delay} seconds, retry : {retries}\n",
                    )
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator

```
vllm 异步推理示例：

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.sampling_params import SamplingParams
import torch

# Define request data model
class RequestData(BaseModel):
    prompts: List[str]
    max_tokens: int = 2048
    temperature: float = 0.7

# Initialize FastAPI app
app = FastAPI()

# Determine device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize AsyncLLMEngine
engine_args = AsyncEngineArgs(
    model="your-model-name",  # Replace with your model name
    dtype="bfloat16",
    gpu_memory_utilization=0.8,
    max_model_len=4096,
    trust_remote_code=True
)
llm_engine = AsyncLLMEngine.from_engine_args(engine_args)

# Define the inference endpoint
@app.post("/predict")
async def generate_text(data: RequestData):
    sampling_params = SamplingParams(
        max_tokens=data.max_tokens,
        temperature=data.temperature
    )
    request_id = "unique_request_id"  # Generate a unique request ID
    results_generator = llm_engine.generate(data.prompts, sampling_params, request_id)
    
    final_output = None
    async for request_output in results_generator:
        final_output = request_output
    
    assert final_output is not None
    text_outputs = [output.text for output in final_output.outputs]
    return {"responses": text_outputs}

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

## 待添加脚本



## Install

```bash
pip install sparrow-python
# Or dev version
pip install sparrow-python[dev]
# Or
pip install -e .
# Or
pip install -e .[dev]
```

## Usage

### Multiprocessing SyncManager

Open server first:

```bash
$ spr start-server
```

The defualt port `50001`.

(Process1) productor:

```python
from sparrow.multiprocess.client import Client

client = Client(port=50001)
client.update_dict({'a': 1, 'b': 2})
```

(Process2) consumer:

```python
from sparrow.multiprocess.client import Client

client = Client(port=50001)
print(client.get_dict_data())

>> > {'a': 1, 'b': 2}
```

### Common tools

- **Kill process by port**

```bash
$ spr kill {port}
```

- **pack & unpack**  
  support archive format: "zip", "tar", "gztar", "bztar", or "xztar".

```bash
$ spr pack pack_dir
```

```bash
$ spr unpack filename extract_dir
```

- **Scaffold**

```bash
$ spr create awosome-project
```

### Some useful functions

> `sparrow.relp`  
> Relative path, which is used to read or save files more easily.

> `sparrow.performance.MeasureTime`  
> For measuring time (including gpu time)

> `sparrow.performance.get_process_memory`  
> Get the memory size occupied by the process

> `sparrow.performance.get_virtual_memory`  
> Get virtual machine memory information

> `sparrow.add_env_path`  
> Add python environment variable (use relative file path)

### Safe logger in `multiprocessing`

```python
from sparrow.log import Logger
import numpy as np

logger = Logger(name='train-log', log_dir='./logs', )
logger.info("hello", "numpy:", np.arange(10))

logger2 = Logger.get_logger('train-log')
print(id(logger2) == id(logger))
>> > True
```
