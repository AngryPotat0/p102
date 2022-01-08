from Run import*

run = Runner()
while True:
    text = ""
    file_name = ""
    file_name = input("请输入中间代码文件名，输入exit退出：")
    if(file_name == 'exit'): break
    file = open(file_name)
    while(True):
        line = file.readline()
        text += line
        if(not line):
            break
    file.close()
    ans = run.run(text)
    print(ans['msg'])