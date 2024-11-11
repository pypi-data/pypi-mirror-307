import os.path
from fnmatch import fnmatch
import win32com.client as win32


class ExcelHandler:

    def __init__(self, visible=True):
        self.xApp = win32.Dispatch('Excel.Application')
        self.xApp.Visible = visible
        self.xApp.DisplayAlerts = False
        self.workbook = None
        self.active_sheet = None

    def open(self, file_path, sheet_name=None, unprotect=False, password=None):
        self.workbook = self.xApp.Workbooks.Open(file_path, UpdateLinks=0)
        # 设置 DisplayAlerts 为 False 以禁止弹窗警告
        self.sheet(sheet_name or 1, unprotect, password)
        if unprotect is True:
            self.workbook.Unprotect()

    def get_last_used_row(self):
        used_range = self.active_sheet.UsedRange
        return used_range.Rows(used_range.Rows.count).Row

    def find_sheets(self, name):
        return list(filter(lambda _: fnmatch(_.Name, name), self.workbook.Sheets))

    def find_sheet(self, name):
        r = self.find_sheets(name)
        return r[0] if r else None

    def sheet(self, sheet_name, unprotect=False, password=None):
        self.active_sheet = self.workbook.Sheets(sheet_name)
        if unprotect:
            self.active_sheet.Unprotect(password)

    def read_cell(self, w, h):
        return self.active_sheet.cells(h, w)

    def write_cell(self, x, y, value):
        self.active_sheet.cells(y, x).Value = value

    def write_range(self, x, y, data):
        start_cell = self.active_sheet.Cells(y, x)  # 起始单元格
        end_cell = self.active_sheet.Cells(y, x + len(data) - 1)  # 结束单元格
        range_to_write = self.active_sheet.Range(start_cell, end_cell)
        range_to_write.Value = data

    def delete_cell(self, w, h):
        self.active_sheet.cells(h, w).Delete()

    def add_sheet(self, sheet_name):
        new_sheet = self.workbook.Sheets.Add()
        new_sheet.Name = sheet_name
        self.active_sheet = new_sheet

    def save_as(self, new_filename):
        if os.path.exists(new_filename):
            os.remove(new_filename)
        self.workbook.SaveAs(new_filename)

    def save(self):
        self.workbook.Save()

    def close(self):
        self.workbook.Close(SaveChanges=False)
        # self.xApp.Quit()
        self.quit()

    def quit(self):
        self.xApp.Quit()

    def inject_vba(self, macro_code):
        """注入vba代码
        1：标准模块
        2：类模块
        3：用户窗体
        """
        xlmodule = self.workbook.VBProject.VBComponents.Add(1)
        xlmodule.CodeModule.AddFromString(macro_code)

    def run_vba(self, fun_name, *arge):
        """执行vba"""
        self.workbook.Application.Run(fun_name, *arge)


def isFloat(s):
    try:
        float(s)
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    handler = ExcelHandler()
    handler.open(os.path.join(os.path.abspath('..'), 'templates/WebADI.xlsm'), unprotect=True)
    # 往excel写入vba code,及运行vba
    code = '''
    Sub VBAMacro(a,b)
        Dim sh As Worksheet
        Sheet1.Range("E12") = a
        Sheet1.Range("E13") = b
    End Sub
            '''
    handler.inject_vba(code)
    handler.run_vba('VBAMacro', 123123, 6666)

    # handler.open(r"C:\Users\xingqiao.he\Desktop\贝壳\LJ67-240126-02042北京公寓底租成本-闪店计算表.xlsx",
    #              sheet_name="核算指引")
    # sheet = handler.find_sheet("见合-酒*")
    # print(sheet)
    # print(sheet.Name)
    # row3 = handler.active_sheet.Range("A3:BB3")
    # row4 = handler.active_sheet.Range("A4:BB4")
    # find_column = ""
    # # 检查第三行和第四行的每个单元格
    # for cell in row3:
    #     if cell.Value == '24.1月入账' and row4[cell.Column - 1].value == "北京见合-酒店":
    #         find_column = f"{cell.Address}:{cell.Address.split('$')[1]}100"
    #         print(f"The column that satisfies the condition is column {find_column}")
    #         break
    # # 遍历第二列
    # for i in handler.active_sheet.Range(find_column):
    #     if i.value and str(i.value) != "0.0" and str(i.value) != "0" and isFloat(i.value):
    #         print(handler.read_cell(6, i.Row).value)

    # 显示筛选结果
    # handler.active_sheet.UsedRange.AutoFilter.ShowAllItems
    # handler.save_as(os.path.join(os.getcwd(), "adi.xlsm"))
    # handler.close()
