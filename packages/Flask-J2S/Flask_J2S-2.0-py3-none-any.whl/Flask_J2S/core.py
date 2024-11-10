from Modul_Wrapper import Wrap
import inspect

class Processing(Wrap):
	def __init__(kimin, **parameter):
		kimin.parameter = parameter
		super().__init__(modul_path=parameter.get('path_modul', {"modul":[]}))
		kimin.base_dir = kimin.Base_Dir()
	
	def Base_Dir(kimin):
		stack = inspect.stack()
		for frame_info in stack:
			# Menghindari frame dari modul ini sendiri
			if frame_info.filename != __file__:
				# Mendapatkan path dari file yang memanggil fungsi ini
				caller_file = frame_info.filename
				# Mendapatkan base path dari file pemanggil
				caller_base_path = kimin.modul['os'].path.dirname(kimin.modul['os'].path.abspath(caller_file))
				return caller_base_path
		return None
	
	def Run_Server(kimin):
		x = kimin.modul['server'](config=kimin.parameter['config_path'], modul=kimin.modul, base_dir=kimin.base_dir)
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