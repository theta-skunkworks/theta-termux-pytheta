# pyTheta.py

Japanese page [here](README_jp.md)

## Overview

pyTheta.py is a Python script for setting shooting parameters and shooting with simple commands in an environment where Termux is installed in THETA.<br>For commands, see the “List of commands” chapter.<br>See the “Response message specification” chapter for command responses.

## How to use

There are three ways to use this script.

(1) If this script is executed without any arguments, commands can be executed continuously from the command prompt ">>". It is the most standard usage that is assumed.

```
$ ./pyTheta.py
>>
>> mode
i-AUTO 0.0ev auto
>> mode m
i-MANU F2.1 ss1/60 iso100 auto
>> ss 1"
i-MANU F2.1 ss 1" iso100 auto
>>
>> movie
m-AUTO 0.0ev auto
>> image
i-MANU F2.1 ss 1" iso100 auto
>>
>> q
#### (^-^)/~ Bye! ####
$
```

(2) By giving a command to the argument of this script, the command can be executed once. This is useful when calling this script from a shell script.

```
$ ./pyTheta.py mode
i-AUTO 0.0ev auto
$ ./pyTheta.py mode m
i-MANU F2.1 ss1/60 iso100 auto
$ ./pyTheta.py ss 1\"
i-MANU F2.1 ss 1" iso100 auto
$
$ .pyTheta.py movie
m-AUTO 0.0ev auto
$ .pyTheta.py image
i-MANU F2.1 ss 1" iso100 auto
$
```

(3) By importing this script into other Python scripts, you can partially use the functions included in this script.


