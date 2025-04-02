call winrm quickconfig -quiet
call winrm set winrm/config/service/auth @{Basic="true"}
call winrm set winrm/config/service @{AllowUnencrypted="true"}