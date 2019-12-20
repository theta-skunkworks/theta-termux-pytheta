#!/data/data/com.termux/files/usr/bin/python
#
# Copyright 2018 Ricoh Company, Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import pycurl
import json
#Hide warnings from perform_rs(), perform_rb(), perform().
import warnings
warnings.filterwarnings('ignore')


#--- THETA IP & Port ---
ip='127.0.0.1'
port='8080'

#--- THETA API URLs ---
urlInfo     = '/osc/info'
urlState    = '/osc/state'
urlChkForUp = '/osc/checkForUpdates'
urlCmdExe   = '/osc/commands/execute'
urlCmdStat  = '/osc/commands/status'

#--- Global variable ---
bTimeShift = False

#--- Fixed values ---

MINUS = '-'
PLUS  = '+'

CAPSTAT_IDLE  = 'idle'

CAPMODE_TGGLE = ''
CAPMODE_IMAGE = 'image'
CAPMODE_VIDEO = 'video'

EXP_PROG = [
	'UNDEF',
	'MANU',
	'AUTO',
	'Av',
	'Tv',
	'UNDEF',
	'UNDEF',
	'UNDEF',
	'UNDEF',
	'ISO']

EXP_PROG_CMD = [
	'UNDEF',
	'm',
	'p',
	'av',
	'tv',
	'UNDEF',
	'UNDEF',
	'UNDEF',
	'UNDEF',
	'iso']

SS_CMD2API = {
		""  : "",
		"+" : "+",
		"-" : "-",
		"25000": "0.00004",
		"20000": "0.00005",
		"16000": "0.0000625",
		"12500": "0.00008",
		"10000": "0.0001",
		"8000":  "0.000125",
		"6400":  "0.00015625",
		"5000":  "0.0002",
		"4000":  "0.00025",
		"3200":  "0.0003125",
		"2500":  "0.0004",
		"2000":  "0.0005",
		"1600":  "0.000625",
		"1250":  "0.0008",
		"1000":  "0.001",
		"800":   "0.00125",
		"640":   "0.0015625",
		"500":   "0.002",
		"400":   "0.0025",
		"320":   "0.003125",
		"250":   "0.004",
		"200":   "0.005",
		"160":   "0.00625",
		"125":   "0.008",
		"100":   "0.01",
		"80":    "0.0125",
		"60":    "0.01666666",
		"50":    "0.02",
		"40":    "0.025",
		"30":    "0.03333333",
		"25":    "0.04",
		"20":    "0.05",
		"15":    "0.06666666",
		"13":    "0.07692307",
		"10":    "0.1",
		"8":     "0.125",
		"6":     "0.16666666",
		"5":     "0.2",
		"4":     "0.25",
		"3":     "0.33333333",
		"2.5":   "0.4",
		"2":     "0.5",
		"1.6":   "0.625",
		"1.3":   "0.76923076",
		"1\"":   "1",
		"1.3\"": "1.3",
		"1.6\"": "1.6",
		"2\"":   "2",
		"2.5\"": "2.5",
		"3.2\"": "3.2",
		"4\"":   "4",
		"5\"":   "5",
		"6\"":   "6",
		"8\"":   "8",
		"10\"":  "10",
		"13\"":  "13",
		"15\"":  "15",
		"20\"":  "20",
		"25\"":  "25",
		"30\"":  "30",
		"60\"":  "60" 
	}

WB_CMD2API = {
		""     : "",
		"+"    : "+",
		"-"    : "-",
		"auto" : "auto",
		"day"  : "daylight",
		"shade": "shade",
		"cloud": "cloudy-daylight",
		"lamp1": "incandescent",
		"lamp2": "_warmWhiteFluorescent",
		"fluo1": "_dayLightFluorescent",
		"fluo2": "_dayWhiteFluorescent",
		"fluo3": "fluorescent",
		"fluo4": "_bulbFluorescent"
	}

WB_CT  = "_colorTemperature"


EXPOSURE_DELAY_CUR = -2
EXPOSURE_DELAY_TGGLE = -1
EXPOSURE_DELAY_OFF = 0
EXPOSURE_DELAY_MAX = 10

TIMER_CMD2API = {
		""   : EXPOSURE_DELAY_CUR ,
		"t"  : EXPOSURE_DELAY_TGGLE ,
		"0"  : 0 ,
		"1"  : 1 ,
		"2"  : 2 ,
		"3"  : 3 ,
		"4"  : 4 ,
		"5"  : 5 ,
		"6"  : 6 ,
		"7"  : 7 ,
		"8"  : 8 ,
		"9"  : 9 ,
		"10" : 10
	}


