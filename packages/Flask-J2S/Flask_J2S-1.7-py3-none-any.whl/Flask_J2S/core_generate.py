class Generate:
	def __init__(kimin, modul, **parameter):
		kimin.modul, kimin.parameter, kimin.aset, kimin.base_template = modul, parameter, [], "https://raw.githubusercontent.com/staykimin/Flask-J2S/master/Base_Template/route.json"
		kimin.modul['init'](autoreset=True)
	
	def Get_Header(kimin, data):
		x = f"\n\n\tdef {data['function']}(kimin"
		y = [i.replace("<",", ").replace(">","") for i in data['url'].split("/") if not i == ""]
		return x + "".join(y) + "):\n\t\t" if len(y) > 1 else x + "):\n\t\t"
	
	def Get_Time(kimin, format="%d-%m-%Y %H:%M:%S"):
		return kimin.modul['datetime'].datetime.now().strftime(format)
	
	def Submit(kimin, url):
		respon = kimin.modul['Executor'](
			modul=kimin.modul,
			url=url,
			method='GET'
			).Execute()
		return respon['data'] if 'status_code' in respon and respon['status_code'] == 200 else None
	
	
	def Set_FE(kimin, template, data, name):
		log = kimin.parameter.get('log', False)
		path = f"{template}/{data['path']}"
		if not kimin.modul['os'].path.exists(path):
			cfg = kimin.Submit(kimin.base_template)
			if cfg:
				cfg = kimin.modul['json'].loads(cfg)
				if data['content']['type'] in cfg['data']:
					if data['content']['author'] in cfg['data'][data['content']['type']]:
						if str(data['content']['version']) in cfg['data'][data['content']['type']][data['content']['author']]:
							x = kimin.Submit(f"{cfg['base_server']}{cfg['data'][data['content']['type']][data['content']['author']][str(data['content']['version'])]['path']}")
							if x:
								with open(path, 'w', encoding='UTF-8') as dataku:
									dataku.write(x)
								if log:
									print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate File {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{name}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].GREEN} Success {kimin.modul['Fore'].WHITE}-> {path}")
							else:
								if log:
									print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate File {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{name}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].RED} Failed {kimin.modul['Fore'].BLUE}-> Gagal Terhubung Dengan Server!!")
						else:
							if log:
								print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate File {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{name}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].RED} Failed {kimin.modul['Fore'].BLUE}-> Versi '{data['content']['version']}' Tidak Tersedia!!")
					else:
						if log:
							print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate File {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{name}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].RED} Failed {kimin.modul['Fore'].BLUE}-> Author '{data['content']['author']}' Tidak Tersedia!!")
				else:
					if log:
						print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate File {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{name}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].RED} Failed {kimin.modul['Fore'].BLUE}-> Type '{data['content']['type']}' Tidak Tersedia!!")
			else:
				if log:
					print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate File {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{name}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].RED} Failed {kimin.modul['Fore'].BLUE}-> Gagal Terhubung Dengan Server!!")
		else:
			if log:
				print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate File {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{name}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].RED} Failed {kimin.modul['Fore'].BLUE}-> File {path} Sudah Ada!!")
	
	def Set_BasePath(kimin, static, template):
		log = kimin.parameter.get('log', False)
		if not kimin.modul['os'].path.exists(static):
			kimin.modul['os'].makedirs(static)
			if log:
				print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate Path {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{static}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].GREEN} Success")
		
		if not kimin.modul['os'].path.exists(template):
			kimin.modul['os'].makedirs(template)
			if log:
				print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate Path {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{template}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].GREEN} Success")
		
		for i in kimin.aset:
			path =f"{static}/{i}"
			if not kimin.modul['os'].path.exists(path):
				kimin.modul['os'].makedirs(path)
				if log:
					print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate Path {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{path}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].GREEN} Success")
		
		for i in kimin.aset:
			path =f"{template}/{i}"
			if not kimin.modul['os'].path.exists(path):
				kimin.modul['os'].makedirs(path)
				if log:
					print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate Path {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{path}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].GREEN} Success")
	
	def Generate(kimin, func, mode='add', **parameter):
		log = kimin.parameter.get('log', False)
		awal = "./"
		for i in kimin.parameter['modul_path'].split(".")[:-1]:
			path = f"{awal}/{i}"
			path = path.replace("//", '/')
			if not kimin.modul['os'].path.exists(path):
				kimin.modul['os'].makedirs(path)
				if log:
					print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate Path {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{path}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].GREEN} Success")
			awal = path
		
		path = f"{kimin.parameter['modul_path'].replace('.', '/')}.py"
		if mode == 'add':
			if kimin.modul['os'].path.exists(path):
				with open(path, 'r', encoding='UTF-8') as dataku:
					data = dataku.read()
				
				header = kimin.Get_Header(func)
				if data.find(header) == -1:
					hasil = {'status':False}
					if 'output' in func:
						if 'type' in func['output'] and func['output']['type'].lower() in ['api', 'string', 'render_template']:
							if "data" in func['output']:
								if func['output']['type'].lower() == 'api':
									data += header + "return {'data':"
									data += f"kimin.parameter['cfg']['routes']['{parameter['kunci']}']['output']['data']"
									data += "}"
								elif func['output']['type'].lower() == "string":
									data += header + f"return str(kimin.parameter['cfg']['routes']['{parameter['kunci']}']['output']['data'])"
								
								elif func['output']['type'].lower() == 'render_template':
									data += header + f"with open(kimin.parameter['cfg']['front-end']['config'], 'r', encoding='UTF-8') as dataku:\n\t\t\tdata=kimin.modul['json'].loads(dataku.read())"
									data += f"\n\t\treturn kimin.modul['render_template'](data['{func['output']['data']}']['path'], base=data[data['{func['output']['data']}']['base']]['path'], header=data[data['{func['output']['data']}']['header']]['path'], judul='{parameter['kunci']}')"
							else:
								data += header + f"return 'Ini Fungsi {func['function']}'"
							with open(path, 'w', encoding='UTF-8') as dataku:
								dataku.write(data)
								hasil['status'] = True
						else:
							hasil['error'] = 'Type Output Tidak Tersedia'
					else:
						data += header + f"return 'Ini Fungsi {func['function']}'"
						with open(path, 'w', encoding='UTF-8') as dataku:
							dataku.write(data)
						hasil['status'] = True
					if log:
						if hasil['status']:
							print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate Function {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{func['function']}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].GREEN} Success")
						elif not hasil['static']:
							print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate Function {kimin.modul['Fore'].LIGHTMAGENTA_EX}'{func['function']}' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].GREEN} Failed {kimin.modul['Fore'].WHITE}-> {hasil['error']}")
		
		elif mode == 'new':
			with open(path, 'w', encoding='UTF-8') as dataku:
				dataku.write(f"class {kimin.parameter['class_name']}:\n\tdef __init__(kimin, modul, **parameter):\n\t\tkimin.modul, kimin.parameter = modul, parameter")
			if log:
				print(f"{kimin.modul['Fore'].LIGHTBLUE_EX}[{kimin.Get_Time()}]{kimin.modul['Fore'].YELLOW} Generate {kimin.modul['Fore'].LIGHTMAGENTA_EX}'Base Function' {kimin.modul['Fore'].WHITE}->{kimin.modul['Fore'].GREEN} Success")