import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

capabilities: dict[str, str | bool | None] = {
    "platformName": os.environ.get("PLATFORMNAME"),
    "platformVersion": os.environ.get("PLATFORMVERSION"),
    "automationNam": os.environ.get("AUTOMATIONNAME"),
    "deviceName": os.environ.get("DEVICENAME"),
    # "appPackage": os.environ.get("APPPACKAGE"),
    # "appActivity": os.environ.get("APPACTIVITY"),
    # "appActivity": ".MainActivity",
    # "appWaitActivity": ".LauncherActivity",
    "language": os.environ.get("LANGUAGE"),
    "autoGrantPermissions": True,  # GRANT PERMISSIONS FOR ANDROID
    "autoDismissAlerts": True,
    "autoAcceptAlerts": True,
}

appium_server_url: str = f"http://{os.environ.get('HOST')}:{os.environ.get('PORT')}"
app_id = os.environ.get("APPPACKAGE")
