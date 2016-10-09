#coding:utf-8
import codecs
import jieba.posseg as pseg
from collections import Counter
from data_processing.txt_file_processing.basic_nlp_func import sentence_cut

def load_data(file_path):
    sentences = []
    with codecs.open(file_path, 'r', encoding='GBK') as fr:
        for line in fr.readlines():
            line = line.strip()
            if len(line) > 0:
                sentences.append(line)
    title = sentences[0]
    content = sentences[1:]
    return title, content

def get_key_words(title, content, types=['ns', 'nr', 'n', 'v']):
    # 统计词频
    keywords = []  # postagger = Postagger() postagger.load('') title_words = pseg.cut(title)
    for line in content:
        for word, flag in pseg.cut(line):
            if flag in types and len(word)>1:
                keywords.append(word)
    keywords_weights = Counter(keywords)
    # 以句为单位计算inverse sentence frequency
    for word in keywords_weights.keys():
        count = 0
        for line in content:
            if word in line:
                count += 1
        # 如果关键词在标题中出现，则增加权重
        if word in title:
            keywords_weights[word] = keywords_weights[word]*1.5/count
        else:
            keywords_weights[word] = keywords_weights[word]*1.0/count
    return keywords_weights

def get_key_sentences(content_weights, content, p_weight=1.2, s_bias=1, s_weight = 1.2):
    sentences = sentence_cut(content, punctuation_list='!！。')
    for i in range(s_bias):
        content_weights[sentences[i]] = {'weight': 0, 'p_weight': p_weight, 's_weight':s_weight}
        content_weights[sentences[-i-1]] = {'weight': 0, 'p_weight': p_weight, 's_weight': s_weight}
    for sentence in sentences[s_bias:-s_bias]:
        content_weights[sentence] = {'weight': 0, 'p_weight': p_weight, 's_weight':1}
    return content_weights

def compute_sentences_weigths(keywords, paragraphs, p_bias=1, p_weight=1.2, s_bias=1, s_weight = 1.2):
    content_weights = {}
    for i in range(p_bias):
        content_weights = get_key_sentences(content_weights, paragraphs[i], p_weight=p_weight, s_bias=s_bias, s_weight =s_weight)
        content_weights = get_key_sentences(content_weights, paragraphs[-i-1], p_weight=p_weight, s_bias=s_bias, s_weight =s_weight)
    for paragraph in paragraphs[p_bias:-p_bias]:
        content_weights = get_key_sentences(content_weights, paragraph, p_weight=1, s_bias=s_bias, s_weight =s_weight)
    for sentence in content_weights.keys():
        for word in keywords.keys():
            if word in sentence:
                content_weights[sentence]['weight'] += keywords[word]
        inner_num = len(sentence_cut(sentence, punctuation_list=',;，:：；… '))
        content_weights[sentence] = content_weights[sentence]['weight']*\
                                    content_weights[sentence]['p_weight']*content_weights[sentence]['s_weight']/inner_num
    content_weights = sorted(content_weights.iteritems(), key=lambda d: d[1], reverse=True)
    content_weights = [list(result)[0] for result in content_weights]
    return content_weights

def main():
    # 输入压缩比
    ratio = raw_input("Please enter the compressed ratio: ")
    title, paragraghs = load_data("data/01.txt")
    sentences = []

    # 构建文本的句子顺序
    for paragragh in paragraghs:
        sentences.extend(sentence_cut(paragragh, punctuation_list='!！。'))
    sentences_with_indices = dict(zip(sentences, range(len(sentences))))

    # 抽取关键词，并计算句子的权重
    keywords = get_key_words(title, paragraghs)
    key_sentences = compute_sentences_weigths(keywords, paragraghs)

    # 根据压缩比，计算需要抽取多少个句子
    topK = int(len(key_sentences) * float(ratio))
    result_dict = {}
    for sentence in key_sentences[:topK]:
        result_dict[sentence] = sentences_with_indices[sentence]

    # 将抽取出来的句子按原文顺序排好输出
    result_dict = sorted(result_dict.iteritems(), key=lambda d: d[1])
    result_dict = [result[0] for result in result_dict]
    summary = ''.join(result_dict)
    print summary

if __name__=='__main__':
    main()