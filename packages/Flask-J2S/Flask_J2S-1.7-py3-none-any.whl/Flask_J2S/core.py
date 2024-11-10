from Modul_Wrapper import Wrap
import argparse

class Core(Wrap):
	def __init__(kimin, **parameter):
		kimin.parser = argparse.ArgumentParser(description="Flask J2S")
		kimin.parameter = parameter
		super().__init__(modul_path=parameter.get('path_modul', {"modul":[]}))
		
	
	def Run_Server(kimin):
		x = kimin.modul['server'](config=kimin.parameter['config_path'], modul=kimin.modul)
		if len(kimin.modul['sys'].argv) > 1 and kimin.modul['sys'].argv[1] == 'generate':
			x.Prepare()
			print("File Routes Berhasil Di Generate\nSilahkan Jalankan Ulang!!")
			kimin.modul['sys'].exit(1)
		elif len(kimin.modul['sys'].argv) > 1 and kimin.modul['sys'].argv[1] == 'set-fe':
			x.Set_FE()
			print("File File Berhasil Di Generate\nSilahkan Jalankan Ulang!!")
			kimin.modul['sys'].exit(1)
		
		server = x.Server()
		kimin.modul['cors'](server)
		x.Routes(server)
		x.Run(server)