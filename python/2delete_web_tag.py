#python练习2
#从网页代码中提取正文内容

_encoding='gbk'   #'utf-8'
#提示用户进行输入
s_path = input('文件路径:')

# 打开旧文件
f = open(s_path, 'r', encoding=_encoding)

# 打开新文件
s_path_part = s_path[0: s_path.find('.')]

a_path_new = [s_path_part, '_u.txt'] 
s_path_new = ''.join(a_path_new)
f_u = open(s_path_new, 'w', encoding= _encoding)

a_str_for_del=[
    '/',
    '<em>'
    ]

#导入regex正值表达式
import re

#例子：匹配<!-- 「注释」--> ； 为了防止跨多个注释，中间内容要排除「<!--」出现
p_comment = re.compile(r'<!-- ([^<!--]*) -->')

#例子：匹配<div开头的标识符，比如，<div class="left fl">
p_div = re.compile(r'<div([^<]*)>')

#例子：匹配<ul开头的标识符 比如，<ul class="list-right">
p_ul = re.compile(r'<ul([^<]*)>')

#例子：匹配<li开头的标识符 比如，<li class="list-child-li"> 或者 <li> 
p_li = re.compile(r'<li([^<]*)>')

#例子：匹配<p开头的标识符
p_p = re.compile(r'<p([^<]*)>')

p_h = re.compile(r'<[H|h]([^<]*)>')

a_p =[p_comment, p_div, p_ul, p_li, p_p, p_h]

#for n in range(1, 11):  
#    a_str_for_del.append('%s%s%s' % ('<!-- ', n, ' -->'))

# 循环读取旧文件
for line in f:
    # 进行判断
    for s_str in a_str_for_del:
        if s_str in line:
            line = line.replace(s_str,'')
    for it in a_p:
        line = it.sub(r'',line)
    f_u.write(line)
    #print(line)
    
f.close()
f_u.close()
