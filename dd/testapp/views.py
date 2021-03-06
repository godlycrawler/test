import time
from .servers import add_all_data
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import base64
from datetime import datetime
from Cryptodome.Cipher import AES
# Create your views here.


class Encrypt:
    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')

    def pkcs7padding(self, text):
        """ 明文使用PKCS7填充 """
        bs = 16
        length = len(text)
        bytes_length = len(text.encode('utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding
        self.coding = chr(padding)
        return text + padding_text

    def aes_encrypt(self, content):
        """ AES加密 """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 处理明文
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def aes_decrypt(self, content):
        """AES解密 """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        content = base64.b64decode(content)
        text = cipher.decrypt(content)
        return text.decode('utf-8')


def encode(request):
    if request.method == 'POST':
        dic = {}
        key = 'JXU5NkM2JXU1NkUyJXU4RkQw'
        iv = '1234567812345678'
        # 加密/密文
        code = request.POST.get('data').strip()
        print(code)
        enc = Encrypt(key=key, iv=iv)
        # 解密/明文
        dec = enc.aes_decrypt(code).replace('\\', '')
        now = datetime.now()
        insert_time = now.strftime('%Y-%m-%d %H:%M:%S')
        add_all_data(encode=code, insert_date=insert_time)
        return HttpResponse('success')
    return render(request, 'encode.html')
