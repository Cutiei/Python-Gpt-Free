from pyfreegpt import Ask
for i in range(100):
        print("\n"*5,f"For .{i}",Ask("你可以帮我写代码吗？,使用python编写一个关于{}的程序".format(i),callback=None))
