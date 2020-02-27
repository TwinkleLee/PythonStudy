from tkinter import *           # 导入 Tkinter 库
root = Tk()                     # 创建顶级窗口
root.title('窗口标题')
# 创建两个列表
li = ['C', 'python', 'php', 'html', 'SQL', 'java']
listb = Listbox(root)           # 在root中创建两个列表组件
for item in li:                 # 第一个小部件插入数据
    listb.insert(0, item)

w = Label(root, text="Hello Tkinter!")

# 调用pack进行布局
w.pack()
listb.pack()

# root.mainloop()                 # 进入消息循环

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        # 调用initWidgets()方法初始化界面
        self.initWidgets()

    def initWidgets(self):
        # 创建Label对象，第一个参数指定该Label放入root
        w = Label(self)
        # 创建一个位图
        bm = PhotoImage(file='0.png')
        # 必须用一个不会被释放的变量引用该图片，否则该图片会被回收
        w.x = bm
        # 设置显示的图片是bm
        w['image'] = bm
        w.pack()
        # 创建Button对象，第一个参数指定该Button放入root
        okButton = Button(self, text="确定", background="blue")
        # okButton['background'] = 'yellow'
        # okButton.configure(background='yellow')
        okButton.pack()



# 创建Application对象
app = Application()
# Frame实例的master属性指向Tk对象（窗口）
print(type(app.master))
# 启动主窗口的消息循环
app.mainloop()

