## after formatting raspi:

- add "ssh" file to /boot
- boot raspi
- ssh to machine
- change password
- add to ansible inventory
- start VM to use as an ansible control node

```
vagrant up
```
- cd /vagrant/monitor

```
ansible-playbook -i ./hosts.yml ./deploy.yml
```

## troubleshooting

- [ADC userguide](http://alchemy-power.com/wp-content/uploads/2017/03/Pi-16ADC-User-Guide.pdf)
- [ADC downloads](http://alchemy-power.com/downloads)