def thetaWebApiExec(post_get, url, send_param):
	
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, 'http://' + ip + ':' + port + url)
	curl.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json; charset=utf-8','-X-XSRF-Protected: 1'])
	curl.setopt(pycurl.CUSTOMREQUEST, post_get)
	if post_get == 'POST' :
		curl.setopt(pycurl.POSTFIELDS, send_param)
	
	return curl.perform_rs()


def shutterButton(bTimeShift):
	
	ret = thetaWebApiExec('POST', urlState, '')
	jsonRet = json.loads(ret)
	#print(json.dumps(jsonRet, indent=4))
	captureStatus = jsonRet['state']['_captureStatus']
	recordedTime = jsonRet['state']['_recordedTime']
	
	ret = thetaWebApiExec('POST', urlCmdExe, '{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\":[\"captureMode\"] } }')
	jsonRet = json.loads(ret)
	#print(json.dumps(jsonRet, indent=4))
	captureMode = jsonRet['results']['options']['captureMode']
	#print(captureMode)
	
	
	if captureMode == CAPMODE_IMAGE :
		if captureStatus == CAPSTAT_IDLE :
			if bTimeShift :
				jsonTakePicture = '{\"name\": \"camera.startCapture\", \"parameters\": {\"_mode\":\"timeShift\"} }'
			else :
				jsonTakePicture = '{\"name\": \"camera.takePicture\"}'
			
			ret = thetaWebApiExec('POST', urlCmdExe, jsonTakePicture)
			
		else :
			if bTimeShift :
				jsonTakePicture = '{\"name\": \"camera.stopCapture\" }'
				ret = thetaWebApiExec('POST', urlCmdExe, jsonTakePicture)
	else :
		if recordedTime == 0 :
			jsonStartStop ='{\"name\": \"camera.startCapture\" }'
		else :
			jsonStartStop ='{\"name\": \"camera.stopCapture\" }'
		
		ret = thetaWebApiExec('POST', urlCmdExe, jsonStartStop)
	
	return ret


def checkBusy():
	ret = thetaWebApiExec('POST', urlState, '')
	jsonRet = json.loads(ret)
	#print(json.dumps(jsonRet, indent=4))
	captureStatus = jsonRet['state']['_captureStatus']
	recordedTime = jsonRet['state']['_recordedTime']
	
	if captureStatus == CAPSTAT_IDLE and recordedTime == 0 :
		busy = False
	else :
		busy = True
	
	return busy


def changeCaptureMode(setCapMode):
	strResult = ''
	
	if not checkBusy() :
		if setCapMode == CAPMODE_TGGLE :
			jsonGetCapMode ='{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\":[\"captureMode\"] } }'
			ret = thetaWebApiExec('POST', urlCmdExe, jsonGetCapMode)
			jsonRet = json.loads(ret)
			#print(json.dumps(jsonRet, indent=4))
			curCapMode = jsonRet['results']['options']['captureMode']
			
			if curCapMode == CAPMODE_IMAGE :
				setCapMode = CAPMODE_VIDEO
			else :
				setCapMode = CAPMODE_IMAGE
		
		
		#print('setCapMode = ' + setCapMode )
		jsonSetCapMode = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"captureMode\":\"' + setCapMode + '\"} } }'
		ret = thetaWebApiExec('POST', urlCmdExe, jsonSetCapMode)
		
	else :
		strResult='BUSY'
	
	return strResult


