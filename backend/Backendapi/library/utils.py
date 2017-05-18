# -*- coding:UTF-8
# 用户点击借这本书以后,生成信息二维码,加密处理还没加上去
import qrcode
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import time
def create_qrcode(id_list,ctime,qrtype):
    """
    :param bid:表示书籍的唯一id,用isbn号码
    :param ctime: 创建时间,一分钟后过期
    :param type: 二维码类型
    :return:
    """
    qr = qrcode.QRCode(
        version =1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    id = ''
    for i in id_list:
        id += 'b'+ str(i)  # 参数最后的样子:id = b1b2b3b56
    url = "http://baidu.com/?ctime="+str(ctime)+"&id="+str(id)+"&qrtype="+qrtype
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    if qrtype == 'borrow':
        filename = 'media_root/borrow_qrcode/'+str(id) + ".png"
        url = '/media/borrow_qrcode/'+str(id) + ".png"
        img.save(filename)
        return url
    elif qrtype == 'return':
        filename = 'media_root/return_qrcode/'+str(id) + ".png"
        url = '/media/return_qrcode/' + str(id) + ".png"
        img.save(filename)
        return url

def create_qrcode_two(id1,id2,ctime,qrtype):
    pass
key = "tangzongyuisgood"
mode = AES.MODE_CBC
# 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
def enpwd(text):
    cryptor = AES.new(key, mode,key)
    # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
    length = 16
    count = len(text)
    add = length - (count % length)
    text = text + ('\0' * add)
    ciphertext = cryptor.encrypt(text)
    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串
    return b2a_hex(ciphertext)

# 解密后，去掉补足的空格用strip() 去掉
def depwd(text):
    cryptor = AES.new(key, mode, key)
    plain_text = cryptor.decrypt(a2b_hex(text))
    return plain_text.rstrip('\0')