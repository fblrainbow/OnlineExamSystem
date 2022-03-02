# -*- coding: utf-8 -*-
"""
Created on 2020年10月26日 20点06分
@author: fanbinglin
"""
#%%导入模块
# from datetime import  datetime,timedelta,time#时间处理函数
import time#时间处理函数
# import pandas as pd
# import numpy as np
import pymysql #mysql操作库
import re
import sys
import os
#%%全局对象

#生产环境mysql配置
mysqlSetting_server={
    'host':"127.0.0.1",
    'port':3306,
    'user':"root", 
    'passwd':"FBLATPX520@", 
    'db':"acp_cc", 
    'charset':'utf8'
}
#本地
mysqlSetting_local={
    'host':"localhost",
    'port':3306,
    'user':"root", 
    'passwd':"FBLATPX520@", 
    'db':"acp_cc", 
    'charset':'utf8'
}

#执行sql语句
def exeSql(mysqlSetting,sql,mode = 0):
    # 打开数据库连接
    db = pymysql.connect(host=mysqlSetting['host'], port=mysqlSetting['port'],user=mysqlSetting['user'], \
        passwd=mysqlSetting['passwd'], db=mysqlSetting['db'], charset=mysqlSetting['charset'] )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    if mode == 0:
        ret = 0
        try:
            cursor.execute(sql)
            ret = cursor.fetchall()
            print(ret)
            db.commit()
        except:
            print(mode,"执行SQL失败")
            db.rollback()
        # 关闭数据库连接
        finally:
            db.commit()
            db.close()
            return ret
    else: #一次执行多条SQL
        for line in sql:
            try:
                cursor.execute(line)
            except:
                print(mode,"执行SQL失败",line)
                db.rollback()
            # 关闭数据库连接
        db.commit()
        db.close()
#DataFrame对象落地数据库
def readFile(fileName):
    with open(fileName,mode='r',encoding='utf8') as fp:
        return fp.read()
def saveFile(fileName,content,code):
    with open(fileName,mode='w',encoding=code) as fp:
        fp.write(content)
if __name__ == "__main__":
    f = readFile('ACP.txt')
    ItemList = [x for x in f.split(r'|') if x]
    print("总长度为:",len(ItemList))
    itemCount = 0
    ItemDict = {}
    realCount = 0
    for index,item in enumerate(ItemList,start=1):
        optionCount = 1
        if int(item[0:4]) != index:
            print(index,'Error' ,item)
            break
        itemElement = [x for x in item.split('\n') if x]
        if itemElement[1][0] != 'A':
            print('A',index,itemElement)
            break
        if itemElement[2][0] != 'B':
            print('B',index,itemElement)
            break
        if itemElement[-1][0:3] != '解析:':
            print('解析',index,itemElement)
            break
        if itemElement[-2][0:3] != '答案:':
            print('答案',index,itemElement)
            break
        if len(itemElement) > itemCount:
            itemCount = len(itemElement)
        elementDict = {}
        if itemElement[0][5] == '单':
            elementType = 'S'
        elif itemElement[0][5] == '多':
            continue
        else:
            print("类型错误！",item)
            break
        elementType = elementType
        elementSubject = itemElement[0][9:]
        elementOptionList = itemElement[1:-2]
        if len(elementOptionList) != 4:
            continue
        resultString = itemElement[-2]
        resultList = re.compile(r'([A-H])\.').findall(resultString)   # 查找数字
        if len(set(resultList)) != len(resultList):
            print("答案有重复",item)
            resultList = sorted(list(set(resultList)))
            print(resultList)
        elementResultList = resultList
        # if len(elementResultList) != int(optionCount):
            # print("答案数量与提示不一致",item,resultList)
        elementDict['title'] = elementSubject
        elementDict['optionList'] = elementOptionList
        elementDict['result'] = elementResultList
        realCount = realCount + 1
        ItemDict[realCount] =  elementDict
    print("======================================================================")
    # exeSql(mysqlSetting_local,"desc acp",mode = 0)
    # exeSql(mysqlSetting_local,"delete from acp",mode = 0)
    print("总长度",len(ItemDict))
    questionSqlList = []
    paper_idSqlList = []
    exeSql(mysqlSetting_local,"delete from paper_pid",mode = 0)
    exeSql(mysqlSetting_local,"delete from question",mode = 0)
    for i in range(1,len(ItemDict)+1,1):
        item = ItemDict[i]
        title = item['title']
        optionA = item['optionList'][0][2:]
        optionB = item['optionList'][1][2:]
        optionC = item['optionList'][2][2:]
        optionD = item['optionList'][3][2:]
        answer = item['result'][0]
        id = i
        sql = f"insert into question(id,subject,title,optionA,optionB,optionC,optionD,answer,level,score) values({id},'ACP云计算','{title}','{optionA}','{optionB}','{optionC}','{optionD}','{answer}',4,1)"
        #print(id,sql)
        questionSqlList.append(sql)
        sql = f"insert into paper_pid(id,paper_id,question_id) values({id},'123456',{id})"
        paper_idSqlList.append(sql)
        #break
    """  local
    exeSql(mysqlSetting_local,questionSqlList,mode = 1)
    exeSql(mysqlSetting_local,paper_idSqlList,mode = 1)
    """
    
    exeSql(mysqlSetting_server,questionSqlList,mode = 1)
    exeSql(mysqlSetting_server,paper_idSqlList,mode = 1)

    
    """
    print("======================================================================")
    sqlList = []
    for i in range(1,len(ItemDict)+1,1):
        itemTmp = ItemDict[i]
        id = i
        url = itemTmp['url']
        topicType = itemTmp['type']
        topicContent = itemTmp['subject']
        optionList = '\n'.join(itemTmp['optionList'])
        solution = ''.join(itemTmp['result'])
        solutionCount = itemTmp['optionCount']
        tips = itemTmp['tip']
        sql = f"insert into acp(id,url,topicType,topicContent,optionList,solution,solutionCount,tips) values({id},'{url}','{topicType}','{topicContent}','{optionList}','{solution}',{solutionCount},'{tips}')"
        sqlList.append(sql)
    exeSql(mysqlSetting_local,sqlList,mode = 1)
    """
        
        
        
        
        
        
        
        