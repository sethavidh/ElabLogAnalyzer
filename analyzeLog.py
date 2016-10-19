# Analyzing elab logs for logins/submits using different IP during test
#  by Sethavidh Gertphol
#  18 Oct 2016
#  to do: 1. log file from command line
#         2. move into functions, refactor

from operator import itemgetter

def parse_log(log_file):
    logins = []
    submits = []
    for line in open(log_file,'r'):
        log_line = []
        fields = line.split()
        if len(fields) == 5: #logins
            time_str = fields[2] + ' ' + fields[3]
            time_str = time_str.rstrip(']').lstrip('[')
            time_fmt = '%Y-%m-%d %H:%M:%S'
            #time = datetime.datetime.strptime(time_str, time_fmt)
            if not (start_time < time_str < end_time): continue
            id_ip = fields[4].split('/')
            id = id_ip[0].lstrip('(')
            log_line.append(id)
            log_line.append(fields[0])
            log_line.append(time_str)
            log_line.append('LOGIN')
            logins.append(log_line)
        elif len(fields) == 11: # submits
            time_str = fields[8] + ' ' + fields[9]
            time_str = time_str.rstrip(']').lstrip('[')
            time_fmt = '%Y-%m-%d %H:%M:%S'
            #time = datetime.datetime.strptime(time_str, time_fmt)
            if not (start_time < time_str < end_time): continue
            id_ip = fields[10].split('/')
            id = id_ip[0].lstrip('(')
            log_line.append(id)
            log_line.append(fields[0])
            log_line.append(time_str)
            log_line.append('SUBMIT')
            log_line.append(fields[7]) #sec
            log_line.append(fields[5].rstrip(',')) #problem number
            submits.append(log_line)
    return logins, submits 

def insert_db(db, logs):
    for i in logs:
        id = i[0]
        if id not in db:
            db[id] = []
        db[id].append(i)    

path = '/Users/akepooh/Dropbox/Documents/Classes/Intro_to_Comp/114_591/Midterm/'    
log1 = r'log.section497.txt'
log2 = r'log.section498.txt'
log1 = path+log1
log2 = path+log2

start_time = '2016-10-09 09:00:00'
end_time = '2016-10-09 12:10:00'

logins, submits = parse_log(log1)
logins2, submits2 = parse_log(log2)
logins.extend(logins2)
submits.extend(submits2)

d = {}
insert_db(d,logins)
insert_db(d,submits)

for i in d: #sort by time and analyze diff ip
    d[i].sort(key=itemgetter(2))
    ip_ls = []
    for x in d[i]:
        ip = x[1]
        if ip not in ip_ls:
            ip_ls.append(ip)
    if len(ip_ls) > 1:
        print(i, ': ')
        for x in d[i]:
            print(x)

while (1):
    id = input('\nEnter Student ID to check: ')
    if id == '': break
    if id not in d:
        print('No ID in DB')
    else:
        for x in d[id]:
            print(x)