def changeExpProg(setExpProg):
	strResult = ''
	
	if not checkBusy() :
		
		jsonGetExpProg = '{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\": [\"exposureProgram\", \"exposureProgramSupport\"] } }'
		ret = thetaWebApiExec('POST', urlCmdExe, jsonGetExpProg)
		jsonRet = json.loads(ret)
		#print(json.dumps(jsonRet, indent=4))
		curExpProg = jsonRet['results']['options']['exposureProgram']
		expProgSupport = jsonRet['results']['options']['exposureProgramSupport']
		
		if setExpProg==MINUS or setExpProg==PLUS :
			index = expProgSupport.index(curExpProg)
			
			nextPos=0
			if setExpProg==PLUS :
				nextPos = index + 1
				if nextPos >= len(expProgSupport) :
					nextPos = 0
			else :
				nextPos = index - 1
				if nextPos < 0 :
					nextPos = len(expProgSupport) -  1
			
			newExpProg = expProgSupport[nextPos]
			
			jsonSetExpProg = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"exposureProgram\":\"' + str(newExpProg) + '\"} } }'
			ret = thetaWebApiExec('POST', urlCmdExe, jsonSetExpProg)
			#jsonRet = json.loads(ret)
			#print(json.dumps(jsonRet, indent=4))
			
		else :
			if setExpProg == '' :
				index = curExpProg
			else :
				if setExpProg in EXP_PROG_CMD :
					index = EXP_PROG_CMD.index(setExpProg)
				else :
					index = -1;
			
			if index != -1 :
				jsonSetExpProg = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"exposureProgram\":\"' + str(index) + '\"} } }'
				ret = thetaWebApiExec('POST', urlCmdExe, jsonSetExpProg)
				#jsonRet = json.loads(ret)
				#print(json.dumps(jsonRet, indent=4))
			else :
				strResult='ParamERR'
		
	else :
		strResult='BUSY'
	
	return strResult


def changeEv(setEv):
	strResult = ''
	
	if not checkBusy() :
		
		jsonGetCurInfo = '{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\": [\"exposureCompensation\", \"exposureCompensationSupport\", \"exposureProgram\"] } }'
		ret = thetaWebApiExec('POST', urlCmdExe, jsonGetCurInfo)
		jsonRet = json.loads(ret)
		#print(json.dumps(jsonRet, indent=4))
		curExpProg = jsonRet['results']['options']['exposureProgram']
		curExpComp = jsonRet['results']['options']['exposureCompensation']
		expCompSupport = jsonRet['results']['options']['exposureCompensationSupport']
		
		
		if curExpProg != 1 : #not MANUAL
			
			if setEv==MINUS or setEv==PLUS :
				index = expCompSupport.index(curExpComp)
				
				nextPos=0
				if setEv==PLUS :
					nextPos = index + 1
					if nextPos >= len(expCompSupport) :
						nextPos = len(expCompSupport) -  1
				else :
					nextPos = index - 1
					if nextPos < 0 :
						nextPos = 0
				
				newEv = expCompSupport[nextPos]
				
				jsonSetEv = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"exposureCompensation\":\"' + str(newEv) + '\"} } }'
				ret = thetaWebApiExec('POST', urlCmdExe, jsonSetEv)
				#jsonRet = json.loads(ret)
				#print(json.dumps(jsonRet, indent=4))
				
			else :
				if setEv == '' :
					index = expCompSupport.index(curExpComp)
				else :
					index = -1
					for i, chkEv in enumerate(expCompSupport) :
						if setEv == str(chkEv) :
							index=i
							break
					
				if index != -1 :
					newEv = expCompSupport[index]
					jsonSetEv = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"exposureCompensation\":\"' + str(newEv) + '\"} } }'
					ret = thetaWebApiExec('POST', urlCmdExe, jsonSetEv)
					#jsonRet = json.loads(ret)
					#print(json.dumps(jsonRet, indent=4))
					
				else :
					strResult='ParamERR'
			
		else :
			strResult='Can\'tSET'
		
	else :
		strResult='BUSY'
	
	return strResult


def changeIso(setIso):
	strResult = ''
	
	if not checkBusy() :
		
		jsonGetCurInfo = '{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\": [\"iso\", \"isoSupport\"] } }'
		ret = thetaWebApiExec('POST', urlCmdExe, jsonGetCurInfo)
		jsonRet = json.loads(ret)
		#print(json.dumps(jsonRet, indent=4))
		curIso = jsonRet['results']['options']['iso']
		isoSupport = jsonRet['results']['options']['isoSupport']
		
		
		if setIso==MINUS or setIso==PLUS :
			index = isoSupport.index(curIso)
			
			nextPos=0
			if setIso==PLUS :
				nextPos = index + 1
				if nextPos >= len(isoSupport) :
					nextPos = len(isoSupport) -  1
			else :
				nextPos = index - 1
				if nextPos < 0 :
					nextPos = 0
			
			newIso = isoSupport[nextPos]
			
			jsonSetIso = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"iso\":\"' + str(newIso) + '\"} } }'
			ret = thetaWebApiExec('POST', urlCmdExe, jsonSetIso)
			#jsonRet = json.loads(ret)
			#print(json.dumps(jsonRet, indent=4))
			
		else :
			if setIso == '' :
				index = isoSupport.index(curIso)
			else :
				index = -1
				for i, chkIso in enumerate(isoSupport) :
					if setIso == str(chkIso) :
						index=i
						break
				
				if index != -1 :
					newIso = isoSupport[index]
					jsonSetIso = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"iso\":\"' + str(newIso) + '\"} } }'
					ret = thetaWebApiExec('POST', urlCmdExe, jsonSetIso)
					#jsonRet = json.loads(ret)
					#print(json.dumps(jsonRet, indent=4))
					
				else :
					strResult='ParamERR'
		
	else :
		strResult='BUSY'
	
	return strResult


