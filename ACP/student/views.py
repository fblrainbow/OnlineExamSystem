from django.shortcuts import render, redirect
from student import models


# from django.http import HttpResponse
# from django.contrib.auth import logout


# Create your views here.
def index(request):
    return render(request, 'index.html')


def logout(request):
    return render(request, 'index.html')


def studentLogin(request):
    print("studentLogin")
    if request.method == 'POST':
        # 获取表单信息
        print("Post")
        stuId = request.POST.get('id')
        password = request.POST.get('password')
        print("id", stuId, "password", password)
        # 通过学号获取该学生实体
        try:
            student = models.Student.objects.get(id=stuId)
            print(student)
            if password == student.password:  # 登录成功
                # 查询考试信息
                paper = models.Paper.objects.filter(major=student.major)
                # 查询成绩信息
                grade = models.Grade.objects.filter(sid=student.id)
                # 渲染index模板
                return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade})
            else:
                return render(request, 'index.html', {'message': '密码不正确'})
        except:
            print('没找到id:', stuId)
    else:
        print('点击学生登录')
        return render(request, 'studentLogin.html')


# teacherLogin
def teacherLogin(request):
    print("teacherLogin")
    if request.method == 'POST':
        # 获取表单信息
        print("Post")
        stuId = request.POST.get('id')
        password = request.POST.get('password')
        print("id", stuId, "password", password)
        # 通过学号获取该学生实体
        try:
            teacher = models.Teacher.objects.get(id=stuId)
            print(teacher)
            if password == teacher.password:  # 登录成功
                # 查询考试信息
                print('logon')
                paper = models.Paper.objects.filter(major=teacher.major)
                # 查询成绩信息
                grade = models.Grade.objects.filter(sid=teacher.id)
                # 渲染index模板
                print("1")
                return render(request, 'index.html', {'teacher': teacher, 'paper': paper, 'grade': grade})
            else:
                return render(request, 'index.html', {'message': '密码不正确'})
        except:
            print('没找到id:', stuId)
            return render(request, 'index.html', {'message': stuId + '不存在'})


def studentLogin(request):
    print("studentLogin")
    if request.method == 'POST':
        # 获取表单信息
        print("Post")
        stuId = request.POST.get('id')
        password = request.POST.get('password')
        print("id", stuId, "password", password)
        # 通过学号获取该学生实体
        try:
            student = models.Student.objects.get(id=stuId)
            print(student)
            if password == student.password:  # 登录成功
                # 查询考试信息
                paper = models.Paper.objects.filter(major=student.major)
                # 查询成绩信息
                grade = models.Grade.objects.filter(sid=student.id)
                # 渲染index模板
                return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade})
            else:
                return render(request, 'index.html', {'message': '密码不正确'})
        except:
            print('没找到id:', stuId)
            return render(request, 'index.html', {'message': stuId + '不存在'})


def toExamStart(request):
    print(123)
    return render(request, 'index.html', {'message': '密码不正确'})


def toLibrary(request):
    print("toLibrary")
    return render(request, 'library.html')


def startExam(request):
    print("StartExam")
    sid = request.GET.get('sid')
    subject1 = request.GET.get('subject')
    # 得到学生信息
    student = models.Student.objects.get(id=sid)
    # 试卷信息
    paper = models.Paper.objects.filter(subject=subject1)
    print('学号', sid, '考试科目', subject1, student, paper)

    return render(request, 'exam1.html', {'student': student, 'paper': paper, 'subject': subject1})


def calGrade(request):
    if request.method == 'POST':
        # 得到学号和科目
        sid = request.POST.get('sid')
        subject1 = request.POST.get('subject')

        # 重新生成Student实例，Paper实例，Grade实例，名字和index中for的一致，可重复渲染
        student = models.Student.objects.get(id=sid)
        paper = models.Paper.objects.filter(major=student.major)
        grade = models.Grade.objects.filter(sid=student.id)
        # 计算该门考试的学生成绩
        question = models.Paper.objects.filter(subject=subject1).values("pid").values('pid__id', 'pid__answer',
                                                                                      'pid__score')
        mygrade = 0  # 初始化一个成绩为0
        for p in question[0:60]:
            qId = str(p['pid__id'])  # int 转 string,通过pid找到题号
            myans = request.POST.get(qId)  # 通过 qid 得到学生关于该题的作答
            okans = p['pid__answer']  # 得到正确答案
            print(qId, okans, myans)
            if myans == okans:  # 判断学生作答与正确答案是否一致
                mygrade += p['pid__score']  # 若一致,得到该题的分数,累加 mygrade 变量
        # 向Grade表中插入数据
        models.Grade.objects.create(sid_id=sid, subject=subject1, grade=mygrade)
        # 重新渲染index.html模板
        return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade})


# 教师查看成绩
def showGrade(request):
    subject1 = request.GET.get('subject')
    grade = models.Grade.objects.filter(subject=subject1)
    data1 = models.Grade.objects.filter(subject=subject1, grade__lt=60).count()
    data2 = models.Grade.objects.filter(subject=subject1, grade__gte=60, grade__lt=70).count()
    data3 = models.Grade.objects.filter(subject=subject1, grade__gte=70, grade__lt=80).count()
    data4 = models.Grade.objects.filter(subject=subject1, grade__gte=80, grade__lt=90).count()
    data5 = models.Grade.objects.filter(subject=subject1, grade__gte=90).count()
    data = {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5}
    return render(request, 'showGrade.html', {'grade': grade, 'data': data, 'subject': subject1})
