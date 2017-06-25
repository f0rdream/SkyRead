# coding:utf-8
import  qrcode
def create_qrcode(isbn13,id,title):
    """
    生成借书二维码
    :param isbn13:
    :param id:
    :param title:
    :return:
    """
    qr = qrcode.QRCode(
        version =1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data ="isbn13=%s&id=%s&title=%s" % (isbn13,id,title)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    filename = 'add_to_borrow_qrcode/%s--%s.png' % (isbn13,title)
    img.save(filename)

create_qrcode('9787111187776','554939','算法导论（原书第2版）')