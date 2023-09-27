from pyfreegpt import Ask

for i in range(1):
    print(
        "\n" * 5,
        f"For .{i}",
        Ask("你可以帮我写代码吗？,使用python编写一个关于{}的程序".format(i), callback=None),
    )


from pyfreegpt import GPT

g = GPT(sessfile="sess2.txt")
for i in range(1):
    print(
        "\n" * 5,
        f"For .{i}",
        g.Ask("你可以帮我写代码吗？,使用python编写一个关于{}的程序".format(i), callback=lambda x: x),
    )
