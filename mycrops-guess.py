#-*- coding: utf-8 -*-
import urllib
import urllib2
import hashlib
import time
import thread

# prepare data
info = {
    'action': 'getGuessTeam',
    'timestamp': '',
    'sign': ''
}

f_error = open('error.log', 'a')
f_res = open('res.log', 'a')
call_num = 0
error_num = 0
res_num = 0


def makedata(test_case=info):
    case = test_case
    case['timestamp'] = str(int(time.time()))
    appid = '1105260001'
    appkey = 'f46806d675f16feae23b5c07d4a3c935'

    sign_data = appid+case['timestamp']+appkey
    sign_md5 = hashlib.md5()
    sign_md5.update(sign_data)
    case['sign'] = sign_md5.hexdigest()

    data = urllib.urlencode(case)

    f = open('urlencode_data.txt', 'a')
    f.write(str(data)+'\n')
    f.close


def send(url_data):
    global error_num, res_num, call_num, f_error, f_res
    data = url_data
    # print data
    url = 'http://activityapi.qa.15166.com/sqNewData/corps-guess'
    request = urllib2.Request(url, data)
    try:
        call_num = call_num+1
        response = urllib2.urlopen(request,timeout=10)
        res_num = res_num+1
        res = response.read()
        f_res.write(str(res)+'\n')
    except urllib2.URLError, e:
        error_num = error_num+1
        f_error.write(str(e)+'\n')
    except urllib2.HTTPError, e:
        error_num = error_num+1
        f_error.write(str(e)+'\n')
    except urllib2.socket.timeout,e:
        error_num = error_num+1
        f_error.write(str(e)+'\n')

max_id = 60
round_count = 60

for i in range(max_id*round_count):
    print 'create data ', i
    makedata()

f = open('urlencode_data.txt', 'r')
case = []

for line in f:
    line = line.strip('\n')
    line = line.strip('\r')
    data = line
    case = case+[data]

f.close()
start_time = time.time()

for i in range(round_count):
    R_time = time.time()

    for j in range(max_id):
        # print 'excute press ',i*max_id+j
        thread.start_new_thread(send, (case[i*max_id+j],))

    E_time = time.time()
    if E_time-R_time < 1:
        time.sleep(1-(E_time-R_time))
    else:
        f = open('time_error.txt', 'a')
        f.write("a round excute time has aleady greater than one sec at round")
        f.write(i+'\n')

time.sleep(30)
end_time = time.time()
f_res.close()
f_error.close()
excute_time = end_time - start_time

print 'call_num : ', call_num
print 'res_num : ', res_num
print 'error_num : ', error_num
print 'excute time :', excute_time
