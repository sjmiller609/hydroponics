## after formatting raspi:

- add "ssh" file to /boot
- boot raspi
- ssh to machine
- change password
- ssh-key gen
- add ~/.ssh/id_rsa.pub as r/w deploy key in github
- clone this repo, cd into it
- sudo /bin/bash setup.sh

## start monitor

```
tmux
python
```

- interpreter starts...

```
from moisture_monitor import HydrationMonitor
monitor = HydrationMonitor([0])#listen only channel zero
```

- now press "control+b", then "d"
- results logged to "hydration.csv"

## troubleshooting

- [ADC userguide](http://alchemy-power.com/wp-content/uploads/2017/03/Pi-16ADC-User-Guide.pdf)
- [ADC downloads](http://alchemy-power.com/downloads)
