#coding:utf-8
import codecs

def check_dict(word, filePath):
    with codecs.open(filePath, 'r', encoding='utf-8') as fr:
        primitiveDict = list(set([term.strip() for term in fr.readlines()]))
    if word in primitiveDict:
        print True
    else:
        print False

# 由规则处理的一些特殊符号
numMath = [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9']
numMath_suffix = [u'.', u'%', u'亿', u'万', u'千', u'百', u'十', u'个']
numCn = [u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'〇', u'零']
numCn_suffix_date = [u'年', u'月', u'日']
numCn_suffix_unit = [u'亿', u'万', u'千', u'百', u'十', u'个']
special_char = [u'(', u')']

def proc_num_math(line, start):
    """ 处理句子中出现的数学符号 """
    oldstart = start
    while line[start] in numMath or line[start] in numMath_suffix:
        start = start + 1
    if line[start] in numCn_suffix_date:
        start = start + 1
    return start - oldstart

def proc_num_cn(line, start):
    """ 处理句子中出现的中文数字 """
    oldstart = start
    while line[start] in numCn or line[start] in numCn_suffix_unit:
        start = start + 1
    if line[start] in numCn_suffix_date:
        start = start + 1
    return start - oldstart

def rules(line, start):
    """ 处理特殊规则 """
    if line[start] in numMath:
        return proc_num_math(line, start)
    elif line[start] in numCn:
        return proc_num_cn(line, start)

def forward_dict(filePath):
    with codecs.open(filePath, 'r', encoding='utf-8') as fr:
        primitiveDict = list(set([term.strip() for term in fr.readlines()]))
    orderdict = {}
    for term in primitiveDict: #构建键为字,值是以字开头的词的列表这样的字典
        if len(term) > 0:
            word = term[0] #取该词的首字
            if word in orderdict.iterkeys():
                orderdict[word].append(term) #如果该字在字典的key中,则将该词添加至对应的value
            else:
                orderdict[word] = [term] #如果不在,增加键值对
    return orderdict

def forward_max_match(sentence, orderdict):
    word_segment_result = []
    position = 0
    while position < len(sentence):
        word = sentence[position]
        max_word_len = 1
        if word in numCn or word in numMath:
            max_word_len = rules(sentence, position)
        if word in orderdict:
            for option in orderdict[word]:
                word_len = len(option)
                if sentence[position:position+word_len] == option and word_len > max_word_len:
                    max_word_len = word_len
        word_segment_result.append(sentence[position: position+max_word_len])
        position += max_word_len
    return word_segment_result

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

def backward_max_match(sentence, orderdict):
    word_segment_result = []
    position = -1
    while -position < len(sentence):
        max_word_len = 1
        word = sentence[position]
        if word in numCn or word in numMath:
            max_word_len = rules(sentence, position)
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
    return [word_segment_result[-i] for i in range(1, len(word_segment_result) + 1)]

def main():
    testFilePath = '/Users/lyj/Movies/DataGuru/NLP/icwb2-data/testing/pku_test.utf8'
    resultFilePath = '/Users/lyj/Movies/DataGuru/NLP/icwb2-data/scripts/pku_result.utf8'
    f_dict = forward_dict('/Users/lyj/Movies/DataGuru/NLP/icwb2-data/gold/pku_training_words.utf8')
    b_dict = backward_dict('/Users/lyj/Movies/DataGuru/NLP/icwb2-data/gold/pku_training_words.utf8')
    with codecs.open(resultFilePath, 'w', encoding='utf-8') as fw:
        with codecs.open(testFilePath, 'r', encoding='utf-8') as fr:
            for sentence in fr.readlines():
                if len(forward_max_match(sentence, f_dict)) > len(backward_max_match(sentence, b_dict)):
                    result = backward_max_match(sentence, b_dict)
                    for term in result:
                        fw.write(term + ' ')
                    fw.write('\n')
                else:
                    result = forward_max_match(sentence, f_dict)
                    for term in result:
                        fw.write(term + ' ')

if __name__ == "__main__":
    main()