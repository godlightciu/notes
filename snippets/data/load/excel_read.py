import pandas as pd
import matplotlib.pyplot as plt

info = pd.read_excel('sample.xlsx',sheetname='Sheet1')
info.columns = ['年级','学号','民族','姓名','性别','学院','系所','校区','出生日期','生源地']
print(info['姓名'])