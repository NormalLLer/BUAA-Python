# -*- coding = utf-8 -*-
# @Time :2022/8/1 8:30
# @Author:banana889
# @File : Module.py
'''
前端调用的主要模块
'''
import datetime
import calendar
import time

from src.backend.importModule import *
from src.backend.importance import Importance
from src.backend.state import State
from src.backend.species import Species
from src.util.tools import *
import pickle as pk

import tinydb
# tinydb 的基本使用方法 ： https://blog.csdn.net/yangzm/article/details/82803746

class Calendar:
    def __init__(self, time,  user):
        self.time = time
        self.user = user
        self.ymStr = self.time.strftime("%Y%m")
        self.monthTodoTable = user.todoDb.table(self.ymStr)
        self.monthTodo = {}
        self.readFromDb()

    def readFromDb(self):
        # 从monthTodoTable中读取，存入 monthtodo中
        for tt in self.monthTodoTable.all():
            task = Task.parseTask(tt)
            day = task.time.day

            if day not in self.monthTodo.keys():
                self.monthTodo[day] = []
            self.monthTodo[day].append(task)

    # # 设置月份，这个影响到日历缩略图
    # def setAnsMonth(self, y, m):
    #     pass

    def getCalendar(self):
        # 二维数组
        MonthCal = calendar.monthcalendar(self.y, self.m)
        return MonthCal

    def getTasksOfMonth(self):
        # 返回一个三维列表，前两个下标和getCalendar对应，第三个下标对应这个日期的任务列表
        pass

    '''
    获取某一天的任务列表
    '''

    def getTasksOfDay(self, date: datetime.datetime):
        # return self.monthTodoTable
        if date.day in self.monthTodo.keys():
            return self.monthTodo[date.day]
        return []

    # datetime.datetime.now()
    def getTasksToday(self):
        pass

    def getTasksPeriod(self, date1, date2):
        pass

    def getTasksTodayAndAfter(self):
        pass

    def addTask(self, task):
        self.monthTodoTable.insert(task.toDict())
        day = task.time.day
        if day not in self.monthTodo.keys():
            self.monthTodo[day] = []
        self.monthTodo[day].append(task)
        debugPrint("add task " + task.title)


class User:
    def __init__(self, name):
        self.name = name
        self.calendarMap = {}
        # 一个月的代办对应一个table
        self.todoDb = db.TinyDB(DATAPATH + name + "/todoDb.json")
        # self.initCalendarMap(
    '''
    获取某个月的日历
    '''
    # def getCalendar(self, yy, mm) -> Calendar:
    #     cal = Calendar(yy, mm, self)
    #     return cal

    # done
    def addTask(self, title: str, content: str, time: datetime.datetime,
                 importance=Importance.normal, state=State.notStarted):
        task = Task(title, content, time, importance, state)
        ymStr = time.strftime("%Y%m")

        if ymStr not in self.calendarMap.keys():
            newCalender = Calendar(time, self)
            self.calendarMap[ymStr] = newCalender
        calendar_ : Calendar = self.calendarMap.get(ymStr)
        calendar_.addTask(task)

    # done
    def getTasksOfDay(self, day : datetime.datetime):
        ymStr = day.strftime("%Y%m")
        if self.todoDb.table(ymStr) != None:
            self.calendarMap[ymStr] = Calendar(day, self)

        if ymStr in self.calendarMap:
            calendar_:Calendar = self.calendarMap.get(ymStr)
            return calendar_.getTasksOfDay(day)
        else:
            return []


class Date:
    def __init__(self, date : datetime.datetime):
        self.yy = date.year
        self.mm = date.month
        self.dd = date.day
        self.taskList = []

    '''
    taskName, taskDescribe, time, importance
    taskDescribe, importance can be None
    '''
    def addTask(self, title, time: datetime.datetime, content="", importance=Importance.normal):
        newTask = Task(title, content, time, importance)
        self.taskList.append(newTask)
        debugPrint("added task : " + title)

    def getTasks(self):
        return self.taskList

# 暂且使用time 分别代表日常任务的起始时间和普通任务的结束时间
class Task:
    def __init__(self, title: str, content: str, time: datetime.datetime,
                 importance=Importance.normal, state=State.notStarted,speices=Species.work):
        self.title = title
        self.content = content
        self.time = time
        self.importance = importance
        self.state = state
        self.species = speices

    @staticmethod
    def parseTask(dict):
        # dict -> Task
        time = datetime.datetime.fromtimestamp(dict["time"])
        task = Task(dict["title"], dict["content"], time, Importance(dict["importance"]),
                    State(dict["state"]), Species(dict["species"]))
        return task

    def toDict(self):
        dict = {"title" : self.title,
                "content" : self.content,
                "time" : self.time.timestamp(),
                "importance" : self.importance.value,
                "state" : self.state.value,
                "species" : self.species.value
                }
        return dict

    def setStart(self):
        self.state = State.inProgress

    def setFinish(self):
        self.state =State.finished

if __name__ == "__main__":
    u = User("ba")
    # u.addTask("qc", "learn qc", datetime.datetime.now())
    task = u.getTasksOfDay(datetime.datetime.now())

    print(u.calendarMap)

    for _ in task:
        print(_.toDict())

    # task.clear()