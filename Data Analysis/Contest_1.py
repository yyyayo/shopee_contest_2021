import json
import time
import pandas as pd

start = time.time()

f = open('contacts.json','r')
content = f.read()
data = json.loads(content)
# data = data[0:10000]

for i in range(len(data)):
	data[i]['Class'] = i

classes = []
newClass = {}
newClass['Class'] = len(classes)
newClass['ticket_trace'] = str(data[0]['Id'])
newClass['contact'] = data[0]['Contacts']
newClass['Email'] = []
newClass['Email'].append(data[0]['Email'])
newClass['Phone'] = []
newClass['Phone'].append(data[0]['Phone'])
newClass['OrderId'] = []
newClass['OrderId'].append(data[0]['OrderId'])
classes.append(newClass)

for i in range(1, len(data)):
	length = len(classes)
	j = 0
	flag = False
	for j in range(length):
		if(((data[i]['Email'] in classes[j]['Email']) and data[i]['Email']!="") or ((data[i]['Phone'] in classes[j]['Phone']) and data[i]['Phone']!="") or ((data[i]['OrderId'] in classes[j]['OrderId']) and data[i]['OrderId']!="")):
			data[i]['Class'] = classes[j]['Class']
			classes[j]['ticket_trace'] += '-'
			classes[j]['ticket_trace'] += str(data[i]['Id'])
			classes[j]['contact'] += data[i]['Contacts']
			if data[i]['Email']!="":
				classes[j]['Email'].append(data[i]['Email'])
			if data[i]['Phone']!="":
				classes[j]['Phone'].append(data[i]['Phone'])
			if data[i]['OrderId']!="":
				classes[j]['OrderId'].append(data[i]['OrderId'])
			flag = True
			break
	if flag == False:
		data[i]['Class'] = len(classes)
		newClass = {}
		newClass['Class'] = len(classes)
		newClass['ticket_trace'] = str(data[i]['Id'])
		newClass['contact'] = data[i]['Contacts']
		newClass['Email'] = []
		newClass['Email'].append(data[i]['Email'])
		newClass['Phone'] = []
		newClass['Phone'].append(data[i]['Phone'])
		newClass['OrderId'] = []
		newClass['OrderId'].append(data[i]['OrderId'])
		classes.append(newClass)

out1 = list()
out2 = list()
out = pd.DataFrame()
for i in range(len(data)):
    out1.append(i)
    class_id = data[i]['Class']
    ticket_trace = classes[class_id]['ticket_trace']
    contact = classes[class_id]['contact']
    str_ = [ticket_trace,", ",str(contact)]
    new_str = "".join(str_)
    out2.append(new_str)
out['ticket_id'] = out1
out['ticket_trace/contact'] = out2
out.to_csv('contact_result_new.csv', index=False)
print(time.time() - start)