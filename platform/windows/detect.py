

import os

import sys	


def is_active():
	return True
		
def get_name():
		return "Windows"

def can_build():
	if os.name=="nt":
		#building natively on windows!
		if (os.getenv("VSINSTALLDIR")):
			return True 
		else:
			return True
	if os.name == "posix":
		# Cross-compiling with MinGW-w64 (old MinGW32 is not supported)
		mingw = "i586-mingw32msvc-"
		mingw64 = "i686-w64-mingw32-"
		if (os.getenv("MINGW32_PREFIX")):
			mingw=os.getenv("MINGW32_PREFIX")
		if (os.getenv("MINGW64_PREFIX")):
			mingw64=os.getenv("MINGW64_PREFIX")
		if os.system(mingw+"gcc --version >/dev/null") == 0 or os.system(mingw64+"gcc --version >/dev/null") ==0:
			return True

def get_opts():
	mingw=""
	mingw64=""
	if (os.name!="nt"):
		mingw = "i586-mingw32msvc-"
		mingw64 = "i686-w64-mingw32-"
		if (os.getenv("MINGW32_PREFIX")):
			mingw=os.getenv("MINGW32_PREFIX")
		if (os.getenv("MINGW64_PREFIX")):
			mingw64=os.getenv("MINGW64_PREFIX")

	return [
		('mingw_prefix','Mingw Prefix',mingw),
		('mingw_prefix_64','Mingw Prefix 64 bits',mingw64),
		('mingw64_for_32','Use Mingw 64 for 32 Bits Build',"no"),
	]
  
def get_flags():
	return [
		('freetype','builtin'), #use builtin freetype
		('openssl','builtin'), #use builtin openssl
		('theora','no'),
	]
			