def changeShutterSpeed(setSs):
	strResult = ''
	
	if not checkBusy() :
		
		jsonGetCurInfo = '{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\": [\"shutterSpeed\", \"shutterSpeedSupport\"] } }'
		ret = thetaWebApiExec('POST', urlCmdExe, jsonGetCurInfo)
		jsonRet = json.loads(ret)
		#print(json.dumps(jsonRet, indent=4))
		curSs = jsonRet['results']['options']['shutterSpeed']
		ssSupport = jsonRet['results']['options']['shutterSpeedSupport']
		
		
		if setSs==MINUS or setSs==PLUS :
			index = ssSupport.index(curSs)
			
			nextPos=0
			if setSs==PLUS :
				nextPos = index + 1
				if nextPos >= len(ssSupport) :
					nextPos = len(ssSupport) -  1
			else :
				nextPos = index - 1
				if nextPos < 0 :
					nextPos = 0
			
			newSs = ssSupport[nextPos]
			
			jsonSetSs = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"shutterSpeed\":\"' + str(newSs) + '\"} } }'
			ret = thetaWebApiExec('POST', urlCmdExe, jsonSetSs)
			#jsonRet = json.loads(ret)
			#print(json.dumps(jsonRet, indent=4))
			
		else :
			if setSs == '' :
				index = ssSupport.index(curSs)
			else :
				index = -1
				for i, chkSs in enumerate(ssSupport) :
					if setSs == str(chkSs) :
						index=i
						break
				
				if index != -1 :
					newSs = ssSupport[index]
					jsonSetSs = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"shutterSpeed\":\"' + str(newSs) + '\"} } }'
					ret = thetaWebApiExec('POST', urlCmdExe, jsonSetSs)
					#jsonRet = json.loads(ret)
					#print(json.dumps(jsonRet, indent=4))
					
				else :
					strResult='ParamERR'
		
	else :
		strResult='BUSY'
	
	return strResult


def changeAperture(setAv):
	strResult = ''
	
	if not checkBusy() :
		
		jsonGetCurInfo = '{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\": [\"aperture\", \"apertureSupport\"] } }'
		ret = thetaWebApiExec('POST', urlCmdExe, jsonGetCurInfo)
		jsonRet = json.loads(ret)
		#print(json.dumps(jsonRet, indent=4))
		curAv = jsonRet['results']['options']['aperture']
		avSupport = jsonRet['results']['options']['apertureSupport']
		
		if setAv==MINUS or setAv==PLUS :
			index = avSupport.index(curAv)
			
			nextPos=0
			if setAv==PLUS :
				nextPos = index + 1
				if nextPos >= len(avSupport) :
					nextPos = len(avSupport) -  1
			else :
				nextPos = index - 1
				if nextPos < 0 :
					nextPos = 0
			
			newAv = avSupport[nextPos]
			
			jsonSetAv = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"aperture\":\"' + str(newAv) + '\"} } }'
			ret = thetaWebApiExec('POST', urlCmdExe, jsonSetAv)
			#jsonRet = json.loads(ret)
			#print(json.dumps(jsonRet, indent=4))
			
		else :
			if setAv == '' :
				index = avSupport.index(curAv)
			else :
				index = -1
				for i, chkAv in enumerate(avSupport) :
					if setAv == str(chkAv) :
						index=i
						break
				
				if index != -1 :
					newAv = avSupport[index]
					jsonSetAv = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"aperture\":\"' + str(newAv) + '\"} } }'
					ret = thetaWebApiExec('POST', urlCmdExe, jsonSetAv)
					#jsonRet = json.loads(ret)
					#print(json.dumps(jsonRet, indent=4))
					
				else :
					strResult='ParamERR'
		
	else :
		strResult='BUSY'
	
	return strResult


