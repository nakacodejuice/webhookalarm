from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from alarm.models import Request
import json
import requests
from django.http import JsonResponse
from RNGWebServEngine.RNGWebServices import RNGConnector
from RNGWebServEngine.Trains import TrainConnector

TokenViber = ''
hosttrain = ''
logintrains=''
passwordtrains=''
hostviber = 'https://chatapi.viber.com'
ImageGIS = 'https://image.ibb.co/nex8se/image.jpg'
ImageKKT = 'https://image.ibb.co/nnnYse/imgonline_com_ua_Resize_Ag83_Qyr0u_Nbzfo_X.jpg'
ImageSMS = 'https://image.ibb.co/n1aKXe/image.jpg'
sender = {'name':'alarmbot','avatar':'https://vignette.wikia.nocookie.net/ru.starwars/images/1/1a/R2d2.jpg/revision/latest/scale-to-width-down/500?cb=20120924084739'}


def index(request):
    return HttpResponse(status=404)

@csrf_exempt
def viber(request):
    try:
        if(request.body.decode("utf-8")!=''):
            p = Request(Messanger='viber', requesttext=request.body.decode("utf-8"))
            p.save()
            received_json_data = json.loads(request.body.decode("utf-8-sig"))
            if(type(received_json_data)==str):
                received_json_data = json.loads(received_json_data)
            if (received_json_data['event'] == 'message'):
                messagestr = received_json_data['message']
                id = str(messagestr['from']['id'])
                Exec(id, messagestr)
    finally:
        return HttpResponse(status=200)

def SendMain(self, id):
    keyboard = Keyboard()
    keyboard.AddButton(2, 2, "Данные по чекам", "small", "center", "bottom", "reply", "Взаиморасчеты", "#f6f7f9",
                           ImageKKT)
    keyboard.AddButton(2, 2, "Показания по смс", "small", "center", "bottom", "reply",
                           "Передать показания счетчика", "#f6f7f9",
                           ImageSMS)
    keyboard.AddButton(2, 2, "ГИС ЖКХ", "small", "center", "bottom", "reply", "Адреса пунктов", "#f6f7f9",
                           ImageGIS)
    SendMessage(id, 'Выберите действие', keyboard.CreateKeyboard())


def SendMessage(self,id, text,keyboard=''):
    message = structSendMessage(id, text,'',keyboard)
    headers = {'content-type': 'application/json'}
    res = requests.post(hostviber + '/pa/send_message', json=message, headers=headers)
    if res.status_code == 200:
        return True
    else:
        return False

def structSendMessage(chat_id = '', text = ' ', type='text',keyboard='',location=''):
    if keyboard=='':
        return {'receiver':chat_id,'min_api_version':1,'sender':sender,'tracking_data':'tracking data','type':type,'text':text}
    elif type=='location':
        return {'receiver': chat_id, 'min_api_version': 1, 'sender': sender, 'tracking_data': 'tracking data',
                'type': type, 'location': location}
    else:
        return {'receiver': chat_id, 'min_api_version': 1, 'sender': sender, 'tracking_data': 'tracking data',
                'type': type, 'text': text, 'keyboard':keyboard}

def Exec(id,message):
    if message == 'ГИС ЖКХ':
        res = GetGISState();
        SendMessage(id, res)
    elif message == 'Показания по смс':
        res = GetSMSState();
        SendMessage(id, res)
    elif message == 'Данные по чекам':
        res = GetKKTState();
        SendMessage(id, res)
    SendMain(id)
def GetGISState(id):
    datajson = ExecInRNG(id, 'Alarm_GetGISState',{'id':id})
    #return 'Все супер'
    data= json.loads(datajson)
    return data['result']

def GetSMSState():
    datajson = ExecInRNG(id, 'Alarm_GetSMSState', {'id': id})
    # return 'Все супер'
    data = json.loads(datajson)
    return data['result']

def GetKKTState():
    datajson = ExecInRNG(id, 'Alarm_GetKKTState', {'id': id})
    # return 'Все супер'
    data = json.loads(datajson)
    return data['result']

def ExecInRNG(self, id, algname, params):
    datameterjson = ''
    try:
        RNG = TrainConnector(hosttrain, logintrains, passwordtrains)
        datameterjson = RNG.Execute(algname, JsonResponse(params, safe=False))
        if (datameterjson == "Error"):
            datameterjson  = {'result':'не отвечает сервис РНГ ЕГС'}
    except:
        datameterjson = {'result': 'Ошибка сервиса РНГ ЕГС'}
    return datameterjson


class Keyboard():
    DefaultHeight = True
    BgColor = "#FFFFFF"
    buttons = []
    def __init__(self,DefaultHeight=True,BgColor="#FFFFFF"):
        self.BgColor = BgColor
        self.DefaultHeight = DefaultHeight

    def AddButton(self,Columns,Rows,Text,TextSize,TextHAlign,TextVAlign,ActionType,ActionBody,BgColor='',Image=""):
        body = {
            "Columns": Columns,
            "Rows": Rows,
            "Text": Text,
            "TextSize": TextSize,
            "TextHAlign": TextHAlign,
            "TextVAlign": TextVAlign,
            "ActionType": ActionType,
            "ActionBody": ActionBody,
            "BgColor": BgColor,
            "Image": Image
        }
        self.buttons.append(body)

    def CreateKeyboard(self):
        return {"Type": "keyboard",
            "BgColor": self.BgColor,
            "DefaultHeight": self.DefaultHeight,
            "Buttons": self.buttons
        }
