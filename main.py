import os
import yaml
import time
import zipfile
import schedule
import datetime
import PySimpleGUI as sg

version = "v1.0.0"

def CreateYaml(key):
    with open("config.yml", "w", encoding="utf-8") as c:
        yaml.dump(key, c)

if not os.path.exists("config.yml"):
    Dict = {"BackupPath":f"{os.getcwd()}", "SavePath":f"{os.getcwd()}", "BackupTime":300}
    CreateYaml(Dict)
    layout = [[sg.Text("请输入您的存档位置", key='-BakPathText-')],
          [sg.Input(key='-BakPath-')],
          [sg.Text("请输入保存位置", key='-SavePathText-')],
          [sg.Input(key='-SavePath-')],
          [sg.Text("请输入备份次数（未实现）")],
          [sg.Input(key='-BakCount-')],
          [sg.Text("请输入备份间隔，单位：秒", key='-BakTimeText-')],
          [sg.Input(key='-BakTime-')],
          [sg.Text("注：确定后程序将会卡死，如需结束强制结束进程即可", size=(40,1), key='-OUTPUT-')],
          [sg.Button('确定')]]
elif os.path.exists("config.yml"):
    with open("config.yml", encoding='utf-8') as r:
        config = yaml.load(r, Loader=yaml.FullLoader)
        BackupPath = config["BackupPath"]
        SavePath = config["SavePath"]
        BackupTime = config["BackupTime"]
    layout = [[sg.Text(f"存档位置，默认：{BackupPath}", key='-BakPathText-')],
          [sg.Input(key='-BakPath-')],
          [sg.Text(f"保存位置，默认：{SavePath}", key='-SavePathText-')],
          [sg.Input(key='-SavePath-')],
          [sg.Text("请输入备份次数（未实现）")],
          [sg.Input(key='-BakCount-')],
          [sg.Text(f"请输入备份间隔，单位：秒，默认：{BackupTime}", key='-BakTimeText-')],
          [sg.Input(key='-BakTime-')],
          [sg.Text("注：确定后程序将会卡死，如需结束强制结束进程即可", size=(40,1), key='-OUTPUT-')],
          [sg.Button('确定')]]

def InputConf():
    with open("config.yml",'r',encoding='utf-8') as c:
        config = yaml.load(c, Loader=yaml.FullLoader)
    with open("config.yml",'w',encoding='utf-8') as f:
        config["BackupPath"] = values['-BakPath-']
        config["SavePath"] = values['-SavePath-']
        config["BackupTime"] = values['-BakTime-']
        yaml.dump(config, f)

def ssb():
    BakTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if os.path.exists("config.yml"):
        if values['-BakPath-'] != "" and values['-SavePath-'] != "":
            if os.path.isfile(values['-BakPath-']):
                    with zipfile.ZipFile(values['-SavePath-'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                        z.write(values['-BakPath-'])
            else:
                with zipfile.ZipFile(values['-SavePath-'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                    for root, dirs, files in os.walk(values['-BakPath-']):
                        for single_file in files:
                            if single_file != values['-SavePath-'] + f'\\ssb_{BakTime}.zip':
                                filepath = os.path.join(root, single_file)
                                z.write(filepath)
        if values['-BakPath-'] == "" and values['-SavePath-'] == "":
            if os.path.isfile(config["BackupPath"]):
                    with zipfile.ZipFile(config['SavePath'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                        z.write(config["BackupPath"])
            else:
                with zipfile.ZipFile(config['SavePath'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                    for root, dirs, files in os.walk(config["BackupPath"]):
                        for single_file in files:
                            if single_file != config['SavePath'] + f'\\ssb_{BakTime}.zip':
                                filepath = os.path.join(root, single_file)
                                z.write(filepath)
        elif values['-BakPath-'] == "" and values['-SavePath-'] != "":
            if os.path.isfile(config["BackupPath"]):
                with zipfile.ZipFile(values['-SavePath-'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                    z.write(config["BackupPath"])
            else:
                with zipfile.ZipFile(values['-SavePath-'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                    for root, dirs, files in os.walk(config["BackupPath"]):
                        for single_file in files:
                            if single_file != values['-SavePath-'] + f'\\ssb_{BakTime}.zip':
                                filepath = os.path.join(root, single_file)
                                z.write(filepath)
        elif values['-BakPath-'] != "" and values['-SavePath-'] == "":
            if os.path.isfile(values['-BakPath-']):
                with zipfile.ZipFile(config['SavePath'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                    z.write(values['-BakPath-'])
            else:
                with zipfile.ZipFile(config['SavePath'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                    for root, dirs, files in os.walk(values['-BakPath-']):
                        for single_file in files:
                            if single_file != config['SavePath'] + f'\\ssb_{BakTime}.zip':
                                filepath = os.path.join(root, single_file)
                                z.write(filepath)
    else:
        if os.path.isfile(values['-BakPath-']):
            with zipfile.ZipFile(values['-SavePath-'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                z.write(values['-BakPath-'])
        else:
            with zipfile.ZipFile(values['-SavePath-'] + f'\\ssb_{BakTime}.zip', 'w') as z:
                for root, dirs, files in os.walk(values['-BakPath-']):
                    for single_file in files:
                        if single_file != values['-SavePath-'] + f'\\ssb_{BakTime}.zip':
                            filepath = os.path.join(root, single_file)
                            z.write(filepath)

window = sg.Window(f'ssb {version}', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    ssb()
    InputConf()
    window['-OUTPUT-'].update("已成功备份！")
    if os.path.exists("config.yml"):
        if values['-BakTime-'] == "":
            schedule.every(int(config["BackupTime"])).seconds.do(ssb)
        else:
            schedule.every(int(values['-BakTime-'])).seconds.do(ssb)
    else:
        schedule.every(int(values['-BakTime-'])).seconds.do(ssb)
    while True:
        schedule.run_pending()
        time.sleep(1)
        window['-OUTPUT-'].update("已成功备份！")

window.close()