def changeWB(setWB, setCT):
	strResult = ''
	
	if not checkBusy() :
		
		jsonGetCurInfo = '{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\": [\"whiteBalance\", \"whiteBalanceSupport\", \"_colorTemperature\", \"_colorTemperatureSupport\"] } }'
		ret = thetaWebApiExec('POST', urlCmdExe, jsonGetCurInfo)
		jsonRet = json.loads(ret)
		#print(json.dumps(jsonRet, indent=4))
		curWB = jsonRet['results']['options']['whiteBalance']
		wbSupport = jsonRet['results']['options']['whiteBalanceSupport']
		
		curCT = jsonRet['results']['options']['_colorTemperature']
		ctMax = jsonRet['results']['options']['_colorTemperatureSupport']['maxTemperature']
		ctMin = jsonRet['results']['options']['_colorTemperatureSupport']['minTemperature']
		ctStep = jsonRet['results']['options']['_colorTemperatureSupport']['stepSize']
		
		
		if setWB == '' :
			setWB = curWB
			setCT = str(curCT)
		
		if setWB == WB_CT or ( curWB == WB_CT and ( setWB == PLUS or setWB == MINUS ) ) :
			#---- Set Color Temperature ----
			
			if setCT == PLUS or setCT == MINUS or ( curWB == WB_CT and ( setWB == PLUS or setWB == MINUS ) ) :
				#-- CT +/- --
				
				newCT = curCT
				if setCT == PLUS or setWB == PLUS :
					newCT += ctStep
					if newCT > ctMax :
						newCT = ctMax
				else :
					newCT -= ctStep
					if newCT < ctMin :
						newCT = ctMin
				
				jsonSetCT = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"whiteBalance\":\"_colorTemperature\", \"_colorTemperature\":\"' + str(newCT) + '\"} } }'
				ret = thetaWebApiExec('POST', urlCmdExe, jsonSetCT)
				#jsonRet = json.loads(ret)
				#print(json.dumps(jsonRet, indent=4))
				
			else :
				#-- set CT --
				
				if setCT == '' :
					newCT = curCT
				else :
					newCT = int(setCT)
				
				chkFlag = False
				for chkCT in range(ctMin, ctMax+ctStep, ctStep) : # ctMin <= chkCT < ctMax+ctStep
					if chkCT == newCT :
						chkFlag = True
						break
				
				if chkFlag :
					jsonSetCT = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"whiteBalance\":\"_colorTemperature\", \"_colorTemperature\":\"' + str(newCT) + '\"} } }'
					ret = thetaWebApiExec('POST', urlCmdExe, jsonSetCT)
					#jsonRet = json.loads(ret)
					#print(json.dumps(jsonRet, indent=4))
				else :
					strResult = 'ParamERR'
			
		else :
			#---- Set preset WB ----
			
			if setWB == PLUS or setWB == MINUS :
				#-- WB +/- --
				
				index = wbSupport.index(curWB)
				
				if setWB == PLUS :
					index += 1
					if index > (len(wbSupport) - 2) : # Excluding _colorTemperature
						index = 0
				else :
					index -= 1
					if index < 0 :
						index = len(wbSupport) - 2  # Excluding _colorTemperature
				
				newWB = wbSupport[index]
				jsonSetWB = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"whiteBalance\":\"' + newWB + '\"} } }'
				ret = thetaWebApiExec('POST', urlCmdExe, jsonSetWB)
				#jsonRet = json.loads(ret)
				#print(json.dumps(jsonRet, indent=4))
				
			else :
				#-- set WB --
				if setWB in wbSupport :
					jsonSetWB = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"whiteBalance\":\"' + setWB + '\"} } }'
					ret = thetaWebApiExec('POST', urlCmdExe, jsonSetWB)
					#jsonRet = json.loads(ret)
					#print(json.dumps(jsonRet, indent=4))
				else :
					strResult = 'ParamERR'
		
	else :
		strResult='BUSY'
	
	return strResult


