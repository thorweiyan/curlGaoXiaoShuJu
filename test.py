# -*- coding: utf-8 -*-
import sqlite3
# import unicode
import sys

conn = sqlite3.connect('test.db')
conn.text_factory=str
c = conn.cursor()
c.execute("SELECT *  from 测试双一流")

for row in c:
   print("ID = ", row[0])
   print("NAME = ", str(row[1]).encode('utf-8'))
   print("ADDRESS = ", str(row[2]).encode('gbk'))
   print("SALARY = ", row[3], "\n")

conn.close()