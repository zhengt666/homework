from feasibility_utils import upload_excel_files
from tkinter import messagebox


# 确认用户是否要批量上传
user_confirmation = messagebox.askyesno("上传确认", "请上传Excel文件")
if not user_confirmation:
    exit()
# 调用函数以上传Excel文件
upload_excel_files()