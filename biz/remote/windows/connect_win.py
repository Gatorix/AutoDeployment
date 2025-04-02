import winrm

session = winrm.Session('127.0.0.1', ('bytter.com\\caos', 'cs0307'), transport='ntlm')
cmd = session.run_cmd('ipconfig')
print(cmd.std_out)
