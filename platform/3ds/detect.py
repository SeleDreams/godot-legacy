
import os
import sys	


def is_active():
	return True
		
def get_name():
	return "3ds"

def can_build():
	return True # enabled
  
def get_opts():
	return [
	('use_llvm','Use llvm compiler','no'),
	('force_32_bits','Force 32 bits binary','no')
	]
  
def get_flags():
	return [
		('tools', 'no'),
		('squish', 'no'),
		('theora', 'no'),
		('vorbis', 'yes'),
		('speex', 'no'),
		('dds', 'no'),
		('pvr', 'no'),
		('builtin_zlib', 'yes'),
		('builtin_freetype','yes'),
		("openssl", "no"),
		('musepack', 'no')
	]

def configure(env):
	if (os.name=="nt"):
		import subprocess
		if os.name != "nt":
			return  # not needed, only for windows
		env.Replace(ARFLAGS="q")

		def mySubProcess(cmdline, env):
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			popen_args = {
				"stdin": subprocess.PIPE,
				"stdout": subprocess.PIPE,
				"stderr": subprocess.PIPE,
				"startupinfo": startupinfo,
				"shell": False,
				"env": env,
			}
			if sys.version_info >= (3, 7, 0):
				popen_args["text"] = True
			proc = subprocess.Popen(cmdline, **popen_args)
			_, err = proc.communicate()
			rv = proc.wait()
			if rv:
				print(err)
			return rv

		def mySpawn(sh, escape, cmd, args, env):
			newargs = " ".join(args[1:])
			cmdline = cmd + " " + newargs

			rv = 0
			env = {str(key): str(value) for key, value in iter(env.items())}
			if len(cmdline) > 32000 and cmd.endswith("ar"):
				cmdline = cmd + " " + args[1] + " " + args[2] + " "
				for i in range(3, len(args)):
					rv = mySubProcess(cmdline + args[i], env)
					if rv:
						break
			else:
				rv = mySubProcess(cmdline, env)

			return rv

		env["SPAWN"] = mySpawn
	if (os.name=="nt"):
		env['ENV']['TMP'] = os.environ['TMP']
	env.disabled_modules = ['enet']
	devkitpro_path = env.get('devkitpro', "")
	if devkitpro_path == "":
		print("DEVKITPRO PATH NOT SPECIFIED")
		exit(1)
	else:
		print(devkitpro_path)
	devkitarm_path = devkitpro_path + "/devkitARM"
	ctrulib_path = devkitpro_path + "/libctru"
	env.Append(CPPPATH=['#platform/3ds'])
	env["CC"] = devkitarm_path + "/bin/arm-none-eabi-gcc"
	env["CXX"] = devkitarm_path + "/bin/arm-none-eabi-g++"
	env["LD"] = devkitarm_path + "/bin/arm-none-eabi-g++"
	env["AR"] = devkitarm_path + "/bin/arm-none-eabi-ar"
	env["RANLIB"] = devkitarm_path + "/bin/arm-none-eabi-ranlib"
	env["AS"] = devkitarm_path + "/bin/arm-none-eabi-as"

	arch = ['-march=armv6k', '-mtune=mpcore','-mfloat-abi=hard','-mtp=soft' ]
	env.Append(CCFLAGS=['-g','-Wall','-mword-relocations','-ffunction-sections','-Wno-error=incompatible-pointer-types'] + arch)
	env.Append(CPPFLAGS=[ '-fno-rtti', '-fno-exceptions', '-Wno-parentheses','-std=gnu++11'])
	env.Append(CCFLAGS=['-D_3DS', '-DARM11','-D__3DS__','-DNEED_LONG_INT', '-DLIBC_FILEIO_ENABLED','-DNO_SAFE_CAST'])
	env.Append(CPPPATH=[devkitpro_path+"/portlibs/armv6k/include", devkitpro_path +
			   "/portlibs/3ds/include", ctrulib_path + "/include", devkitarm_path + "/arm-none-eabi/include"])
	env.Append(LIBPATH=[devkitpro_path+"/portlibs/armv6k/lib", devkitpro_path +
			   "/portlibs/3ds/lib", ctrulib_path + "/lib", devkitarm_path + "/arm-none-eabi/lib/armv6k/fpu"])

	env.Append(LINKFLAGS=['-specs=3dsx.specs', '-g'] + arch)
	env.Append(LIBS=["citro3d", "ctru","png","z"])
   
	if (env["target"] == "release"):
		if (env["debug_release"] == "yes"):
			env.Append(CCFLAGS=['-g2'])
		else:
			env.Append(CCFLAGS=['-O3'])
	elif (env["target"] == "release_debug"):
		env.Append(CCFLAGS=['-O2', '-ffast-math', '-DDEBUG_ENABLED'])
		if (env["debug_release"] == "yes"):
			env.Append(CCFLAGS=['-g2'])
	elif (env["target"] == "debug"):
		env.Append(CCFLAGS=['-O3','-g2','-Wall',
				   '-DDEBUG_ENABLED', '-DDEBUG_MEMORY_ENABLED'])

