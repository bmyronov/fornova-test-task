import os
from dotenv import load_dotenv

load_dotenv()

TEST_RUNNER_URL: str = (
    f"http://{os.environ.get('TEST_RUNNER_HOST')}:{os.environ.get('TEST_RUNNER_PORT')}"
)

print(TEST_RUNNER_URL)
