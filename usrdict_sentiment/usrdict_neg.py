# coding:utf-8

import re
import codecs


comment_file = u"C:/..../2017-06_chinese.txt"
neg_file = u"C:/......./chinese_neg_2.txt"
neg_word = u"C:/......../negative_new.txt"

business_negdict = codecs.open(neg_word, "r", "utf-8").read().split()


pattern = "|".join(business_negdict)

with codecs.open(comment_file, "r", "utf-8") as fr, codecs.open(neg_file, "w", "utf-8") as fw:
    fw.write(u"用户ID\t\t接受者ID\t时间\t\t文本内容\r\n")
    for line in fr:
        line2 = line.strip().split("\t")
        label2 = re.findall(pattern, line2[3])
        if label2 and len(line) < 130:
            fw.write(u"{}\r\n".format(line.strip()))
            # fw.write(u"{}\t{}\r\n".format(line2[0], line2[1], line2[2], line2[3]))
