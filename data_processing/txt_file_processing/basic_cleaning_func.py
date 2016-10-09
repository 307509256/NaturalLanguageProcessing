#coding:utf-8
import re
import jieba
from stp_nlp import stp_seg
from hanziconv import HanziConv

# 繁简转换:把繁体转换为简体
def traditional_to_simplified(ustring):
    return HanziConv.toSimplified(ustring)

# 全角转半角(中文文字永远是全角，只有英文字母、数字键、符号键才有全角半角的概念
# 一个字母或数字占一个汉字的位置叫全角，占半个汉字的位置叫半角。)
def quan_to_ban(ustring):
    banjiao = ''
    for uchar in ustring:
        int_ordinal = ord(uchar)  #the integer ordinal of a one-character string
        if int_ordinal == 12288:
            int_ordinal = 32
        elif (int_ordinal >= 65281) and (int_ordinal <= 65374):
            int_ordinal -= 65248
        banjiao += unichr(int_ordinal)
    return banjiao

# 删除数字/将数字统一转换为1
def number_processing(ustring, str=''):
    if str == '':
        return re.sub('\d+', '', ustring)
    else:
        return re.sub('\d+', '1', ustring)

# 去除特殊字符
def char_filter(ustring):
    special_char = u"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）()——《》<>『』{}「」]"
    return [term for term in ustring if term not in special_char]

# 去除标点符号
def punctuate_filter(ustring):
    punctuation_list = u',.!?;~，。！？；:～… “”‘’'
    return [term for term in ustring if term not in punctuation_list]

# 分词
def word_segmentation(utext, param='jieba'):
    if param == 'stp':
        text = utext.encode('utf-8')
        return [term.decode('utf-8') for term in stp_seg.cut(text)]
    elif param == 'jieba':
        return list(jieba.cut(utext))