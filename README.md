## Fornava Test
Project structure:
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

## Other helpful resources


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

    ![alt text](https://github.com/bmyronov/fornova-test-task/blob/main/media/windows_environment _variables.png?raw=true)


- appium server
- python 3.12+
- java sdk

## Getting Started
