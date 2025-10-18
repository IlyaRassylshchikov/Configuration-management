@echo off
REM Тестирование Этапа 5
REM Автор: IlyaRassylshchikov

echo ============================================================
echo    Testing Stage 5: Additional Commands
echo ============================================================
echo.

if not exist tests\vfs_archives\complex_vfs.zip (
    echo Создание тестовых VFS архивов...
    python scripts\create_vfs_archives.py
    echo.
)

echo ============================================================
echo Test 1: Command chown (change of owner)
echo ============================================================
(
echo ls -l
echo chown alice README.md
echo ls -l README.md
echo chown bob:developers etc/config.json
echo ls -l etc/config.json
echo chown -R dave:admins home/user
echo ls -l home/user
echo chown alice nonexistent.txt
echo exit
) | python shell_emulator.py --vfs tests\vfs_archives\complex_vfs.zip

echo.
echo ============================================================
echo Test 2: Command rm (deleting files)
echo ============================================================
(
echo cd /tmp
echo ls
echo rm temp1.txt
echo ls
echo cd /
echo rm tmp
echo exit
) | python shell_emulator.py --vfs tests\vfs_archives\complex_vfs.zip

echo.
echo ============================================================
echo Test 3: Command rm -r (deleting directories)
echo ============================================================
(
echo ls
echo rm -r tmp
echo ls
echo cd /home/user
echo ls
echo rm -r documents
echo ls
echo exit
) | python shell_emulator.py --vfs tests\vfs_archives\complex_vfs.zip

echo.
echo ============================================================
echo Test 4: rm -f (forced deletion)
echo ============================================================
(
echo rm nonexistent.txt
echo rm -f nonexistent.txt
echo exit
) | python shell_emulator.py --vfs tests\vfs_archives\complex_vfs.zip

echo.
echo ============================================================
echo Test 5: Error handling
echo ============================================================
(
echo chown
echo chown owner
echo rm
echo rm -rf /
echo exit
) | python shell_emulator.py --vfs tests\vfs_archives\complex_vfs.zip

echo.
echo ============================================================
echo Test 6: Full test with script
echo ============================================================
python shell_emulator.py --vfs tests\vfs_archives\complex_vfs.zip --startup tests\test_scripts\test_stage5_full.sh

echo.
echo ============================================================
echo    ALL STAGE 5 TESTS COMPLETED!
echo ============================================================
pause