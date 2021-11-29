import xlrd
data = xlrd.open_workbook('F:\Python实验\data2.xlsx')
names = data.sheet_names()
table = data.sheet_by_index(0)
table = data.sheet_by_name(names[0])
rowNum = table.nrows
colNum = table.ncols
print(rowNum, colNum)
key_list=list()
depar_list=list()
sum_list=list()
for i in range(1,rowNum):
    for j in range(colNum):
        cell = table.cell(i, j).value
        if(j==0):
            key_list.append(cell)
        elif(j==1):
            depar_list.append(cell)
        else:
            sum_list[i-1]+=cell
c=dict(zip(key_list,sum_list))
print(c)