#  -*- coding:utf-8 -*-

import os
import codecs


def eachFile(filepath):
    pathDir = os.listdir(filepath)#file path为所处理文件所在的文件夹
    each_file = list()
    for allDir in pathDir:#文件夹下的所有文件名
        child = os.path.join('%s/%s' % (filepath, allDir))
        each_file.append(child)#返回该文件夹下所有的路径及其文件名称
    return each_file


def main(ori_road, new_file, new_chinese_file):
    if os.path.exists(new_file):
        os.remove(new_file)
    for one_path in eachFile(ori_road):  # 循环每一个原始文件
        print one_path
        temt_line = list()
        with codecs.open(new_file, "a", "utf-8") as fw, codecs.open(one_path, 'r', "utf-8") as fr:
            for line in fr:
                if line.strip()[-1] == "}":
                    if not temt_line:
                        fw.write(u"{}\r\n".format(line.strip()))
                    else:
                        temt_line.append(line.strip())
                        fw.write(u"{}\r\n".format("".join(temt_line)))
                        temt_line = list()
                else:
                    temt_line.append(line.strip())

    with codecs.open(new_file, "r", "utf-8") as fr, codecs.open(new_chinese_file, 'w', "utf-8") as fw:
        for line in fr:
            try:
                all_message = eval(line.strip()[19:])
                message_time = line.strip()[:19]
                user_id = all_message["fromUserId"]
                target_id = all_message["targetId"]

                chinese_content = ''.join(x for x in line if ord(x) >= 256)
                chinese_content = unicode(chinese_content.strip())
                if chinese_content:
                    fw.write(u"{}\t{}\t{}\t{}\r\n".format(user_id, target_id, message_time, chinese_content))
            except:
                continue


if __name__ == "__main__":
    ori_road = u"C:/..../原始数据2017-06"
    new_file = u"C:/..../2017-06.txt"
    new_chinese_file = u"C:/...../2017-06_chinese.txt"
    main(ori_road, new_file, new_chinese_file)
