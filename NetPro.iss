
#define MyAppName "NetPro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "EffyDoe21"
#define MyAppExeName "NetPro.exe"

[Setup]
AppId={{B79C6D51-9E48-4A91-8B73-3D2F1E9C605A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

OutputDir=installer
OutputBaseFilename=NetPro_Setup

; Icono personalizado del instalador
SetupIconFile=assets\netpro.ico

Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Files]
Source: "dist\NetPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\NetPro"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\netpro.ico"
Name: "{autodesktop}\NetPro"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\netpro.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Ejecutar NetPro"; Flags: nowait postinstall skipifsilent
