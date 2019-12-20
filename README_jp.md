# pyTheta.py

English page [here](README.md)

## Overview

pyTheta.pyは、TermuxをTHETAにインストールした環境において、簡単なコマンドで撮影パラメータの設定や撮影を行うためのPythonスクリプトです。<br>コマンドについては「List of commands」の章を参照してください。<br>コマンドの応答については「Response message specification」の章を参照してください。

## How to use
本スクリプトは以下３通りの利用方法があります。

(1) 本スクリプトを引数なしで実行すると、コマンドプロンプト「>>」から、連続してコマンドを実行できます。想定している最もスタンダードな使い方です。

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

(2) 本スクリプトの引数にコマンドを与えることで、1回づつコマンドを実行できます。シェルスクリプトなどから本スクリプトを呼び出す時に便利です。

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

(3) 他のPythonスクリプトに本スクリプトをimportして、本スクリプトに含まれる関数を部分利用することができます。


## Setup
THETAへのTermux環境導入方法については[こちらの記事](https://qiita.com/KA-2/items/29bd65f0b38925ad5417)を参照してください。<br>Termux環境へのPythonインストールについても同様です。

本スクリプトはPycURLを利用しています。インストールしていない方は以下コマンドでインストールしてください。<br>（インストールは、外部ネットワークに接続した状態で行ってください）

```
pip install pycurl
```

お好みのディレクトリにスクリプトを配置したあとは、以下コマンドでスクリプトに実行権限をつけてください。

```
chmod +x pyTheta.py
```

## When using this script on an external device

本スクリプトは、シバン（Shebang）、IPアドレス、ポート番号を書き換えると、THETAにWi-Fi経由で接続したPython実行環境でも動作します。

### シバン（Shebang）

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

### IPアドレスとポート
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

コマンドは「コマンド文字列+半角スペース+値」の形式です。 <br>(例:露出補正を-0.3に指定したい場合には「ev -0.3」となります)

|コマンド<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|値<br>&nbsp;|説明<br>&nbsp;|
|---|---|---|
|tp|なし|撮影のトリガー<br>shutterと同じ<br>’tp’は’take picture’を略した文字列|
|shutter|なし|撮影のトリガー<br>tpと同じ|
|image|なし|Capture Modeを静止画モードにする|
|movie|なし|Capture Modeを動画モードにする|
|mode|なし/+/-/<br>p/av/tv/iso/m|露出プログラムを指定します。<br>値なしの場合、現在の値を返します。<br>'av'はZ1でのみ有効です。|
|ev|なし/+/-/<br>webAPIの仕様書 [exposureCompensation](https://api.ricoh/docs/theta-web-api-v2.1/options/exposure_compensation/)で定義された数値。|露出補正値を指定します。<br>値なしの場合、現在の値を返します。|
|ss|なし/+/-/<br><br>・1秒以上の場合<br>webAPIの仕様書 [shutterSpeed](https://api.ricoh/docs/theta-web-api-v2.1/options/shutter_speed/)で定義された数値の後ろに「"（ダブルクォート）」を付与した文字列。<br>(例:1sec=1")<br><br>・1秒より短い場合<br>webAPIの仕様書 [shutterSpeed](https://api.ricoh/docs/theta-web-api-v2.1/options/shutter_speed/)で定義された数値の分母のみ。<br>(例:1/1000sec=1000)|シャッター速度を指定します。<br>値なしの場合、現在の値を返します。|
|iso|なし/+/-/<br>webAPIの仕様書 [iso](https://api.ricoh/docs/theta-web-api-v2.1/options/iso/)で定義された数値。|ISO感度を指定します。<br>値なしの場合、現在の値を返します。|
|f|なし/+/-/<br>webAPIの仕様書 [aperture](https://api.ricoh/docs/theta-web-api-v2.1/options/aperture/)で定義された数値。|絞り値を指定します。<br>値なしの場合、現在の値を返します。<br>Z1でのみ有効です。|
|wb|なし/+/-/<br><br>・プリセットWBの場合<br>auto/day/shade/cloud/lamp1/lamp2/fluo1/fluo2/fluo3/fluo4<br><br>・色温度の場合<br>webAPIの仕様書 [_colorTemperature](https://api.ricoh/docs/theta-web-api-v2.1/options/white_balance/)で定義された色温度の数値。<br>|ホワイトバランスを指定します。<br>値なしの場合、現在の値を返します。<br>値により、プリセットホワイトバランスと色温度指定のいずれかを選択することができます。|
|timer|なし/0～10までの数値のいずれか|タイマーの振る舞いを指定します。<br>0を指定するとタイマーOFFとなります。<br>値なしの場合、現在の値を返します。|
|ts|なし/on/off|タイムシフト撮影をする/しないを指定します。<br>値なしの場合、現在の値を返します。|
|vol|なし/0～100の数値|THETAの音量を設定します。<br>値なしの場合、現在の値を返します。|
|q/quit/<br>exit/bye|なし|連続コマンド入力を終了する。|


## Response message specification

応答文字列の仕様を以下にまとめます。

### Basic response

露出プログラムに応じてフォーマットが変わります。<br>それぞれ以下のとおりです。

|露出プログラム|応答文字列フォーマット|
|---|---|
|オート|[i/m]-AUTO [露出補正値]ev [ホワイトバランス] [TimeShift onのとき'ts'] [timer1～10:0のときは非表示]|
|絞り優先<br>（Z1のみ）|[i/m]-Av [露出補正値]ev F[絞り値] [ホワイトバランス] [TimeShift onのとき'ts'] [timer1～10:0のときは非表示]|
|シャッター速度優先|[i/m]-Tv [露出補正値]ev ss[シャッター速度] [ホワイトバランス] [TimeShift onのとき'ts'] [timer1～10:0のときは非表示]|
|ISO感度優先|[i/m]-ISO [露出補正値]ev iso[ISO感度] [ホワイトバランス] [TimeShift onのとき'ts'] [timer1～10:0のときは非表示]|
|マニュアル|[i/m]-MANU F[絞り値] [シャッター速度] [ISO感度] [ホワイトバランス] [TimeShift onのとき'ts'] [timer1～10:0のときは非表示]|

* 先頭の[i/m]はCapture Modeを示します。
* Volコマンドののみ 音量の数値だけを返します。


### When THETA recognizes an error

|文字列|説明|
|---|---|
|UndefCmd|未定義コマンド|
|SplitERR|スペースで分割されたブロックが3以上ある|
|BUSY    |THETAがBUSY（撮影直後など）|
|ParamERR|パラメータ（値）に間違いがある|



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

