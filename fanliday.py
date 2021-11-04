import re
import sys
import os
import datetime


mdpath = "/home/slain/文档/dayliplan/plan.md" #md文档存放路径
tasklist = []
workpath = os.getcwd()

def mdexist():
    if os.path.exists(mdpath):
        pass
    else:
        print("md文件不存在")
        planner = open(mdpath,"x")
        planner.close()
        print("md新建成功")


def matcher(arg):
    planner = open(mdpath,"r")
    for line in planner:
        if re.match("# " + arg,line):
            return True


def reader(args):
    global tasklist
    global date
    planner = open(mdpath,"r")
    for line in planner:
         if re.match("# "+args,line):
            print(line)
            date = line
            while True:
                try:
                    global tasklist
                    textline = next(planner)
                    if re.match(r'-\s',textline):
                        tasklist.append(textline)
                    else:
                        break
                except StopIteration:
                    break
            break
    planner.close()

def blockwriter(arg):
    planner = open(mdpath,"r+")
    old = planner.read()
    planner.seek(0)
    for i in arg:
        planner.write(i+"\n")
    planner.write(old)


def linewriter(arg,args):
    if args == 'today':
        planner = open(mdpath,"r+")
        pltext = planner.read().split("\n")
        planner.seek(0)
        for i in arg:
            for k in pltext:
                if re.match("# "+today,k):
                    target = pltext.index(k)
                    pltext.insert(target+1,i)
        for n in pltext:
            planner.write(n+"\n")
    if args == 'tomorrow':
        planner = open(mdpath,"+")
        pltext = planner.read().split("\n")
        planner.seek(0)
        for i in arg:
            for k in pltext:
                if re.match("# "+tomorrow,k):
                    target = pltext.index(k)
                    pltext.insert(target+1,i)
                else:
                    continue
        for n in pltext:
            planner.write(n+"\n")
    planner.close()


def timer():
    global today
    global yesterday
    global tomorrow
    today=datetime.date.today().strftime('%Y-%m-%d')
    yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    tomorrow = (datetime.date.today() + datetime.timedelta(days=+1)).strftime('%Y-%m-%d')


def signer():
    reader(today)
    for i in tasklist:
        print(str(tasklist.index(i)+1)+'.'+i[2:])
    print("今日事毕几何？")
    t = input().split(" ")
    print(t)
    planner = open(mdpath,"r")
    pltext = planner.read().split("\n")
    for m in t:
        for n in pltext:
            if n+'\n' == tasklist[int(m)-1]:
                print("毕")
                pltext[pltext.index(n)] = pltext[pltext.index(n)] + "   --此事已成"
                break
    planner.close()
    planner = open(mdpath,"r+")
    planner.seek(0)
    for x in pltext:
        planner.write(x+"\n")



def main(arg):
    mdexist()
    timer()
    try:
        argv = sys.argv[1]
        if argv == '-v' or argv == '-v today':
            reader(today)
            if matcher(today):
                for i in tasklist:
                    print(i)
            else:
                print("今日无事可做。")
        if argv == '-vt':
            reader(tomorrow)
            if matcher(tomorrow):
                print("明日仍旧迷茫。")
            else:
                for i in tasklist:
                    print(i)
        if argv == '-s':
            signer()
            print("规明日之事否？(y/n)")
            i = input()
            if i == "y":
                os.system("python3 {} -wf".format(workpath+"/fanliday.py"))
            elif i == "n":
                print("息")
            else:
                pass
        if argv == '-wt':
            if matcher(today):
                print("今天已经有计划了，是否要继续添加？(y/n)")
                i = input()
                if i == "y":
                    list = []
                    print("续写今日之事：")
                    while True:
                        inputtext = input()
                        if inputtext == "exit":
                            break
                        else:
                            list.append("- " + inputtext)
                    linewriter(list,"today")
            else:
                list = ["# " + today]
                print("写今日之事：")
                while True:
                    inputtext = input()
                    if inputtext == "exit":
                        break
                    else:
                        list.append("- " + inputtext)
                print(list)
                blockwriter(list)
        if argv == '-wf':
            if matcher(tomorrow):
                print("明天已经有计划了，是否要继续添加？(y/n)")
                i = input()
                if i == "y":
                    list = []
                    print("续写明日之事：")
                    while True:
                        inputtext = input()
                        if inputtext == "exit":
                            break
                        else:
                            list.append("- " + inputtext)
                    linewriter(list,"tomorrow")
            else:
                list = ["# " + tomorrow]
                print("写明日之事：")
                while True:
                    inputtext = input()
                    if inputtext == "exit":
                        break
                    else:
                        list.append("- " + inputtext)
                print(list)
                blockwriter(list)
        if argv == '--help':
            print("-s for sign task today.\n")
            print("-f for task list today.\n")
            print("-v for view task today.\n")
            print("-wt for write task today.\n")
            print("-wf for write task tomorrow.\n")
    except IndexError:
        print("You have input no option,--help for more information.")

if __name__ == '__main__':
    main(sys.argv)
