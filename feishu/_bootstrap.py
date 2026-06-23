"""把 feishu/ 目录加入 import 路径，让脚本无论从哪运行都能 `from config import ...`。

每个可执行脚本第一行 `import _bootstrap` 即可。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
