from djitellopy import Tello
from linebot.models import QuickReplyButton, MessageAction, TextSendMessage, QuickReply

ifconnect = False
me = Tello()


def connect():
    # connect to tello
    me.connect()
    me.for_back_velocity = 0
    me.left_right_velocity = 0
    me.up_down_velocity = 0
    me.yaw_velocity = 0
    me.speed = 0


def show_battery():
    """顯示電量"""
    me.connect()
    global ifconnect
    if not ifconnect:
        try:
            connect()
            ifconnect = True
        except:
            message = 'tello連接失敗'
            return message
    try:
        battery = me.get_battery()
    except:
        message = 'tello連接失敗'
        return message
    return f"電量剩餘:{battery}%"


def check_connectORnot(func):
    def inner():
        global ifconnect
        if not ifconnect:
            return '請先按1連接tello'
        return func()
    return inner


@check_connectORnot
def take_off():
    """起飛"""
    me.takeoff()
    return '成功收到起飛指令,準備起飛'


@check_connectORnot
def land():
    """降落"""
    global ifconnect
    me.land()
    ifconnect = False
    return '成功收到降落指令,準備降落'


@check_connectORnot
def move(mtext):
    if mtext=='前進':
        me.move_forward(30)
        return '成功收到前進指令,準備前進'
    elif mtext=='後退':
        me.move_back(30)
        return '成功收到後退指令,準備後退'
    elif mtext=='左平移':
        me.move_left(30)
        return '成功收到後退指令,準備後退'
    elif mtext=='右平移':
        me.move_right(30)
        return '成功收到向右指令,準備向右'
    elif mtext=='向上':
        me.move_up(50)
        return '成功收到上升指令,準備上升'
    else:
        me.move_down(50)
        return '成功收到下降指令,準備下降'  

    
@check_connectORnot
def flip(mtext):
    if mtext=='前滾翻':
        me.flip_forward()
        return '成功收到向前翻滾指令,準備向前翻滾'
    elif mtext=='後滾翻':
        me.flip_back()
        return '成功收到向後翻滾指令,準備向後翻滾'
    elif mtext=='左滾翻':
        me.flip_left()
        return '成功收到向左指令,準備向左翻滾'
    else:
        me.flip_right()
        return '成功收到向右指令,準備向右翻滾'
    
    
@check_connectORnot
def rotate(mtext):
    if mtext=='向右轉360度':
        me.rotate_clockwise(360)
        return '成功收到向右轉圈指令,準備右轉圈一圈'
    elif mtext=='向右轉180度':
        me.rotate_clockwise(180)
        return '成功收到右轉指令,準備右轉180度'
    elif mtext=='向左轉360度':
        me.rotate_clockwise(-360)
        return '成功收到左轉指令,準備左轉一圈'
    else:
        me.rotate_clockwise(-180)
        return '成功收到向左轉圈指令,準備左轉180度'

    
def Send_Text(event, selections):
    """文字回應"""
    F = quickReply(selections)
    try:
        message = TextSendMessage(
            text='請選擇以下指令',
            quick_reply=F,  # 快速選單
        )
    except:
        message = TextSendMessage(text='發生錯誤')
    return event, message


def quickReply(selections: list):
    """快速選單 使用在TextSendMessage裡的參數quick_reply"""
    items = []  # 最多只能有13個
    for select in selections:
        items.append(
            QuickReplyButton(
                action=MessageAction(
                    label=str(select),
                    text='@' + str(select),
                )
            )
        )
    quick_reply = QuickReply(items=items)
    return quick_reply
