from flask import Flask
from flask import request
import hashlib
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply
import time
import RPi.GPIO as GPIO  # 导入树莓派提供的python模块

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        token = 'Password'  ##注意！！！！！这里要和你公众号的一致

        echostr = request.args.get('echostr')

        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            print('error')

        # if signature == sha1_signature:
        return echostr
    elif request.method == 'POST':
        msg = parse_message(request.get_data())
        if msg.type == 'text':
            print(msg.content)
            if msg.content == "开启":
                openTest()
            if msg.content == "关闭":
                closeTest()
            reply = create_reply('这是条文字消息', msg)
        if msg.type == 'image':
            reply = create_reply('这是条图片消息', msg)
    return reply.render()


def openTest():
    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有数码派通用
    GPIO.setup(21, GPIO.OUT)  # 设置GPIO21为电流输出
    GPIO.output(21, GPIO.HIGH)  # GPIO21 输出3.3V


def closeTest():
    GPIO.cleanup()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0', port=8080, debug=True,
    )
