import re
import sys
from pathlib import Path

client_path = Path("src/client.py")

content = client_path.read_text()
new_content = re.sub(
    r'http://0\.0\.0\.0:8050/sse',
    'http://paylink-app.eastus.azurecontainer.io:8050/sse',
    content
)
client_path.write_text(new_content)

print("[✔] Updated server URL in client.py")
