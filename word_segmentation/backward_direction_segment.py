# coding:utf-8
import codecs

def backward_dict(filePath):
    with codecs.open(filePath, 'r', encoding='utf-8') as fr:
        primitiveDict = list(set([term.strip() for term in fr.readlines()]))
    orderdict = {}
    for term in primitiveDict: #构建键为字,值是以字结尾的词的列表这样的字典
        if len(term) > 0:
            word = term[-1] #取该词的尾字
            if word in orderdict.iterkeys():
                orderdict[word].append(term) #如果该字在字典的key中,则将该词添加至对应的value
            else:
                orderdict[word] = [term] #如果不在,增加键值对
    return orderdict

# def backward_max_match(sentence, orderdict):
#     word_segment_result = []
#     position = -1
#     while -position < len(sentence):
#         word = sentence[position]
#         if word in orderdict:
#             max_word_len = 1
#             for option in orderdict[word]:
#                 word_len = len(option)
#                 if sentence[position-word_len+1: position+1] == option and word_len > max_word_len:
#                     max_word_len = word_len
#             if position == -1:
#                 word_segment_result.append(sentence[position - max_word_len + 1:])
#             else:
#                 word_segment_result.append(sentence[position-max_word_len+1: position+1])
#         position -= max_word_len
#     return word_segment_result

# def backward_max_match(sentence, orderdict):
#     word_segment_result = []
#     position = -1
#     while -position < len(sentence):
#         word = sentence[position]
#         max_word_len = 1
#         if word in orderdict:
#             for option in orderdict[word]:
#                 word_len = len(option)
#                 if sentence[position-word_len: position] == option and word_len> max_word_len:
#                     max_word_len = word_len
#         word_segment_result.append(sentence[position-max_word_len: position])
#         position -= max_word_len
#     return word_segment_result

def backward_max_match(sentence, orderdict):
    word_segment_result = []
    position = -1
    while -position < len(sentence):
        max_word_len = 1
        word = sentence[position]
        if position == -1:
            if word in orderdict:
                for option in orderdict[word]:
                    word_len = len(option)
                    if sentence[position-word_len+1:] == option and word_len > max_word_len:
                        max_word_len = word_len
                word_segment_result.append(sentence[position - max_word_len + 1:])
        else:
            if word in orderdict:
                for option in orderdict[word]:
                    word_len = len(option)
                    if sentence[position-word_len+1: position+1] == option and word_len > max_word_len:
                        max_word_len = word_len
                word_segment_result.append(sentence[position-max_word_len+1: position+1])
        position -= max_word_len
    return [word_segment_result[-i] for i in range(1,len(word_segment_result)+1)]

# sentence = u'我们在野生动物园玩'
# # sentence = u'正向最大匹配法和逆向最大匹配法，都有其局限性'
# dictPath = '/Users/lyj/Movies/DataGuru/NLP/icwb2-data/gold/pku_training_words.utf8'
# d_dict = backward_dict(dictPath)
#
# backward_result = backward_max_match(sentence, d_dict)
# for item in backward_result:
#     print item

def main():
    testFilePath = '/Users/lyj/Movies/DataGuru/NLP/icwb2-data/testing/pku_test.utf8'
    resultFilePath = '/Users/lyj/Movies/DataGuru/NLP/icwb2-data/scripts/pku_result.utf8'
    f_dict = backward_dict('/Users/lyj/Movies/DataGuru/NLP/icwb2-data/gold/pku_training_words.utf8')
    with codecs.open(resultFilePath, 'w', encoding='utf-8') as fw:
        with codecs.open(testFilePath, 'r', encoding='utf-8') as fr:
            for sentence in fr.readlines():
                for term in backward_max_match(sentence, f_dict):
                    fw.write(term + ' ')
                fw.write('\n')

if __name__ == "__main__":
    main()