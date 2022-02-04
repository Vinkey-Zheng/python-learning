def main():
 while True:
     try:
         n = int(input('请输入评委人数：'))
         assert n > 2
         break
     except:
         print('必须输入大于2的整数')


 maxScore, minScore = 0, 100
 total = 0



 for i in range(n):
     while True:
         try:
             score = float(input('请输入第{0}个评委的分数：'.format(i+1)))
             assert 0 <=score<=100
             break
         except:
             print('必须属于0~100的实数.')
     total += score
     if score > maxScore:
         maxScore= score
     if score < minScore:
         minScore = score
 finalScore = round((total-maxScore-minScore)/(n-2), 2)
 formatter = '去掉一个最高分{0}\n去掉以最低分{1}\n最后得分{2}'
 print(formatter.format(maxScore, minScore, finalScore))


main()
