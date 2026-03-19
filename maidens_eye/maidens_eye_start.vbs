Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pyw -3 app.py", 0, False
Set WshShell = Nothing
