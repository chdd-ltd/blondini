# blondini

## setup
python3 -m venv venv; source venv/bin/activate

$ pip install wheel

$ pip install opencv-python

$ pip install opencv-contrib-python

$ pip install pyautogui

## Turn off color in Linux terminal/bash session

echo "$TERM" -> xterm-256color

export TERM=xterm-mono

Better update your ~/.bashrc file with above line:
echo 'export TERM=xterm-mono' >> ~/.bashrc

###~/.bashrc and/or ~/.bash_aliases 

    # alias ls='ls --color=auto'

    # alias dir='dir --color=auto'

    # alias vdir='vdir --color=auto'

    # alias grep='grep --color=auto'

    # alias fgrep='fgrep --color=auto'

    # alias egrep='egrep --color=auto'

###~/.gitconfig

    [color]        

        ui = false

        branch = false

        diff = false

        interactive = false

        status = false

        log = false

    


