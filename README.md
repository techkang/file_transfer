# file transfer
A simple file transfer tool.

# install

    pip install flask werkzeug
    export user_python="$(which python)"
    sudo $user_python app.py

## run on background
Usually, we want to run this scripts on background. You can using 
following command.

    nohup sudo $user_python app.py > /dev/null 2>&1 &
    
## run on boot
If you are using Ubuntu 18.04 or latter, you can add your command 
in `/etc/rc.local` and refer to [https://www.linuxbabe.com/linux-server/how-to-enable-etcrc-local-with-systemd](https://www.linuxbabe.com/linux-server/how-to-enable-etcrc-local-with-systemd).

# usage

using `ip addr` command to get your ip address and visit `http://your_ip_address`.
