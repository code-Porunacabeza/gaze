import json

import qdarkstyle
from PyQt5.QtWidgets import (QApplication, QInputDialog, QMessageBox,QFileDialog)
from PyQt5.QtGui import QFont
from LoadingWindow import LoadingWindow
from MainWindow import MainWindow
from utils.gazeUtils import refresh
from utils.qtUtils import moveToCenter

helloMessage = '''
This is MIC EYE. 

Look at images, and classify them by typing 0,1,2,3,4,5... on the keyboard, next image will show up.
You can stop any time and the result will be automatically saved in background.

Yours,
MIC EYE-2.0 Beta
'''

# 获取json里面数据
def get_json_data(path,value):
    with open(path, 'rb') as f:  # 使用只读模型，并定义名称为f
        params = json.load(f)  # 加载json文件
        params["image folder"] = value
        print("params", params)  # 打印
    return params  # 返回修改后的内容


# 写入json文件
def write_json_data(path,params):
    # 使用写模式，名称定义为r
    # 其中路径如果和读json方法中的名称不一致，会重新创建一个名称为该方法中写的文件名
    with open(path, 'w') as r:
        # 将dict写入名称为r的文件中
        json.dump(params, r)



config = json.load(open('config.json','r'))
loadingWait: int = config["loading wait"]
font: QFont = QFont(config["font"], 16)
font.setBold(True)
darkMode = config["dark mode"]
logDir = config["save log to"]



if __name__ == "__main__":
    app = QApplication([])
    # startWindow = LoadingWindow(waitTime=loadingWait)
    # moveToCenter(startWindow)
    # startWindow.exec_()
    main = MainWindow(imageDimension=2)
    if darkMode:
        app.setStyleSheet(qdarkstyle.load_stylesheet())
    moveToCenter(main)
    volunteerName, _ = QInputDialog.getText(main, "Name Input", "Please type your file name:")

    # helloBox = QMessageBox()
    # helloBox.setWindowTitle("To user")
    #
    # helloBox.setFont(font)
    # helloBox.setText(f"Hi! {volunteerName},\n" + helloMessage)
    # moveToCenter(helloBox)
    # helloBox.exec_()
    refresh()
    main.setLogSystem(volunteerName, logDir)
    main.show()
    moveToCenter(main)

    app.exec_()
