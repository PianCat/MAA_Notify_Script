import urllib.parse
import urllib.request
import re

LOG_PATH = '..\debug\gui.log' # 日志文件路径
KEYWORD_START = 'Main windows log clear.'
KEYWORD_ERROR = '任务出错'
KEYWORD_WARNING = '代理指挥失误'
KEYWORD_REPORT = ['开始任务: Fight', '完成任务: Fight', '掉落统计:']
KEYWORD_REPORT_BREAK = ['已开始行动', '代理指挥失误']

SERVERCHAN_KEY = 'SCT85856TF6m9Fsztkqcyew8yXHWg3XUP' # Server酱的SCKEY


def search_keyword():
    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        start_line = 0
        line_error = ''
        line_report = []
        line_report_count = [0, 0]
        for i in range(len(lines)):  # 找到最后一个开始标志 KEYWORD_START
            if KEYWORD_START in lines[i]:
                start_line = i
        for i in range(start_line, len(lines)):  # 从最后一个开始标志 KEYWORD_START 开始往后找
            if KEYWORD_ERROR in lines[i] or KEYWORD_WARNING in lines[i]:
                line_error += lines[i] + '\n'
            if KEYWORD_REPORT[0] in lines[i]:  # 记录 开始任务: Fight 的行数
                line_report_count[0] = i
            if KEYWORD_REPORT[1] in lines[i]:  # 记录 完成任务: Fight 的行数
                line_report_count[1] = i
        if line_report_count[0] == 0 or line_report_count[1] == 0:
            line_report = ['No Fight.']
        for i in range(line_report_count[1], line_report_count[0], -1):  # 倒序查找，找到最后一个 掉落统计: 的行数
            if line_report_count[1] - line_report_count[0] == 1:
                line_report = ['No Drop.']
                break
            if KEYWORD_REPORT[2] in lines[i]:
                for j in range(i, line_report_count[1]):
                    # 跳过 代理指挥失误
                    if KEYWORD_REPORT_BREAK[0] in lines[j] or KEYWORD_REPORT_BREAK[1] in lines[j]:
                        break
                    line_report.append(re.sub(r'\s*\(.*?\)', '', lines[j]))  # 去除掉落统计行中的括号及括号内内容
                break
        if KEYWORD_ERROR in line_error or KEYWORD_WARNING in line_error:
            return line_error, line_report
        else:
            return 'No Error Log.', line_report


def line_report_format(line_report):
    if len(line_report) == 1:
        return line_report[0]
    for i in range(len(line_report)):
        line_report[i] = re.sub(r'\n', '', line_report[i])
        if i == 0:
            line_report[i] = re.sub(r'<.*><>', '', line_report[i])
    # 将 line_report 从第 1 行开始(跳过第 0 行) 按照':'分割为两列，储存为二维数组
    line_report_array = [i.split(':') for i in line_report[1:]]
    # # 将二维数组转换为 markdown 表格格式
    # line_report_md = '| 材料 | 数量 |' + '\n' + '|:---:|:---:|\n'
    # for i in range(len(line_report_array)):
    #     line_report_md += '| ' + ' | '.join(line_report_array[i]) + ' |\n'
    # line_report_md = line_report[0] + '\n\n' + line_report_md
    line_report_output = line_report[0] + '\n\n'
    for i in range(len(line_report_array)):
        line_report_output += line_report_array[i][0] + '    ' + line_report_array[i][1] + '\n\n'
    return line_report_output

def serverchan_send(text, desp):
  post_data = urllib.parse.urlencode({
    'text': text,
    'desp': desp
  }).encode('utf-8')

  req = urllib.request.Request('https://sctapi.ftqq.com/%s.send' % SERVERCHAN_KEY, data=post_data)
  urllib.request.urlopen(req)

def notify(text, desc):
  serverchan_send(text, desc)


if __name__ == '__main__':
    log, line_report = search_keyword()
    # print(line_report)
    if KEYWORD_ERROR in log:
        text = '## ⚠️MAA 已经完成了任务, 但有些任务失败了!'
        desc = "### *以下是错误报告*:\n\n" + log + '\n\n' + \
               "### *以下是掉落报告*:\n\n" + line_report_format(line_report)
        # notify('## ⚠️MAA 已经完成了任务, 但有些任务失败了!', "### *这些是错误报告*:\n\n" + log)
    elif KEYWORD_WARNING in log:
        text = '## ⚠️MAA 已经完成了任务, but there\'s warning!'
        desc = "### *以下是警告信息*:\n\n" + log + '\n\n' + \
               "### *以下是掉落报告*:\n\n" + line_report_format(line_report)
        # notify('## ⚠️MAA 已经完成了任务, but there\'s warning!', "### *Here's the WARNING log*:\n\n" + log)
    else:
        text = '## 🎉MAA 已经完成了任务, and everything is perfect!'
        desc = "### *以下是掉落报告*:\n\n" + line_report_format(line_report)
        # notify('## 🎉MAA 已经完成了任务, and everything is perfect!', '*' + log + '*')
    notify(text, desc)
