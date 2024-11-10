import importlib

class Set_Server:
	def __init__(kimin, config, modul, base_dir):
		kimin.modul = modul
		kimin.config = kimin.Get_Conf(path=config)
		kimin.base_dir=base_dir
		kimin.use_routes = []
	
	def Get_Conf(kimin, path):
		if kimin.modul['os'].path.exists(path):
			with open(path, 'r', encoding='UTF-8') as dataku:
				return kimin.modul['json'].loads(dataku.read())
		else:
			print(f"File {path} Tidak Ditemukan")
	
	def Check_Func(kimin, modul, function):
		return hasattr(modul, function)
	
	def Set_FE(kimin):
		if 'config' in kimin.config['front-end'] and not kimin.config['front-end']['config'] == "":
			path = f"./{kimin.config['front-end']['config']}"
			data = kimin.Get_Conf(path)
			for i in data:
				kimin.modul['Gen'](log=kimin.config['system'].get('builder_log', False), modul=kimin.modul).Set_FE(template=kimin.config['server']['template_path'].replace("..", '.'), data=data[i], name=i)
			
	def Prepare(kimin):
		if not kimin.modul['os'].path.exists(f"{kimin.config['routes']['modul_name'].replace('.', '/')}.py"):
			kimin.modul['Gen'](log=kimin.config['system'].get('builder_log', False), modul=kimin.modul, modul_path=kimin.config['routes']['modul_name'], class_name=kimin.config['routes']['class_name']).Generate(func=kimin.config['routes'], mode='new')
		
		for i in kimin.config['routes']:
			if not i == "modul_name" and not i == "class_name":
				fungsi = kimin.config['routes'][i]['function']
				modul = importlib.import_module(f"{kimin.config['routes']['modul_name']}")
				modul = getattr(modul, kimin.config['routes']['class_name'])(modul=kimin.modul)
				if not kimin.Check_Func(modul, fungsi):
					kimin.modul['Gen'](log=kimin.config['system'].get('builder_log', False), modul=kimin.modul, modul_path=kimin.config['routes']['modul_name'], class_name=kimin.config['routes']['class_name']).Generate(func=kimin.config['routes'][i], kunci=i)
		
		sin = kimin.modul['Gen'](log=kimin.config['system'].get('builder_log', False), modul=kimin.modul)
		sin.aset = kimin.config['front-end'].get('assets', ['content', 'base', 'header', 'page'])
		sin.Set_BasePath(static=kimin.config['server']['static_path'].replace("..", "."), template=kimin.config['server']['template_path'].replace("..", "."))
	
	def Routes(kimin, server):
		for i in kimin.config['routes']:
			if not i == "modul_name" and not i == "class_name":
				if not kimin.config['routes'][i] in kimin.use_routes:
					modul = importlib.import_module(f"{kimin.config['routes']['modul_name']}")
					if kimin.config['system']['import_config']:
						modul = getattr(modul, kimin.config['routes']['class_name'])(modul=kimin.modul, be=kimin.config, fe=kimin.Get_Conf(f"{kimin.base_dir}/{kimin.config['front-end']['config']}"), server=server)
					else:
						modul = getattr(modul, kimin.config['routes']['class_name'])(modul=kimin.modul)
					fungsi = kimin.config['routes'][i]['function']
					server.add_url_rule(
						kimin.config['routes'][i]['url'],
						view_func= getattr(modul, fungsi),
						methods=kimin.config['routes'][i]['methods']
						)
					kimin.use_routes.append(kimin.config['routes'][i])
				
	def Server(kimin):
		server = kimin.modul['flask'](
			__name__, 
			static_folder=f"{kimin.base_dir}/{kimin.config['server']['static_path']}", 
			template_folder=f"{kimin.base_dir}/{kimin.config['server']['template_path']}")
		
		if kimin.config['server']['template_auto_reload'] is True:
			server.jinja_env.auto_reload = True
			server.config['TEMPLATES_AUTO_RELOAD'] = True
		
		if kimin.config['server']['debug'] is True:
			server.config['DEBUG'] = True
		
		if 'secret_key' in kimin.config['server'] and not kimin.config['server']['secret_key'] is None:
			server.secret_key=kimin.config['server']['secret_key']
		
		if 'session_lifetime' in kimin.config and isinstance(kimin.config['server']['session_lifetime'], int):
			server.config["SESSION_PERMANENT"] = False
			server.config['PERMANENT_SESSION_LIFETIME'] =  datetime.timedelta(minutes=kimin.config['server']['session_lifetime'])
		return server
	
	def Run(kimin, server):
		server.run(host=kimin.config['server']['host'], debug=kimin.config['server']['debug'], port=kimin.config['server']['port'])