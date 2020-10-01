import json

# commands = ['id', 'pwd', 'ls -la #less']
# commands = ['ifconfig #less', 'cat /etc/resolv.conf', 'netstat -netapl #less']   # network
# commands = ['cat /etc/passwd #less', 'ps -ef #less']    # running processes
# cat /etc/ssh/sshd_config
# commands = ['find / -type f -perm -4000 -print 2>/dev/null #less']
# commands = ['uname -a']

# whoami.json
actions = []
action = {'name': 'setup',
          'pre_requisites': ['minimise_idea', 'coordinates'],
          'commands': [],
          'post_requisites': []}
actions.append(action)
action = {'name': 'printenv',
          'pre_requisites': ['focus', 'prompt'],
          'commands': ['enter', 'clear', 'printenv |less'],
          'post_requisites': ['printenv']}
actions.append(action)
action = {'name': 'id',
          'pre_requisites': [],
          'commands': ['enter', 'clear', 'id'],
          'post_requisites': []}
actions.append(action)

with open('whoami.json', 'w') as write_file:
    json.dump(actions, write_file)

# whatami.json
