import requests
import json
import threading
import Queue
from time import sleep

class Sqlmap_Api():
	def __init__(self,Api_Address="http://127.0.0.1:8775",Filename="../Input/sql_urls.txt",Output="../Output/ret.txt",ThreadNum=5,Result=[]):
		self.Api_Address=Api_Address
		self.Filename=Filename
		self.ThreadNum=ThreadNum
		self.Task=Queue.Queue()
		self.Lock=threading.Lock()
		self.Output=Output
		self.Result=Result

	def GetUrls(self):
		with open(self.Filename,"r") as f:
			for url in f.readlines():
				self.Task.put(url.strip())
	def SendtoApi(self):
		while not self.Task.empty():
			self.Lock.acquire()
			url=self.Task.get().strip()
			print "[*] testing : "+url
			try:
				r = requests.get(self.Api_Address+"/task/new")
				taskid= r.json()['taskid']
				r = requests.post(self.Api_Address+'/scan/'+taskid+'/start', data=json.dumps({'url': url}), headers={'content-type': 'application/json'})
				r = requests.get(self.Api_Address+'/scan/'+taskid+'/status')
				count=0
				while(r.json()["status"] == "running"):
					sleep(5)
					r = requests.get(self.Api_Address+'/scan/'+taskid+'/status')
					count=count+1
					if count==20:
						requests.get(self.Api_Address+'/scan/' + taskid + '/stop')
				r = requests.get(self.Api_Address+'/scan/'+taskid+'/data')
				requests.get(self.Api_Address+'/scan/'+taskid+'/delete')
				if r.json()['data']:
					print "[+] injection found :" + url
					self.Result.append(url)
					with open(self.Output,"a") as f:
						f.write(url+"\n")
			except requests.ConnectionError:
				print "Fail to connect!"
			self.Lock.release()
	def Work(self):
		threads = []
		for i in range(self.ThreadNum):
			t = threading.Thread(target=self.SendtoApi())
			threads.append(t)
			t.start()
		for t in threads:
			t.join()
if __name__ == '__main__':
	test=Sqlmap_Api(Filename="input.txt",Output="ret.txt")
	test.GetUrls()
	test.Work()