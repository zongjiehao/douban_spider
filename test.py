# encoding:utf-8
# author:haozj 
# create_time: 2019/6/30

import re
text = '+0731-8888888'
res = re.match('[\d\-]+',text)
print(res.group())
