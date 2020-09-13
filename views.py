from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import tello_control

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                mtext = event.message.text
                if mtext == '@顯示電量':
                    message = tello_control.show_battery()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

                elif mtext == '@起飛降落':
                    command = ['起飛','降落']
                    event, message = tello_control.Send_Text(event,command)
                    line_bot_api.reply_message(event.reply_token, message)

                elif mtext == '@起飛':
                    message = tello_control.take_off()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@降落':
                    message = tello_control.land()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

                # quick select
                elif mtext == '@移動':
                    command = ['前進','後退','左平移','右平移']
                    event, message = tello_control.Send_Text(event,command)
                    line_bot_api.reply_message(event.reply_token, message)
                elif mtext == '@旋轉':
                    command = ['順時鐘旋轉360','順時鐘旋轉180','逆時針旋轉360','逆時針旋轉180']
                    event, message = tello_control.Send_Text(event, command)
                    line_bot_api.reply_message(event.reply_token, message)
                elif mtext == '@翻滾':
                    command = ['前滾翻','後滾翻','左滾翻','右滾翻']
                    event, message = tello_control.Send_Text(event, command)
                    line_bot_api.reply_message(event.reply_token, message)
                elif mtext == '@升降':
                    command = ['上升','下降']
                    event, message = tello_control.Send_Text(event,command)
                    line_bot_api.reply_message(event.reply_token, message)

                elif mtext == '@前進':
                    message = tello_control.forward()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@後退':
                    message = tello_control.back()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@左平移':
                    message = tello_control.left()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@右平移':
                    message = tello_control.right()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

                elif mtext == '@前滾翻':
                    message = tello_control.flipFoward()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@後滾翻':
                    message = tello_control.flipBack()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@左滾翻':
                    message = tello_control.flipLeft()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@右滾翻':
                    message = tello_control.flipRight()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

                elif mtext == '@上升':
                    message = tello_control.up()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@下降':
                    message = tello_control.down()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

                elif mtext == '@順時鐘旋轉360':
                    message = tello_control.rotate_clockwise_circle()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@逆時針旋轉360':
                    message = tello_control.rotate_unclockwise_circle()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@順時鐘旋轉180':
                    message = tello_control.rotate_clockwise_half_circle()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                elif mtext == '@逆時針旋轉180':
                    message = tello_control.rotate_unclockwise_half_circle()
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))


            return HttpResponse()
    else:
        return HttpResponseBadRequest()
