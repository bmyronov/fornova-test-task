## Usage
- Rename `.env_example` to `.env`.

    ```
    PLATFORMNAME=Android # Platforn you're gonna use e.g. 'Android'
    PLATFORMVERSION=12 # Android version you're using
    AUTOMATIONNAME=uiautomator2
    DEVICENAME=HA1SL3H2 # Device id you can check it with 'adb devices'
    APPPACKAGE=com.tripadvisor.tripadvisor # App id
    # APPACTIVITY=.OnboardingActivity
    LANGUAGE=en
    HOST=localhost
    PORT=4723
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

    # filename="./logs/basic.log", # Uncomment it if you want to save logs to the log file.
)
...