def changeExposureDelay(setExposureDelay):
	strResult = ''
	
	if not checkBusy() :
		
		if setExposureDelay == EXPOSURE_DELAY_CUR or setExposureDelay == EXPOSURE_DELAY_TGGLE :
			jsonGetCurInfo = '{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\": [\"exposureDelay\", \"_latestEnabledExposureDelayTime\"] } }'
			ret = thetaWebApiExec('POST', urlCmdExe, jsonGetCurInfo)
			jsonRet = json.loads(ret)
			#print(json.dumps(jsonRet, indent=4))
			curExposureDelay = jsonRet['results']['options']['exposureDelay']
			latestEnabledExposureDelayTime = jsonRet['results']['options']['_latestEnabledExposureDelayTime']
			
			if   setExposureDelay == EXPOSURE_DELAY_CUR :
				setExposureDelay = curExposureDelay
			elif setExposureDelay == EXPOSURE_DELAY_TGGLE :
				if curExposureDelay == EXPOSURE_DELAY_OFF :
					setExposureDelay = latestEnabledExposureDelayTime
				else :
					setExposureDelay = EXPOSURE_DELAY_OFF
		
		jsonSetExpDelay = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"exposureDelay\":\"' + str(setExposureDelay) + '\"} } }'
		ret = thetaWebApiExec('POST', urlCmdExe, jsonSetExpDelay)
		#jsonRet = json.loads(ret)
		#print(json.dumps(jsonRet, indent=4))
		
	else :
		strResult='BUSY'
	
	return strResult


def changeVolume(setVol):
	strResult = ''
	
	if not checkBusy() :
		
		jsonGetCurInfo = '{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\":[\"_shutterVolume\", \"_shutterVolumeSupport\"] } }'
		ret = thetaWebApiExec('POST', urlCmdExe, jsonGetCurInfo)
		jsonRet = json.loads(ret)
		#print(json.dumps(jsonRet, indent=4))
		curVol = jsonRet['results']['options']['_shutterVolume']
		volMin = jsonRet['results']['options']['_shutterVolumeSupport']['minShutterVolume']
		volMax = jsonRet['results']['options']['_shutterVolumeSupport']['maxShutterVolume']
		
		if setVol == '' :
			strResult='vol ' + str(curVol)
		else :
			try:
				newVol = int(setVol)
				if newVol < volMin :
					newVol = volMin
				if newVol > volMax :
					newVol = volMax
				
				jsonSetExpDelay = '{\"name\": \"camera.setOptions\", \"parameters\": { \"options\":{\"_shutterVolume\":' + str(newVol) + '} } }'
				ret = thetaWebApiExec('POST', urlCmdExe, jsonSetExpDelay)
				#jsonRet = json.loads(ret)
				#print(json.dumps(jsonRet, indent=4))
				
				strResult='vol ' + str(newVol)
			except ValueError:
				strResult='ParamERR'
		
	else :
		strResult='BUSY'
	
	return strResult


def changeTimeShift(setVal):
	global bTimeShift
	strResult = ''
	
	if setVal == '' :
		strResult = '' #NOP
	elif setVal == 'on' :
		bTimeShift = True
	elif setVal == 'off' :
		bTimeShift = False
	else :
		strResult = 'ParamERR'
	
	return strResult


