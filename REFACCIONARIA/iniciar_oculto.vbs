' Script VBS para ejecutar Refaccionaria completamente en segundo plano
' Sin mostrar ninguna ventana de terminal
' El proceso continúa ejecutándose incluso después de cerrar este script

Set objShell = CreateObject("WScript.Shell")
strPath = WScript.ScriptFullName
Set objFSO = CreateObject("Scripting.FileSystemObject")
strFolder = objFSO.GetParentFolderName(strPath)

' Detectar si pythonw.exe está disponible
Dim objExec, bPythonW
On Error Resume Next
Set objExec = objShell.Exec("pythonw.exe --version")
bPythonW = (Err.Number = 0)
On Error Goto 0

' Ejecutar de manera silenciosa sin ventana
If bPythonW Then
    ' Si pythonw existe, usarlo (mejor opción)
    objShell.Run "pythonw.exe """ & strFolder & "\launch_desktop.py""", 0, False
Else
    ' Alternativa: usar python con ocultamiento de ventana
    objShell.Run "python """ & strFolder & "\launch_desktop.py""", 0, False
End If

' El script termina aquí, pero el proceso Python continúa ejecutándose
WScript.Quit 0
