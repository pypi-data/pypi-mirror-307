class Driver:
	def __init__(kimin, modul, **parameter):
		kimin.parameter = parameter
		kimin.modul = modul
	
	def Execute(kimin):
		hasil = {'status':False}
		try:
			if kimin.parameter['method'].lower() == 'get':
				respon = kimin.modul['Driver'].request(kimin.parameter['method'], kimin.parameter['url'], headers=kimin.parameter.get('header', {}), cookies=kimin.parameter.get('cookie', {}), allow_redirects=kimin.parameter.get('redirect', True))
			elif kimin.parameter['method'].lower() == 'post' or 'patch':
				if kimin.parameter['data_type'].lower() == 'json':
					respon = kimin.modul['Driver'].request(kimin.parameter['method'], kimin.parameter['url'], headers=kimin.parameter.get('header', {}), json=kimin.parameter['data'], cookies=kimin.parameter.get('cookie', {}))
				elif kimin.parameter['data_type'].lower() == 'form':
					respon = kimin.modul['Driver'].request(kimin.parameter['method'], kimin.parameter['url'], headers=kimin.parameter.get('header', {}), data=kimin.parameter['data'], cookies=kimin.parameter.get('cookie', {}), allow_redirects=kimin.parameter.get('redirect', True))
			hasil['status'], hasil['data'], hasil['status_code'], hasil['respon']= True, respon.text, respon.status_code, respon
		except kimin.modul['Driver'].Timeout:
			hasil['data'] = "Timeout"
		except kimin.modul['Driver'].RequestException as e:
			hasil['data'] = 'Tidak Dapat Terhubung Ke Server'
		
		return hasil