## Setup
Please refer to [this article](https://community.theta360.guide/t/how-to-set-up-a-linux-environment-in-the-theta-to-control-the-camera-with-bash-ruby-python/5013) for how to install Termux environment in THETA.<br>The same is true for installing Python in a Termux environment.<br>([The original article is in Japanese.](https://qiita.com/KA-2/items/29bd65f0b38925ad5417))

This script uses PycURL. If you have not installed it, install it with the following command. <br>(Please install while connected to the external network)

```
pip install pycurl
```

After placing the script in the directory of your choice, attach execution privileges to the script with the following command.

```
chmod +x pyTheta.py
```

## When using this script on an external device

This script also works in the Python execution environment connected to THETA via Wi-Fi when the Shebang, IP address, and port number are rewritten.

### Shebang

For Termux

```py:pyTheta.py(Original)
#!/data/data/com.termux/files/usr/bin/python
```

For other Linux platforms
The following is an example. Please adapt to your environment.

```py:pyTheta.py(For_other_Linux)
#!/usr/bin/python3
#!/usr/bin/env python3
```

### IP address and port
For Termux on THETA

```py:pyTheta.py(Original)
#--- THETA IP & Port ---
ip='127.0.0.1'
port='8080'
```

For other Linux platforms (ex: RasPi, Termux installed on smartphone)

```py:pyTheta.py(After_change)
#--- THETA IP & Port ---
ip='192.168.1.1'
port='80'
```

## List of commands

The command is in the format of “Command character string + Single-byte space + Value character string”.<br>(Example: If you want to specify -0.3 for exposure compensation, it will be "ev -0.3")

|Command<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|Value<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|Description<br>&nbsp;|
|---|---|---|
| tp | None | Shooting Trigger <br> Same as shutter <br> 'tp' is an abbreviation for 'take picture' |
| shutter | None| Shooting Trigger <br> Same as tp |
| image | None | Set capture mode to still image mode |
| movie | None | Set capture mode to movie mode |
| mode | None/+/-/ <br>p/av/tv/iso/m | Specify the exposure program. <br> If there is no value, the current value is returned. <br> 'av' is only valid for Z1. |
| ev | None/+/-/ <br> Numbers defined in the webAPI specification [exposureCompensation](https://api.ricoh/docs/theta-web-api-v2.1/options/exposure_compensation/) . | Specify the exposure compensation value. <br> If there is no value, the current value is returned. |
| ss | None/+/-/ <br> <br> -For more than 1 second <br> webAPI specification [shutterSpeed](https://api.ricoh/docs/theta-web-api-v2.1/options/shutter_speed/) A character string with "" (double quotes) "appended after the numerical value. <br> (Example: 1sec = 1") <br> <br>-If shorter than 1 second <br> webAPI specification [shutterSpeed](https://api.ricoh/docs/theta-web-api-v2.1/options/shutter_speed/) Numeric denominator only. <br> (Example: 1/1000sec = 1000) | Specify shutter speed. <br> If no value, current value Returns |
| iso | None/+/-/ <br> Numeric value defined in webAPI specification [iso](https://api.ricoh/docs/theta-web-api-v2.1/options/iso/) . | Specify the ISO sensitivity. <br> If there is no value, the current value is returned. |
| f | None/+/-/ <br> Numeric value defined in webAPI specification [aperture](https://api.ricoh/docs/theta-web-api-v2.1/options/aperture/) . | Specify the aperture value. <br> If there is no value, the current value is returned. <br> Valid only with Z1. |
| wb | None/+/-/ <br> <br>-For preset WB <br>auto/day/shade/cloud/lamp1/lamp2/fluo1/fluo2/fluo3/fluo4<br> <br>-For Color temperature <br> Numerical value of color temperature defined in the webAPI specification [_colorTemperature] (https://api.ricoh/docs/theta-web-api-v2.1/options/_color_temperature/).<br> | Specify the white balance. <br>If there is no value, the current value is returned. <br> Depending on the value, you can choose between preset white balance and color temperature specification. |
| timer | None/A number between 0 and 10 | Specifies the timer behavior. <br>If 0 is specified, the timer is turned off. <br> If there is no value, the current value is returned. |
| ts | on / off | Specify whether or not to use time shift shooting.<br>If there is no value, the current value is returned. |
| vol | None/value between 0 and 100 | Sets the volume of THETA. <br>If there is no value, the current value is returned. |
| q/quit/<br>exit/bye | None | Exits continuous command input. |


## Response message specification

The response string specifications are summarized below.

### Basic response

The format changes depending on the exposure program.<br>Each is as follows.

| Exposure Program | Response String Format |
| --- | --- |
| AUTO |[i/m]-AUTO [Exposure compensation value] ev[White balance] ['ts' when TimeShift is on] [timer 1 to 10. Not displayed when 0]|
| Aperture priority <br> (Z1 only) |[i/m]-Av [Exposure compensation value]ev F[Aperture value] [White balance] ['ts' when TimeShift is on] [timer 1 to 10. Not displayed when 0]|
| Shutter speed priority |[i/m]-Tv [Exposure compensation value]ev ss[Shutter speed] [White balance] ['ts' when TimeShift is on] [timer 1 to 10. Not displayed when 0]|
| ISO sensitivity priority |[i/m]-ISO [Exposure compensation value]ev iso[ISO sensitivity] [White balance] ['ts' when TimeShift is on] [timer 1 to 10. Not displayed when 0]|
| MANUAL |[i/m]-MANU F[Aperture value] [Shutter speed] [ISO sensitivity] [White balance] ['ts' when TimeShift is on] [timer 1 to 10. Not displayed when 0]|

* The first [i/m] indicates Capture Mode.
* Vol command only Returns only the volume value.

### When THETA recognizes an error

| String | description |
| --- | --- |
| UndefCmd | Undefined command |
| SplitERR | There are 3 or more blocks separated by spaces |
| BUSY | THETA BUSY (just after shooting) |
| ParamERR | Incorrect parameter (value) |


## Development Environment

### Camera
* RICOH THETA Z1 Firmware ver.1.11.1 and above
* RICOH THETA V Firmware ver.3.06.1 and above

### Software
* Termux 0.84
* Python 3.8.0
* pip 19.3.1 <br>from /data/data/com.termux/files/usr/lib/python3.8/site-packages/pip (python 3.8)
* PycURL 7.43.0.3


## License

```
Copyright 2018 Ricoh Company, Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Contact
![Contact](img/contact.png)

