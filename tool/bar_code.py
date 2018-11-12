# encoding: utf-8

"""
@version: 1.0
@author: WangNing
@license: GUN 
@contact: yogehaoren@gmail.com
@site: 
@software: PyCharm
@file: bar_code.py
@time: 2018/10/25 12:51
@describe: 生成条形码
"""
from pystrich.code39 import Code39Encoder
from online_library.settings import MEDIA_ROOT
import os

class BarCode:
    @staticmethod
    def create_bar_code(bar_num):
        '''
        生成条形码
        :param bar_num :
        :return (失败， 错误信息)|(成功， 信息， 网址， 具体路径):
        '''
        try:
            bar_num = int(bar_num)
        except ValueError:
            return False, '请输入数字!'
        if bar_num > 10**13-1:
            return False, '数字不应大于十三位!'
        path = os.path.join(MEDIA_ROOT, '%d.png' % bar_num)
        if os.path.exists(path):
            return True, 'Exists!', '/media/%d.png' % bar_num, path,
        encoder = Code39Encoder('{:0=13}'.format(bar_num))
        encoder.save(path)
        return True, 'Successful!', '/media/%d.png' % bar_num, path


if __name__ == '__main__':
    # books = Book.objects.all()
    # for book in books:
    #     print(BarCode.create_bar_code(book.isbn))
    print(BarCode.create_bar_code(00000))