def getCameraStatus(bTimeShift):
	strResult = ''
	
	jsonGetOptions ='{\"name\": \"camera.getOptions\", \"parameters\": { \"optionNames\":[\"captureMode\", \"exposureProgram\", \"aperture\", \"shutterSpeed\", \"iso\", \"exposureCompensation\", \"whiteBalance\", \"_colorTemperature\", \"exposureDelay\"] } }'
	ret = thetaWebApiExec('POST', urlCmdExe, jsonGetOptions)
	jsonRet = json.loads(ret)
	#print(json.dumps(jsonRet, indent=4))
	
	captureMode = jsonRet['results']['options']['captureMode']
	exposureProgram = jsonRet['results']['options']['exposureProgram']
	aperture = jsonRet['results']['options']['aperture']
	iso = jsonRet['results']['options']['iso']
	shutterSpeed = jsonRet['results']['options']['shutterSpeed']
	exposureCompensation = jsonRet['results']['options']['exposureCompensation']
	exposureDelay = jsonRet['results']['options']['exposureDelay']
	presetWb = jsonRet['results']['options']['whiteBalance']
	colorTemperature = jsonRet['results']['options']['_colorTemperature']
	
	
	if shutterSpeed == 0 :
		strSs ='------'
	elif shutterSpeed < 1.0 :
		denominator = 1.0 / shutterSpeed
		strSs = '1/'
		if shutterSpeed==0.4 or shutterSpeed==0.625 or shutterSpeed==0.76923076 :
			strSs += '{0:1.1f}'.format(denominator)
		else :
			strSs += '{0:1.0f}'.format(denominator)
	else :
		strSs = ''
		if shutterSpeed==1.3 or shutterSpeed==1.6 or shutterSpeed==2.5 or shutterSpeed==3.2 :
			strSs += '{0:1.1f}'.format(shutterSpeed)
		else :
			strSs += '{0:2.0f}'.format(shutterSpeed)
		strSs += '\"'
	
	if presetWb == '_colorTemperature' :
		wb = str(colorTemperature) + 'K'
	else :
		wb = presetWb
	
	
	if captureMode == CAPMODE_IMAGE : #MANU
		strResult = 'i-'
	else :
		strResult = 'm-'
	
	strResult +=  EXP_PROG[exposureProgram] + ' '
	
	if   exposureProgram == 1 : #MANU
		strResult += 'F' + str(aperture) + ' ss' + strSs + ' iso' + str(iso) + ' ' + wb
	elif exposureProgram == 2 : #AUTO
		strResult += str(exposureCompensation) + 'ev ' + wb
	elif exposureProgram == 3 : #Av
		strResult += str(exposureCompensation) + 'ev F' + str(aperture) + ' ' + wb
	elif exposureProgram == 4 : #Tv
		strResult += str(exposureCompensation) + 'ev ss' + strSs + ' ' + wb
	elif exposureProgram == 9 : #ISO
		strResult += str(exposureCompensation) + 'ev iso' + str(iso) + ' ' + wb
	
	if bTimeShift :
		strResult += ' ts'
	
	if exposureDelay != 0 :
		strResult += ' timer' + str(exposureDelay)
	
	return strResult


def parseCmd(keyInStr):
	ret = ''
	
	if not keyInStr == '' :
		
		cmd = keyInStr.split()
		if 1 <= len(cmd) and len(cmd) <=2 :
			cmdName = cmd[0]
			if len(cmd) == 1:
				cmdParam = ''
			else :
				cmdParam = cmd[1]
			
			
			if cmdName=='shutter' or  cmdName=='tp':
				shutterButton(bTimeShift)
			elif cmdName=='image' :
				ret = changeCaptureMode(CAPMODE_IMAGE)
			elif cmdName=='movie' :
				ret = changeCaptureMode(CAPMODE_VIDEO)
			
			elif cmdName=='mode' :
				ret = changeExpProg(cmdParam)
			elif cmdName=='ev' :
				ret = changeEv(cmdParam)
			elif cmdName=='ss' :
				if cmdParam in SS_CMD2API :
					ret = changeShutterSpeed( SS_CMD2API.get(cmdParam) )
				else :
					ret = 'ParamERR'
			elif cmdName=='f' :
				ret = changeAperture(cmdParam)
			elif cmdName=='iso' :
				ret = changeIso(cmdParam)
			elif cmdName=='wb' :
				if cmdParam in WB_CMD2API :
					ret = changeWB( WB_CMD2API.get(cmdParam), "" )
				else :
					try:
						setCT = int(cmdParam)
						ret = changeWB( WB_CT, str(setCT) )
					except ValueError:
						ret='ParamERR'
			elif cmdName=='timer' :
				if cmdParam in TIMER_CMD2API :
					ret = changeExposureDelay( TIMER_CMD2API.get(cmdParam) )
				else :
					ret = 'ParamERR'
			elif cmdName=='vol' :
				ret = changeVolume(cmdParam)
			elif cmdName=='ts' :
				ret = changeTimeShift(cmdParam)
			
			else :
				ret = 'UndefCmd'
			
		else :
			ret = 'SplitERR'
		
		if ret=='' :
			ret=getCameraStatus(bTimeShift)
		
		ret+='\n'
	
	return ret


def pyTheta():
	args = sys.argv
	
	if len(args) == 1 :
		prompt = '>> '
		while True:
			keyIn = input(prompt).strip()
			
			if keyIn == 'q' or keyIn == 'quit' or keyIn == 'exit' or keyIn == 'bye' :
				print('#### (^-^)/~ Bye! ####')
				break
			
			print(parseCmd(keyIn), end='')
		
	else :
		keyIn = ''
		for argv in args :
			if argv == args[0] :
				continue
			keyIn += argv + ' '
		
		print(parseCmd(keyIn), end='')

if __name__ == "__main__":
	pyTheta()
