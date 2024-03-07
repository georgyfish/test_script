#!/usr/bin/env python3
# /home/swqa/xc_tool/testcase/
# 执行heaven、valley 1080P LOW
import os
import sys
# from syslog import LOG_WARNING
# import time

_XC_TOOL_PATH = os.path.abspath(os.path.join(os.getcwd(), '../'))
_HEAVEN_PATH = os.path.join(_XC_TOOL_PATH, "tool/Unigine_Heaven-4.0")
_VALLEY_PATH = os.path.join(_XC_TOOL_PATH, "tool/Unigine_Valley-1.0")
APP_PATH = {'heaven': _HEAVEN_PATH, 'valley': _VALLEY_PATH}
DEFAULT_QUALITY = "LOW"


# 执行
def run_app(app, quality):
    app_path = APP_PATH[app]
    #os.system(f'export DISPLAY=:0.0 && cd {app_path}/automation/ && python3 daily_run.py {quality}')
    if quality == 'extreme':
        os.system(f'export DISPLAY=:0.0 && cd {app_path}/automation/ && python3 daily_ultra_run.py')
    else:
        os.system(f'export DISPLAY=:0.0 && cd {app_path}/automation/ && python3 daily_run.py {quality}')



# 取分数
def get_score(app):
    app_path = APP_PATH[app]
    cmd = f'tail -n 1 {app_path}/automation/reports/daily_run_log.csv'
    #    score = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # score = os.popen(cmd)
    score = None
    with os.popen(cmd) as f:
        score = f.read().split(',')[0]
    return score



def run(app=None, quality=DEFAULT_QUALITY):
    # for app in APP_DIC.keys():
    #     app_path = APP_DIC[app]
    #     if not os.path.exists(app_path):
    #         install_app(app)
    apps = {}
    if not app:
        apps = APP_PATH
    else:
        if app in APP_PATH:
            apps[app] = APP_PATH[app]
        else:
            print("Unigine程序不在范围内，请输入valley或heaven")
            return None

    app_score = []
    for app in apps:
        run_app(app, quality)
        app_score.append((app, get_score(app)))
        # print(f'{app}_1080P_LOW:{get_score(app)}')
        # time.sleep(60)

    for (app, fps) in app_score:
        print(f'{app}__{quality}:{fps}')
        os.system( '/bin/bash ' + _XC_TOOL_PATH + f'/lib/submit_data.sh {app} {fps}')

# default run heaven&valley; 参数1指定app，参数2指定质量

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        run(sys.argv[1], sys.argv[2])


