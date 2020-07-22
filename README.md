# file transfer
A simple file transfer tool.

# usage

    pip install flask werkzeug
    export $user_python="$(which python)"
    sudo $user_python main.py

# run on background
Usually, we want to run this scripts on background. You can using 
following command.

    nohup $user_python main.py > /dev/null 2>&1 &
    
# run on boot
If you are using Ubuntu 18.04 or latter, you can add your command 
in `/etc/rc.local` and refer to [https://www.linuxbabe.com/linux-server/how-to-enable-etcrc-local-with-systemd](https://www.linuxbabe.com/linux-server/how-to-enable-etcrc-local-with-systemd).
