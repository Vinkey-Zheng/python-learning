# -*- coding: utf-8 -*-
import jieba

seg_str = "人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器，该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。"

print("/".join(jieba.lcut(seg_str)))    # 精简模式，返回一个列表类型的结果
print("/".join(jieba.lcut(seg_str, cut_all=True)))      # 全模式，使用 'cut_all=True' 指定
print("/".join(jieba.lcut_for_search(seg_str)))     # 搜索引擎模式
