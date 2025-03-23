; Основные настройки
[Setup]
AppName=Kohihausu
AppVersion=1.0.1
AppPublisher=xAI Games
DefaultDirName={pf}\Kohihausu
DefaultGroupName=Kohihausu
OutputDir=C:\kohihausu_release\Output
OutputBaseFilename=Kohihausu_Installer
SetupIconFile=kohihausu.ico
WizardImageFile=banner.bmp
WizardSmallImageFile=small_banner.bmp
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

; Языки
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

; Файлы для установки
[Files]
Source: "C:\kohihausu_release\kohihausu.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\kohihausu_release\kohihausu.ico"; DestDir: "{app}"; Flags: ignoreversion

; Ярлыки
[Icons]
Name: "{group}\Kohihausu"; Filename: "{app}\kohihausu.exe"; IconFilename: "{app}\kohihausu.ico"
Name: "{commondesktop}\Kohihausu"; Filename: "{app}\kohihausu.exe"; IconFilename: "{app}\kohihausu.ico"; Tasks: desktopicon

; Задачи
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

; Компоненты
[Components]
Name: "main"; Description: "Основные файлы игры"; Types: full compact custom; Flags: fixed
Name: "desktopicon"; Description: "Ярлык на рабочем столе"; Types: full custom

; Кастомные сообщения
[Messages]
WelcomeLabel1=Добро пожаловать в Kohihausu!
WelcomeLabel2=Установите или обновите игру на вашем компьютере.
FinishedLabel=Готово! Запустите игру командой "kohihausu" или через ярлык.

; Код для установки/обновления
[Code]
var
  InstalledVersion: string;
  IsUpdate: Boolean;

function InitializeSetup(): Boolean;
var
  RegResult: Boolean;
begin
  // Проверяем, установлена ли игра, и получаем текущую версию
  RegResult := RegQueryStringValue(HKEY_LOCAL_MACHINE, 
                                   'Software\Microsoft\Windows\CurrentVersion\Uninstall\Kohihausu', 
                                   'DisplayVersion', 
                                   InstalledVersion);
  if RegResult then
  begin
    IsUpdate := True;
    if CompareStr(InstalledVersion, '{#SetupSetting("AppVersion")}') >= 0 then
    begin
      if MsgBox('У вас уже установлена версия ' + InstalledVersion + ' или новее. Хотите переустановить?', 
                mbConfirmation, MB_YESNO) = IDNO then
      begin
        Result := False;
        Exit;
      end;
    end;
  end
  else
    IsUpdate := False;
  Result := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  SavePath: string;
  BatFile: string;
  ResultCode: Integer;
begin
  if CurStep = ssInstall then
  begin
    if IsUpdate then
    begin
      // Останавливаем игру, если она запущена
      if Exec('taskkill', '/IM kohihausu.exe /F', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
      begin
        if ResultCode <> 0 then
          MsgBox('Не удалось завершить процесс игры. Закройте Kohihausu вручную и повторите установку.', mbError, MB_OK);
      end;
    end;
  end;

  if CurStep = ssPostInstall then
  begin
    // Создаём папку для сохранений
    SavePath := ExpandConstant('{userdocs}\My Games\Kohihausu');
    ForceDirectories(SavePath);

    // Создаём bat-файл для команды kohihausu
    BatFile := ExpandConstant('{win}\kohihausu.bat');
    SaveStringToFile(BatFile, '@echo off' + #13#10 +
                     'cd "' + ExpandConstant('{app}') + '"' + #13#10 +
                     'kohihausu.exe', False);  // Убрали start, чтобы запуск был в текущем терминале

    // Регистрируем переменную окружения для сохранений в реестре
    RegWriteStringValue(HKEY_LOCAL_MACHINE, 
                        'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 
                        'KOHIHAUSU_SAVES', 
                        SavePath);

    // Применяем переменную окружения сразу через setx
    Exec('setx', 'KOHIHAUSU_SAVES "' + SavePath + '" /M', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    if ResultCode <> 0 then
      MsgBox('Не удалось применить переменную окружения сразу. Перезагрузите компьютер.', mbInformation, MB_OK);

    // Записываем версию в реестр
    RegWriteStringValue(HKEY_LOCAL_MACHINE, 
                        'Software\Microsoft\Windows\CurrentVersion\Uninstall\Kohihausu', 
                        'DisplayVersion', 
                        '{#SetupSetting("AppVersion")}');
    RegWriteStringValue(HKEY_LOCAL_MACHINE, 
                        'Software\Microsoft\Windows\CurrentVersion\Uninstall\Kohihausu', 
                        'DisplayName', 
                        'Kohihausu');
    RegWriteStringValue(HKEY_LOCAL_MACHINE, 
                        'Software\Microsoft\Windows\CurrentVersion\Uninstall\Kohihausu', 
                        'UninstallString', 
                        ExpandConstant('"{app}\unins000.exe"'));

    // Сообщение об успешной установке или обновлении
    if IsUpdate then
      MsgBox('Kohihausu успешно обновлён до версии ' + '{#SetupSetting("AppVersion")}' + '!', mbInformation, MB_OK)
    else
      MsgBox('Kohihausu успешно установлен! Версия: ' + '{#SetupSetting("AppVersion")}', mbInformation, MB_OK);
  end;
end;