# coding:utf-8
import codecs
import jieba.posseg as pseg
import numpy as np
from data_processing.txt_file_processing.basic_nlp_func import sentence_cut

def get_keywords(sentences, types=['ns', 'nr', 'n', 'v']):
    words = []
    text = []
    for sent in sentences[1:]:
        word = [word for word, flag in pseg.cut(sent) if flag in types and len(word) > 1]
        if len(word) > 2:
            words.append(word)
            text.append(sent)
    return words, text

def construct_matrix(text):
    num = len(text)
    weights = np.zeros((num, num))
    # 计算文本相似度
    for i in range(num):
        for j in range(i,num):
            weights[i, j] = len(set(text[i]) & set(text[j]))/(np.log(len(text[i]))*np.log(len(text[j])))
            weights[j, i] = weights[i, j]
    # 按行归一化
    for i in range(num):
        line_sum = sum(weights[i, :])
        for j in range(num):
            weights[i, j] /= line_sum
    return weights

def textrank(start_tr, iters, d, weights):
    count = 0
    num = weights.shape[0]
    while count<iters:
        start_tr = np.ones((1,num))*(1-d) + d*np.dot(np.mat(start_tr),np.mat(weights))
        count += 1
    return start_tr

def summaly(sentences, weigths, topK):
    # 对句子的权重进行排序，得到用户指定的前topK个权重
    ranks = dict(zip(weigths, range(len(weigths))))
    ranks = [list(rank) for rank in sorted(ranks.iteritems(), key=lambda d: d[0], reverse=True)]
    top_rank = ranks[:topK]
    # 抽取前topK个句子，并根据句子在文本中的顺序从小到大进行排序，然后输出
    summary = dict(zip([sentences[rank[1]] for rank in top_rank], [rank[1] for rank in top_rank]))
    summary = [list(rank)[0] for rank in sorted(summary.iteritems(), key=lambda d: d[1])]
    return ''.join(summary)

def main():
    with codecs.open("data/01.txt", 'r', encoding='GBK') as fr:
        sentences = []
        for line in fr.readlines():
            line = line.strip()
            if line:
                sentences.extend(sentence_cut(line, punctuation_list='。！!'))
    words, text = get_keywords(sentences,['ns', 'nr', 'n'])

    weights = construct_matrix(words)
    num = len(text)
    start_tr = np.ones((1,num))
    d = 0.85
    iters = 100
    tr = textrank(start_tr, iters, d, weights).tolist()[0]

    ratio = float(raw_input("Please enter the compressed ratio: "))
    topK = int(num*ratio)
    summary = summaly(text, tr, topK)
    print summary

if __name__ == '__main__':
    main()
