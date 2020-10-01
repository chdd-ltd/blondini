import json


# whoami.json
commands = []

command = {'name': 'printenv',
           'pre-requisite': ['focus'],
           'commands': ['printenv |less'],
           'post-requisite': ['parse:keyvalue']}
commands.append(command)

command = {'name': 'cd home',
           'pre-requisite': ['focus', 'printenv'],
           'commands': ['cd printenv["HOME"]', 'ls'],
           'post-requisite': ['parse:list']}
commands.append(command)

# with open('whoami.json', 'w') as write_file:
#     json.dump(commands, write_file)

session = {}
printenv = {'HOME': '~/'}
session["printenv"] = printenv
print(f'session : {session}')

for c in command['commands']:
    command_string = ''
    components = c.split(' ')
    if len(components) > 1:
        for x in components:
            if '[' in x and ']' in x:
                _ = x.split('[')
                key = _[0]
                _ = x.split('"')
                value = _[1]
                command_string += session[key][value] + ' '
            else:
                command_string += x + ' '
    else:
        command_string += c

    print(f'command_string : {command_string}')

# whatami.json
