#coding:utf-8

class PCFG(object):
    def __init__(self, non_terminals, terminals, rules, start):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start = start

    def sentence_parse(self, sentence):
        words = sentence.split()
        nums = len(words)
        best_path = [[{} for _ in range(nums)] for _ in range(nums)]

        #初始化:for i in range(len(words)), for X in terminals, PI(i,i,X)=q(X->xi)
        for i in range(nums):  #对句子中的词进行遍历
            for item in self.non_terminals:  #遍历非终结字符
                best_path[i][i][item] = {}  #对ii节点进行构造
                if (words[i],) in self.rules[item].keys():  #如果句子中的第i个词是由某个非终结字符item推导得到的
                    best_path[i][i][item]['prob'] = self.rules[item][(words[i],)] #ii节点存放item,以及该条规则的概率
                    best_path[i][i][item]['path'] = {'split':None, 'rule':words[i]}
                else:
                    best_path[i][i][item]['prob'] = 0
                    best_path[i][i][item]['path'] = {'split': None, 'rule': None}

        #CYK算法的迭代过程
        for l in range(1,nums):
            for i in range(nums-l):  #遍历句子中的所有片段
                j = i +l
                for item in self.non_terminals:  #遍历所有非终结符进行迭代计算
                    tmp_best_path = {'prob':0, 'path':None}
                    for key,value in self.rules[item].iteritems():
                        if key[0] not in self.non_terminals:
                            break
                        for s in range(i,j):
                            tmp_prob = value * best_path[i][s][key[0]]['prob'] * best_path[s + 1][j][key[1]]['prob']
                            if tmp_prob > tmp_best_path['prob']:
                                tmp_best_path['prob'] = tmp_prob
                                tmp_best_path['path'] = {'split':s, 'rule':key}
                    best_path[i][j][item] = tmp_best_path
        self.best_path = best_path

        self._parse_result(0, nums - 1, self.start)
        print "prob = ", self.best_path[0][nums - 1][self.start]['prob']

    def _parse_result(self, left_idx, right_idx, root, ind=0):
        node = self.best_path[left_idx][right_idx][root]
        if node['path']['split'] is not None:
            print '\t' * ind, (root, self.rules[root].get(node['path']['rule']))
            self._parse_result(left_idx, node['path']['split'], node['path']['rule'][0], ind + 1)
            self._parse_result(node['path']['split'] + 1, right_idx, node['path']['rule'][1], ind + 1)
        else:
            print '\t' * ind, (root, self.rules[root].get((node['path']['rule'],))),
            print '--->', node['path']['rule']

def main():
    non_terminals = {'S', 'NP', 'VP', 'PP', 'DT', 'Vi', 'Vt', 'NN', 'IN'}
    start = 'S'
    terminals = {'sleeps', 'saw', 'man', 'woman', 'dog', 'telescope', 'the', 'with', 'in'}
    # rules = {'S':{('NP','VP'): 1.0},
    #          'VP':{('Vi',):0.3, ('Vt','NP'):0.5, ('VP','PP'):0.2},
    #          'NP':{('DT','NN'):0.8, ('NP','PP'):0.2},
    #          'PP':{('IN','NP'):1.0},
    #          'Vi':{('sleeps',):1.0},
    #          'Vt':{('saw',): 1.0},
    #          'NN':{('man',):0.1,('woman',):0.1,('telescope',):0.3,('dog',):0.5},
    #          'DT':{('the',):1.0},
    #          'IN':{('with',):0.6,('in',):0.4}
    #          }
    rules = {'S': {('NP', 'VP'): 1.0},
             'VP': {('Vt', 'NP'): 0.8, ('VP', 'PP'): 0.2},
             'NP': {('DT', 'NN'): 0.8, ('NP', 'PP'): 0.2},
             'PP': {('IN', 'NP'): 1.0},
             'Vi': {('sleeps',): 1.0},
             'Vt': {('saw',): 1.0},
             'NN': {('man',): 0.1, ('woman',): 0.1, ('telescope',): 0.3, ('dog',): 0.5},
             'DT': {('the',): 1.0},
             'IN': {('with',): 0.6, ('in',): 0.4},
             }
    sequence = 'the man saw the dog with the telescope'
    pcfg = PCFG(non_terminals, terminals, rules, start)
    pcfg.sentence_parse(sequence)

if __name__ == "__main__":
    main()