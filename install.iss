#define MyAppName "NL2Elem Converter"
#define MyAppName "NL2Elem Converter"
#define MyAppVersion "1.0"
#define MyAppPublisher "Luke Hobbs"
#define MyAppURL "https://github.com/lukehobbs/NL2Elem_Converter"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={commonpf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\nl2elem_converter.exe
OutputDir=.\Output
OutputBaseFilename=nl2elem_converter_setup
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\nl2elem_converter.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\nl2elem_converter.exe"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\nl2elem_converter.exe"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\*.*"
