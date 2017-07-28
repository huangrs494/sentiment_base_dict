# coding:utf-8

import jieba
import numpy as np
import codecs

jieba.add_word("艾艾贴", 0)  # 实际上这些词，即使分错，对负面的判定也是没有影响的。


# 打开词典文件，返回列表
def open_dict(Dict='hahah', path=r'C:/负面语句判别/program/Textming/Textming/'):
    path = path + '%s.txt' % Dict
    path = path.decode("utf-8")
    dictionary = codecs.open(path, 'r', encoding='utf-8')
    dict = []
    for word in dictionary:
        word = word.strip('\n')
        dict.append(word)
    return dict

# 注意，这里你要修改path路径。
deny_word = open_dict(Dict='否定词', path=r'C:/负面语句判别/program/Textming/')
posdict = open_dict(Dict='positive', path=r'C:/负面语句判别/program/Textming/')
negdict = open_dict(Dict='negative', path=r'C:/负面语句判别/program/Textming/')

degree_word = open_dict(Dict='程度级别词语', path=r'C:/负面语句判别/program/Textming/')
mostdict = degree_word[degree_word.index('extreme') + 1: degree_word.index('very')]  # 权重4，即在情感词前乘以4
verydict = degree_word[degree_word.index('very') + 1: degree_word.index('more')]  # 权重3
moredict = degree_word[degree_word.index('more') + 1: degree_word.index('ish')]  # 权重2
ishdict = degree_word[degree_word.index('ish') + 1: degree_word.index('last')]  # 权重0.5

def judgeodd(num):
    if (num % 2) == 0:
        return 'even'  # 双重否定
    else:
        return 'odd'  # 单重否定


def sentiment_score_list(dataset):
    seg_sentence = dataset.split('。')

    count1 = []
    count2 = []
    for sen in seg_sentence:  # 循环遍历每一个评论
        segtmp = jieba.lcut(sen, cut_all=False)  # 把句子进行分词，以列表的形式返回
        i = 0  # 记录扫描到的词的位置
        a = 0  # 记录情感词的位置
        poscount = 0  # 积极词的第一次分值
        poscount2 = 0  # 积极词反转后的分值
        poscount3 = 0  # 积极词的最后分值（包括叹号的分值）
        negcount = 0
        negcount2 = 0
        negcount3 = 0
        for word in segtmp:
            if word in posdict:  # 判断词语是否是情感词
                poscount += 1
                c = 0
                for w in segtmp[a:i]:  # 扫描情感词前的程度词
                    if w in mostdict:
                        poscount *= 4.0
                    elif w in verydict:
                        poscount *= 3.0
                    elif w in moredict:
                        poscount *= 2.0
                    elif w in ishdict:
                        poscount *= 0.5
                    elif w in deny_word:
                        c += 1
                if judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                    poscount *= -1.0
                    poscount2 += poscount
                    poscount = 0
                    poscount3 = poscount + poscount2 + poscount3
                    poscount2 = 0
                else:
                    poscount3 = poscount + poscount2 + poscount3
                    poscount = 0
                a = i + 1  # 情感词的位置变化

            elif word in negdict:  # 消极情感的分析，与上面一致
                negcount += 1
                d = 0
                for w in segtmp[a:i]:
                    if w in mostdict:
                        negcount *= 4.0
                    elif w in verydict:
                        negcount *= 3.0
                    elif w in moredict:
                        negcount *= 2.0
                    elif w in ishdict:
                        negcount *= 0.5
                    elif w in degree_word:
                        d += 1
                if judgeodd(d) == 'odd':
                    negcount *= -1.0
                    negcount2 += negcount
                    negcount = 0
                    negcount3 = negcount + negcount2 + negcount3
                    negcount2 = 0
                else:
                    negcount3 = negcount + negcount2 + negcount3
                    negcount = 0
                a = i + 1
            elif word == '!':  # 判断句子是否有感叹号  word == '！' or
                for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in posdict or negdict:
                        poscount3 += 2
                        negcount3 += 2
                        break
            i += 1  # 扫描词位置前移

            # 以下是防止出现负数的情况
            pos_count = 0
            neg_count = 0
            if poscount3 < 0 and negcount3 > 0:
                neg_count += negcount3 - poscount3
                pos_count = 0
            elif negcount3 < 0 and poscount3 > 0:
                pos_count = poscount3 - negcount3
                neg_count = 0
            elif poscount3 < 0 and negcount3 < 0:
                neg_count = -poscount3
                pos_count = -negcount3
            else:
                pos_count = poscount3
                neg_count = negcount3

            count1.append([pos_count, neg_count])
        count2.append(count1)
        count1 = []

    return count2


def sentiment_score(senti_score_list):
    score = []
    for review in senti_score_list:
        try:
            score_array = np.array(review)
            Pos = np.sum(score_array[:, 0])
            Neg = np.sum(score_array[:, 1])
            AvgPos = np.mean(score_array[:, 0])
            AvgPos = float('%.1f' % AvgPos)
            AvgNeg = np.mean(score_array[:, 1])
            AvgNeg = float('%.1f' % AvgNeg)
            StdPos = np.std(score_array[:, 0])
            StdPos = float('%.1f' % StdPos)
            StdNeg = np.std(score_array[:, 1])
            StdNeg = float('%.1f' % StdNeg)
            score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
        except IndexError:
            continue
    return score


def test():
    # data = '你就是个王八蛋，混账玩意!你们的手机真不好用！非常生气，我非常郁闷！！！！'
    data2 = '我好开心啊，非常非常非常高兴！今天我得了一百分，我很兴奋开心，愉快，开心'
      result = sentiment_score(sentiment_score_list(data3))
    print result


def main(path, comment_file, neg_file):
    print "数据量一大，这将是漫长的等待。。十几分钟吧。"
    with codecs.open(comment_file, "r", "utf-8") as fr, codecs.open(neg_file, "w", "utf-8") as fw:
        fw.write(u"发送者ID\t相应的消息\r\n")
        for line in fr:
            line1 = line.strip().split("\t")
            try:
                all_result = sentiment_score(sentiment_score_list(line1[2].encode("utf-8")))
                for result in all_result:
                    if result[0] - result[1] < 0:
                        fw.write(u"{}\t{}\r\n".format(line1[0], line1[2]))
            except:
                continue


if __name__ == "__main__":
    global path
    path = r'C:/负面语句判别/program/Textming/'  # 词库的位置
    comment_file = u"C:/负面语句判别/抽取出来的数据/2017-030506_chinese.txt"
    neg_file = u"C:/负面语句判别/抽取出来的数据/2017-030506_chinese_neg.txt"
    main(path, comment_file, neg_file)

