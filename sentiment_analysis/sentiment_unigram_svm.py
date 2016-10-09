#coding:utf-8
import re
import jieba
from operator import add
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.mllib.classification import SVMWithSGD
from pyspark.mllib.regression import LabeledPoint

def punctuate_filter(text):
    return ''.join(re.findall(u'[\u4e00-\u9fa5|a-z|A-Z|\d|\s]+', text))

def make_vector(line, lst):
    vector = []
    for term in lst:
        if term in line:
            vector.append(1)
        else:
            vector.append(0)
    return vector

def make_label(score):
    if score > 3:
        return 1.0
    else:
        return 0.0

def main():
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.appName('sentiment analysis').config(conf=conf).getOrCreate()
    positive_df = spark.read.csv('好评.csv', header=True)
    negative_df = spark.read.csv('差评.csv', header=True)

    rdd = positive_df.union(negative_df).select('comment').rdd\
                     .map(lambda line: list(line)[0])\
                     .map(lambda line: punctuate_filter(' '.join(jieba.cut(line))))
    rdd_score = positive_df.union(negative_df).select('score').rdd\
                     .map(lambda line: list(line)[0][-1])\
                    .map(lambda score: make_label(score)).collect()

    # filter_words = rdd.flatMap(lambda line: line.split(' ')).filter(lambda word: word != ' ')\
    #                   .map(lambda word: (word, 1)).reduceByKey(add).map(list)\
    #                   .filter(lambda pair: pair[1]>3)\
    #                   .map(lambda pair: [pair[1], pair[0]]).sortByKey(False)\
    #                   .map(lambda word: word[1]).collect()
    filter_words = rdd.flatMap(lambda line: line.split(' ')).filter(lambda word: len(word)>1)\
                        .map(lambda word: (word, 1)).reduceByKey(add).map(list) \
                        .filter(lambda pair: pair[1] > 3)\
                        .map(lambda pair: [pair[1], pair[0]]).sortByKey(False)\
                        .map(lambda word: word[1]).collect()
    text_vectors = rdd.map(lambda line: line.split(' ')).map(lambda line: make_vector(line, filter_words)).collect()

    data = sc.parallelize([LabeledPoint(rdd_score[i], text_vectors[i]) for i in range(len(rdd_score))])
    splits = data.randomSplit([0.6, 0.4], 1234)
    train = splits[0]
    test = splits[1]

    svm = SVMWithSGD.train(train, iterations=100)
    predictions = test.map(lambda line: [int(line.label), svm.predict(line.features)])
    count = 0
    for pair in predictions.collect():
        if pair[0] == pair[1]:
            count += 1
    accuracy = 1.0*count/predictions.count()
    print accuracy

if __name__=='__main__':
    main()