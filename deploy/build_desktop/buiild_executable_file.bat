@echo off
:: echo Preparing translations...
:: ..\..\venv\Scripts\pyside6-lupdate "." -target-language en_US -ts "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_en_US.ts"
:: ..\..\venv\Scripts\pyside6-lupdate "." -target-language kk_KZ -ts "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_kk_KZ.ts"
:: ..\..\venv\Scripts\pyside6-lupdate "." -target-language ru_RU -ts "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_ru_RU.ts"
:: echo Preparing translations finished
:: echo

echo Compiling translations...
..\..\venv\Scripts\pyside6-lrelease "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_man_en_US.ts" "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_en_US.ts" -qm "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_en_US.qm"
..\..\venv\Scripts\pyside6-lrelease "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_man_kk_KZ.ts" "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_kk_KZ.ts" -qm "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_kk_KZ.qm"
..\..\venv\Scripts\pyside6-lrelease "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_man_ru_RU.ts" "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_ru_RU.ts" -qm "..\..\desktop_constructor_app\constructor_app\translations\bot_constructor_ru_RU.qm"
echo Compiling translations finished
echo

:: Здесь прописываем полный путь к папке, которую следует добавить к Path
set PATH
:: set set PATH=%PATH%;"..\..\venv\Scripts\"
:: set PATH=%PATH%D:\Git Repos\tg_bot_constructor\desktop_constructor_app\venv\Scripts\
echo "D:\Git Repos\tg_bot_constructor\" added to 'PATH'
:: set PATH
echo %PATH%

echo 'UI-forms and .qrc-files compiling...'
:: ..\..\venv\Scripts\pyside6-project build \
..\..\venv\Scripts\pyside6-uic "..\..\desktop_constructor_app\constructor_app\widgets\login_form.ui" -o "..\..\desktop_constructor_app\constructor_app\widgets\ui_login_form.py"
	
..\..\venv\Scripts\pyside6-uic "..\..\desktop_constructor_app\constructor_app\widgets\sign_up_form.ui" -o "..\..\desktop_constructor_app\constructor_app\widgets\ui_sign_up_form.py"

:: ..\..\venv\Scripts\pyside6-uic "..\..\desktop_constructor_app\constructor_app\widgets\variant_editor_dialog.ui" -o "..\..\desktop_constructor_app\constructor_app\widgets\ui_variant_editor_dialog.py"

:: ..\..\venv\Scripts\pyside6-uic "..\..\desktop_constructor_app\constructor_app\widgets\bot_editor\bot_editor_form.ui" -o \
::     "..\..\desktop_constructor_app\constructor_app\widgets\bot_editor\ui_bot_editor_form.py"
	
:: ..\..\venv\Scripts\pyside6-uic "D:\Git Repos\tg_bot_constructor\desktop_constructor_app\constructor_app\widgets\bot_editor\message_editor_dialog.ui" -o \ "D:\Git Repos\tg_bot_constructor\desktop_constructor_app\constructor_app\widgets\bot_editor\ui_message_editor_dialog.py"
	
:: ..\..\venv\Scripts\pyside6-uic "D:\Git Repos\tg_bot_constructor\desktop_constructor_app\constructor_app\widgets\bot_editor\variant_editor_dialog.ui" -o \ "D:\Git Repos\tg_bot_constructor\desktop_constructor_app\constructor_app\widgets\bot_editor\variant_editor_dialog.py"	
		
:: ..\..\venv\Scripts\pyside6-project build \
::     ..\..\venv\Scripts\pyside6-rcc "D:\Git Repos\tg_bot_constructor\desktop_constructor_app\constructor_app\bot_icons.qrc" -o \
::     "D:\Git Repos\tg_bot_constructor\desktop_constructor_app\constructor_app\rc_bot_icons.py"
echo 'UI-forms and .qrc-files compiling finished'
echo

pause
