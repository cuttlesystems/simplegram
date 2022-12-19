
#!/bin/bash

#ssh ubuntu@77.240.38.65 'sudo -Sv' < ~/scripts/77.240.38.65pass.txt '&& bash -s' < ~/scripts/docreg_login.sh < ~/scripts/docreg_password.txt

#ssh ubuntu@77.240.38.65 'sudo -Sv' < ~/scripts/77.240.38.65pass.txt '&& bash -s' -- < ~/scripts/docreg_login.sh "$(cat ~/scripts/docreg_password.txt) $(cat ~/scripts/docreg_password.txt)"
#cat ~/scripts/77.240.38.65pass.txt |

# не работает(zsh:1: bad pattern: et7m(gpFbuia):
#ssh ubuntu@77.240.38.65 'sudo -Sv -- '$(cat ~/scripts/77.240.38.65pass.txt)' && bash -s' -- < ~/scripts/docreg_login.sh "$(cat ~/scripts/docreg_password.txt) $(cat ~/scripts/docreg_password.txt)"
#ssh ubuntu@77.240.38.65 'sudo -Sv '$(cat ~/scripts/77.240.38.65pass.txt)' && bash -s' -- < ~/scripts/docreg_login.sh "$(cat ~/scripts/docreg_password.txt) $(cat ~/scripts/docreg_password.txt)"

#рабочие варианты:
#ssh ubuntu@77.240.38.65 'echo "et7m(gpFbuia" | sudo -Sv && bash -s' -- < ~/scripts/docreg_login.sh "$(cat ~/scripts/docreg_password.txt) $(cat ~/scripts/docreg_password.txt)"
#ssh ubuntu@77.240.38.65 'bash -s' -- < ~/scripts/docreg_login.sh "$(cat ~/scripts/docreg_password.txt) $(cat ~/scripts/docreg_password.txt)"
#ssh ubuntu@77.240.38.65 'bash -s '$(cat ~/scripts/docreg_password.txt)' '$(cat ~/scripts/docreg_password.txt)'' -- < ~/scripts/docreg_login.sh

# works
#ssh ubuntu@185.146.3.196 'bash -s '$(cat ~/scripts/docreg_password.txt)' '$(cat ~/scripts/docreg_password.txt)'' -- < ~/scripts/docreg_login.sh
#ssh ubuntu@185.146.3.196 'bash -s -- '$(cat ~/scripts/docreg_password.txt)'' -- $(cat ~/scripts/docreg_password.txt) < ~/scripts/docreg_login.sh


# To Do: адрес сервера вынести либо в переменную окружения, либо в конфигурационный файл
ssh ubuntu@185.146.3.196 'bash -s '$(cat ~/scripts/docreg_password.txt)' '$(cat ~/scripts/docreg_password.txt)'' -- < ~/scripts/docreg_login.sh

exit 0
