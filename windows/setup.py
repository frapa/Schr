import os
import site
import sys
import glob
from cx_Freeze import setup, Executable

siteDir = site.getsitepackages()[1]
includeDllPath = os.path.join(siteDir, "gnome")

# This is the list of dll which are required by PyGI.
# I get this list of DLL using http://technet.microsoft.com/en-us/sysinternals/bb896656.aspx
#   Procedure: 
#    1) Run your from from your IDE
#    2) Command for using listdlls.exe
#        c:/path/to/listdlls.exe python.exe > output.txt
#    3) This would return lists of all dll required by you program 
#       in my case most of dll file were located in c:\python27\Lib\site-packages\gnome 
#       (I am using PyGI (all in one) installer)
#    4) Below is the list of gnome dll I recevied from listdlls.exe result. 

# If you prefer you can import all dlls from c:\python27\Lib\site-packages\gnome folder
# missingDll = glob.glob(includeDllPath + "\\" + '*.dll')

# List of dll I recevied from listdlls.exe result
missingDLL = ['libffi-6.dll',
              'libgirepository-1.0-1.dll',
              'libgio-2.0-0.dll',
              'libglib-2.0-0.dll',
              'libintl-8.dll',
              'libgmodule-2.0-0.dll',
              'libgobject-2.0-0.dll',
              'libzzz.dll',
              'libwinpthread-1.dll',
              'libgtk-3-0.dll',
              'libgdk-3-0.dll',
              'libcairo-gobject-2.dll',
              'libfontconfig-1.dll',
              'libxmlxpat.dll',
              'libfreetype-6.dll',
              'libpng16-16.dll',
              'libgdk_pixbuf-2.0-0.dll',
              'libjpeg-8.dll',
              'libopenraw-7.dll',
              'librsvg-2-2.dll',
              'libpango-1.0-0.dll',
              'libpangocairo-1.0-0.dll',
              'libpangoft2-1.0-0.dll',
              'libharfbuzz-gobject-0.dll',
              'libpangowin32-1.0-0.dll',
              'libwebp-5.dll',
              'libatk-1.0-0.dll',
              'libgnutls-26.dll',
              'libproxy.dll',
              'libp11-kit-0.dll',
              ]


includeFiles = [
	"glade",
	"translations",
	"images"
]
for DLL in missingDLL:
    includeFiles.append((os.path.join(includeDllPath, DLL), DLL))
    # includeFiles.append(DLL) 

# You can import all Gtk Runtime data from gtk folder              
#gtkLibs= ['etc','lib','share']

# You can import only important Gtk Runtime data from gtk folder  
gtkLibs = ['lib\\gdk-pixbuf-2.0',
           'lib\\girepository-1.0',
           'share\\glib-2.0',
           'lib\\gtk-3.0']


for lib in gtkLibs:
    includeFiles.append((os.path.join(includeDllPath, lib), lib))

base = None
if sys.platform == "win32":
    base = "Win32GUI"

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Schr",           	# Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]schr",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     "[TARGETDIR]images\icon.ico",                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}
	
setup(
    name = "Schr",
    version = "1.0",
    description = "Schr",
    options = {'build_exe' : {
        'compressed': True,
        'includes': ["gi", "tkinter", "tkinter.filedialog"],
        'packages': ["gi", "matplotlib.backends.backend_tkagg"],
        'include_files': includeFiles,
    },
		"bdist_msi": {'data': msi_data}
	},
    executables = [
        Executable("schr.py",
                   base=base
                   )
    ]
)