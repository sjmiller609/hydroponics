while [ 1 ]
do
ansible-playbook -i ./hosts.yml ./deploy.yml --tag check
sleep 60
done