def configure(env):

	env.Append(CPPPATH=['#platform/windows'])

	if (os.name=="nt" and os.getenv("VCINSTALLDIR")!=None):
		#build using visual studio
		env['ENV']['TMP'] = os.environ['TMP']
		env.Append(CPPPATH=['#platform/windows/include'])
		env.Append(LIBPATH=['#platform/windows/lib'])

		if (env["freetype"]!="no"):
			env.Append(CCFLAGS=['/DFREETYPE_ENABLED'])
			env.Append(CPPPATH=['#tools/freetype'])
			env.Append(CPPPATH=['#tools/freetype/freetype/include'])

		if (env["target"]=="release"):

			env.Append(CCFLAGS=['/O2'])
			env.Append(LINKFLAGS=['/SUBSYSTEM:WINDOWS'])
			env.Append(LINKFLAGS=['/ENTRY:mainCRTStartup'])

		elif (env["target"]=="release_debug"):

			env.Append(CCFLAGS=['/O2','/DDEBUG_ENABLED'])
			env.Append(LINKFLAGS=['/SUBSYSTEM:CONSOLE'])

		elif (env["target"]=="debug"):

			env.Append(CCFLAGS=['/Zi','/DDEBUG_ENABLED','/DDEBUG_MEMORY_ENABLED','/DD3D_DEBUG_INFO','/O1'])
			env.Append(LINKFLAGS=['/SUBSYSTEM:CONSOLE'])
			env.Append(LINKFLAGS=['/DEBUG'])


		env.Append(CCFLAGS=['/MT','/Gd','/GR','/nologo'])
		env.Append(CXXFLAGS=['/TP'])
		env.Append(CPPFLAGS=['/DMSVC', '/GR', ])
		env.Append(CCFLAGS=['/I'+os.getenv("WindowsSdkDir")+"/Include"])
		env.Append(CCFLAGS=['/DWINDOWS_ENABLED'])
		env.Append(CCFLAGS=['/DRTAUDIO_ENABLED'])
		env.Append(CCFLAGS=['/DWIN32'])
		env.Append(CCFLAGS=['/DTYPED_METHOD_BIND'])

		env.Append(CCFLAGS=['/DGLES2_ENABLED'])
		env.Append(CCFLAGS=['/DGLES1_ENABLED'])
		env.Append(CCFLAGS=['/DGLEW_ENABLED'])
		LIBS=['winmm','opengl32','dsound','kernel32','ole32','user32','gdi32', 'IPHLPAPI', 'wsock32', 'shell32','advapi32']
		env.Append(LINKFLAGS=[p+env["LIBSUFFIX"] for p in LIBS])
		
		env.Append(LIBPATH=[os.getenv("WindowsSdkDir")+"/Lib"])
		if (os.getenv("DXSDK_DIR")):
				DIRECTX_PATH=os.getenv("DXSDK_DIR")
		else:
				DIRECTX_PATH="C:/Program Files/Microsoft DirectX SDK (March 2009)"

		if (os.getenv("VCINSTALLDIR")):
				VC_PATH=os.getenv("VCINSTALLDIR")
		else:
				VC_PATH=""

		env.Append(CCFLAGS=["/I" + p for p in os.getenv("INCLUDE").split(";")])
		env.Append(LIBPATH=[p for p in os.getenv("LIB").split(";")])
		env.Append(CCFLAGS=["/I"+DIRECTX_PATH+"/Include"])
		env.Append(LIBPATH=[DIRECTX_PATH+"/Lib/x86"])
		env['ENV'] = os.environ;
	else:

		# Workaround for MinGW. See:
		# http://www.scons.org/wiki/LongCmdLinesOnWin32
		if (os.name=="nt"):
			import subprocess
			if os.name != "nt":
				return  # not needed, only for windows

		# On Windows, due to the limited command line length, when creating a static library
		# from a very high number of objects SCons will invoke "ar" once per object file;
		# that makes object files with same names to be overwritten so the last wins and
		# the library loses symbols defined by overwritten objects.
		# By enabling quick append instead of the default mode (replacing), libraries will
		# got built correctly regardless the invocation strategy.
		# Furthermore, since SCons will rebuild the library from scratch when an object file
		# changes, no multiple versions of the same object file will be present.
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

		#build using mingw
		if (os.name=="nt"):
			env['ENV']['TMP'] = os.environ['TMP'] #way to go scons, you can be so stupid sometimes
		else:
			env["PROGSUFFIX"]=env["PROGSUFFIX"]+".exe"

		mingw_prefix=""

		if (env["bits"]=="default"):
			env["bits"]="32"

		use64=False
		if (env["bits"]=="32"):
			if (env["mingw64_for_32"]=="yes"):
				env.Append(CCFLAGS=['-m32'])
				env.Append(LINKFLAGS=['-m32'])
				env.Append(LINKFLAGS=['-static-libgcc'])
				env.Append(LINKFLAGS=['-static-libstdc++'])
				mingw_prefix=env["mingw_prefix_64"];
			else:
				mingw_prefix=env["mingw_prefix"];
		else:
			mingw_prefix=env["mingw_prefix_64"];
			env.Append(LINKFLAGS=['-static'])

		nulstr=""

		if (os.name=="posix"):
			nulstr=">/dev/null"
		else:
			nulstr=">nul"

		if os.system(mingw_prefix+"gcc --version"+nulstr)!=0:
			#not really super consistent but..
			print("Can't find Windows compiler: "+mingw_prefix)
			sys.exit(255)

		if (env["target"]=="release"):
			
			env.Append(CCFLAGS=['-O3','-ffast-math','-fomit-frame-pointer','-msse2'])
			env.Append(LINKFLAGS=['-Wl,--subsystem,windows'])

		elif (env["target"]=="release_debug"):

			env.Append(CCFLAGS=['-O2','-DDEBUG_ENABLED'])

		elif (env["target"]=="debug"):
					
			env.Append(CCFLAGS=['-g', '-Wall','-DDEBUG_ENABLED','-DDEBUG_MEMORY_ENABLED'])

		if (env["freetype"]!="no"):
			env.Append(CCFLAGS=['-DFREETYPE_ENABLED'])
			env.Append(CPPPATH=['#tools/freetype'])
			env.Append(CPPPATH=['#tools/freetype/freetype/include'])

		env["CC"]=mingw_prefix+"gcc"
		env['AS']=mingw_prefix+"as"
		env['CXX'] = mingw_prefix+"g++"
		env['AR'] = mingw_prefix+"ar"
		env['RANLIB'] = mingw_prefix+"ranlib"
		env['LD'] = mingw_prefix+"g++"

		#env['CC'] = "winegcc"
		#env['CXX'] = "wineg++"

		env.Append(CCFLAGS=['-DWINDOWS_ENABLED','-mwindows'])
		env.Append(CPPFLAGS=['-DRTAUDIO_ENABLED'])
		env.Append(CCFLAGS=['-DGLES2_ENABLED','-DGLES1_ENABLED','-DGLEW_ENABLED'])
		env.Append(LIBS=['mingw32','opengl32', 'dsound', 'ole32', 'd3d9','winmm','gdi32','iphlpapi','wsock32','kernel32'])
		env.Append(CCFLAGS=['-Wno-error=incompatible-pointer-types'])
		if (env["bits"]=="32" and env["mingw64_for_32"]!="yes"):
#			env.Append(LIBS=['gcc_s'])
			#--with-arch=i686
			env.Append(CPPFLAGS=['-march=i686'])
			env.Append(LINKFLAGS=['-march=i686'])




		#'d3dx9d'
		env.Append(CPPFLAGS=['-DMINGW_ENABLED'])
		env.Append(LINKFLAGS=['-g'])

	import methods
	env.Append( BUILDERS = { 'GLSL120' : env.Builder(action = methods.build_legacygl_headers, suffix = 'glsl.h',src_suffix = '.glsl') } )
	env.Append( BUILDERS = { 'GLSL' : env.Builder(action = methods.build_glsl_headers, suffix = 'glsl.h',src_suffix = '.glsl') } )
	env.Append( BUILDERS = { 'HLSL9' : env.Builder(action = methods.build_hlsl_dx9_headers, suffix = 'hlsl.h',src_suffix = '.hlsl') } )
	env.Append( BUILDERS = { 'GLSL120GLES' : env.Builder(action = methods.build_gles2_headers, suffix = 'glsl.h',src_suffix = '.glsl') } )

	

