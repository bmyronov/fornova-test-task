# Fornava Test
## Project structure:
- Task 1 -> test_runner
- Task 2 -> task2
- Task 3 -> task3

## Before we start
Acording to the task to write test_runner I should have used Genymotion emulator or use Android phone.

After lots of tries and errors I wasn't able to run Tripadvisor app in Genymotion.
Acording to their documentation:

> If your application is not available in Google Play Store, or if you get the message ```This device isn't supported with this version```, it usually means that it is only available for ARM.
> In that case, please refer to the Applications for ARM/ARM64 section below.

I wans't able to test it on Mac with Arm processor and on the device with arm processor wasn't able to run Genimotion.

So all the test were made on Android device.

I used Lenovo Tablet as my test device (for those who will try to recreate in emulator).

## Requirements
First you need to install Java. To do that install java from their [official cite](https://www.java.com/en/download/) or if you are on Linux install `openjdk` e.g. `sudo dnf install openjdk` or `sudo apt install openjdk`.

After you've installed java install [Android Studion](https://developer.android.com/studio). It install android sdk and all the necessary staff.

Don't forget to set environment variables for Java and Android sdk. 

- On *Linux* you can do it by adding code bellow to your `.bashrc` or `.zshrc` file (just look for java-openjdk path and Andorid sdk path on your system):
``` bash
# JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk

# ANDROID_HOME

export ANDROID_HOME=~/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools
```
- On *Windows*:
    - Open the System Control Panel: You can search for "environment variables" or navigate to "System" -> "Advanced system settings" -> "Environment Variables".
    Add Local Environment Variables as shown below:

    ![alt text](https://github.com/bmyronov/fornova-test-task/blob/main/media/windows_environment_variables.png?raw=true)

- Install [nodejs](https://nodejs.org/en). On *Linux* run `sudo dnf install nodejs npm` or `sudo apt install nodejs npm`.
- Install appium server folowing [official documentation](https://appium.io/docs/en/latest/quickstart/).
*Additional*: if you want to add [Appium Inspector](https://appium.github.io/appium-inspector/latest/quickstart/installation/) run `https://appium.github.io/appium-inspector/latest/quickstart/installation/`.
- To run appium server run `appium` or if you want to run appium with appium inspector run `appium --use-plugins=inspector --allow-cors`. Appium inspector url address `http://localhost:4723/inspector`.
- [UV](https://docs.astral.sh/uv/getting-started/installation/)

## Getting Started
### Before we start
Thanks to "deep and clear" documentation of Appium I made too many mistakes that are not directly addressed in the docs.

First of all the docs suggests to run the app through `capabilities`:
``` python
capabilities: dict[str, str | bool | None] = {
    ...

    "appPackage": os.environ.get("APPPACKAGE"),
    "appActivity": os.environ.get("APPACTIVITY"),
    ...
}
```
But if you do so evry time you start the app it launches new instance of the app without save credentials and so on. Tripadvisor when launched for the first time asks you to authorize and it launches google.auth activity. As the activity differs from the one you specified it brakes the first step.

So to launch the app you should do it with `driver.activate_app(app_id)`.

Some very useful links:
- [Appium UiAutomator2 Driver](https://github.com/appium/appium-uiautomator2-driver#app)
- [Write a Test (Python)](https://appium.io/docs/en/latest/quickstart/test-py/)

### **Task 1 (test_runner)**
Before running the script launch Tripadvisor app on your device and authorize with your google account or any other method so the authorization doesn't bother you in the future (it may brake the script).
- Rename `.env_example` to `.env`.

    ```
    PLATFORMNAME=Android # Platforn you're gonna use e.g. 'Android'
    PLATFORMVERSION=12 # Android version you're using
    AUTOMATIONNAME=uiautomator2
    DEVICENAME=HA1SL3H2 # Device id you can check it with 'adb devices'
    APPPACKAGE=com.tripadvisor.tripadvisor # App id
    # APPACTIVITY=.OnboardingActivity
    LANGUAGE=en
    HOST=localhost # Appium host
    PORT=4723 # Appium port
    ```
    To get uuid of your adroid device or adnroid emulator instance run `adb devices`:
    ```
    List of devices attached
    HA1SL3H2        device
    ```
    Copy the uuid of the device connected and paste it to `.env`:
    ```
    ...

    DEVICENAME=your_device_uuid
    ...
    ```
    To get app id launch the app on your device and on your system run command `adb shell "dumpsys activity activities | grep ResumedActivity"`:
    ```
    mResumedActivity: ActivityRecord{5372e02 u0 com.tripadvisor.tripadvisor/com.tripadvisor.android.ui.primarynavcontainer.MainActivity t1717}
    ResumedActivity: ActivityRecord{5372e02 u0 com.tripadvisor.tripadvisor/com.tripadvisor.android.ui.primarynavcontainer.MainActivity t1717}
    ```
    `com.tripadvisor.tripadvisor` is the app id. Paste it to `.env` file:
    ```
    ...

    APPPACKAGE=com.tripadvisor.tripadvisor
    ...
    ```
- To install project's dependencies run `uv sync --frozen --no-cache`
- To run the program `uv run main.py`

When the program finishes it logs the result, saves screenshots in screenshots folder and closes the app on the device.
If you want to save logs uncomment this in `main.py` file:
``` python
...

logger = logging.basicConfig(
    ...

    # filename="./logs/basic.log", # Uncomment if you want to save logs to the log file.
)
...
```

### **Task 1 (task2)**
Task 2 is a proof of consept of task 3.
The client makes api call to API (`GET /search`). The api makes `POST request` to `test_runner` with parameters `{hotel_name: date_list}`.
``` python
{
"The Grosvenor Hotel": [
    ["June 15", "June 16"],
    ["June 16", "June 17"],
    ["June 17", "June 18"],
    ["June 18", "June 19"],
    ["June 19", "June 26"]
]
}
```
![alt text](https://github.com/bmyronov/fornova-test-task/blob/main/media/diagram_task2_1.png?raw=true)

`/search` - user makes api GET request. Api then makes POST request to the test_runner and waits for the result.