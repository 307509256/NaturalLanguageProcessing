# coding:utf-8
import jieba
from stp_nlp import stp_seg

# 文本长度小于指定长度的进行丢弃
def text_filter(corpus, length=140):
    return [text for text in corpus if len(text)>length]

# 文本分句
def sentence_cut(text, punctuation_list=',.!?;~，。！？；～… '):
    sentences = []
    sentiment_word_position = 0
    word_position = 0
    punctuation_list = punctuation_list.decode('utf8')
    for words in text:
        word_position += 1
        if words in punctuation_list:
            nextWord = list(text[sentiment_word_position:word_position+1]).pop()
            if nextWord not in punctuation_list:
                sentences.append(text[sentiment_word_position:word_position])
                sentiment_word_position = word_position
    if sentiment_word_position < len(text):
        sentences.append(text[sentiment_word_position:])
    return sentences

# 分词
def word_segment(utext, param='stp', output_param = 'ustring'):
    if param == 'stp':
        text = utext.encode('utf-8')
        if output_param == 'ustring':
            return ' '.join([term.decode('utf-8') for term in stp_seg.cut(text)])
        else:
            return [term.decode('utf-8') for term in stp_seg.cut(text)]
    elif param == 'jieba':
        if output_param == 'ustring':
            return ' '.join(jieba.cut(utext))
        else:
            return list(jieba.cut(utext))