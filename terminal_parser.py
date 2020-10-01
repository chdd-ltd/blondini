"""


"""

def terminal_parser(command, terminal_rows, session, display=False):

    prompt = session[1]['prompt']

    if command.startswith('pwd'):
        pwd = parse_list(prompt, terminal_rows, display=display)
        session.append({f'{command}': pwd})

    if command.startswith('printenv'):
        printenv_array = parse_list(prompt, terminal_rows, display=display)
        # print(f'printenv_array:{type(printenv_array)}')
        printenv = {}
        for line in printenv_array:
            x = line.split('=')
            if x[0].isupper():
                if len(x) == 2:
                    printenv[x[0]] = x[1]
                else:
                    # print(f'{x}')
                    _ = ''
                    for i in range(1, len(x), 1):
                        if i < len(x)-1:
                            _ += x[i] + '='
                        else:
                            _ += x[i]
                    printenv[x[0]] = _
                    # print(f'{x[0]} -> {_}')

        session.append({f'printenv': printenv})

    # if command.startswith('find'):
    #     find = parse_list(session[1]["prompt"], terminal_rows, display=True)
    #     session.append({f'{command}': find})
    #
    #
    # if command.startswith('ls'):
    #     ls = parse_list(session[1]["prompt"], terminal_rows, display=True)
    #     session.append({f'{command}': ls})
    #     for i, row in enumerate(ls):
    #         # print(f'{i:>2} : {row}')
    #
    #         if '.bash_history' in row:
    #             words = row.split()
    #             if int(words[4]) > 1:
    #                 commands.append('cat .bash_history #less')
    #                 # print(f'words[4] : {words[4]}')
    #
    #         if row.endswith('.ssh'):
    #             if 'ls -la .ssh/' not in commands:
    #                 commands.append('ls -la .ssh/')
    #
    #         # if row.endswith('authorized_keys') and 'authorized_keys' not in commands:
    #         #     commands.append('cat .ssh/authorized_keys')
    #         # if row.endswith('id_rsa') and 'id_rsa' not in commands:
    #         #     commands.append('cat .ssh/id_rsa #less')
    #         # if row.endswith('id_rsa.pub') and 'id_rsa.pub' not in commands:
    #         #     commands.append('cat .ssh/id_rsa.pub #less')
    #
    # if command.startswith('cat'):
    #     cat = parse_list(session[1]["prompt"], terminal_rows, display=True)
    #     session.append({f'{command}': cat})
    #
    #     if command == 'cat /etc/passwd #less':
    #         for i, e in enumerate(cat):
    #             user = e.split(':')
    #             users.append(user[0])
    #         users.sort()
    #         session.append({f'users': users})
    #
    # if command.startswith('id'):
    #     id = parse_id(session[1]["prompt"], terminal_rows, display=True)
    #     session.append({f'{command}': id})
    #
    # if command.startswith('uname'):
    #     uname = parse_uname(session[1]["prompt"], terminal_rows, display=True)
    #     session.append({f'{command}': uname})
    #
    # if command.startswith('ifconfig'):
    #     ifconfig = parse_ifconfig(session[1]["prompt"], terminal_rows, display=True)
    #     session.append({f'{command}': ifconfig})
    #
    # if 'resolv' in command:
    #     resolv = parse_resolv(session[1]["prompt"], terminal_rows, display=True)
    #     session.append({f'{command}': resolv})
    #
    # if 'netstat' in command:
    #     netstat = parse_netstat(session[1]["prompt"], terminal_rows, display=True)
    #     session.append({f'{command}': netstat})
    #
    # if command.startswith('ps') and len(users) > 0:
    #     ps = parse_ps(session[1]["prompt"], terminal_rows, users, display=True)
    #     session.append({f'{command}': ps})
    #
    # # return command_output


# def parse_ps(session[1]["prompt"], terminal_rows, users, display=False):
#     tmp = ''
#     for i, row in enumerate(terminal_rows):
#         tmp = tmp + row
#
#     users.remove('dnsmasq')
#     users.remove('daemon')
#     users.remove('lightdm')
#     users.append('systemd+')
#     users.append('message+')
#
#     # print(f'tmp:{tmp}')
#     for user in users:
#         old = user + ' '
#         new = '\n' + user + ' '
#         # print(f'old:{old} new:{new}')
#         tmp = tmp.replace(old, new)
#
#     tmp = tmp.replace('ch\nroot', 'chroot')
#     tmp = tmp.replace('novtswitchroot', 'novtswitch\nroot')
#     tmp = tmp.replace('/usr/sbin/\nsshd', '/usr/sbin/sshd')
#     tmp = tmp.replace('/usr/bin/\nwhoopsie', '/usr/bin/whoopsie')
#
#     # print(f'tmp:{tmp}')
#     command_output = tmp.split('\n')
#     # print(f'command_output:{command_output}')
#
#     if display:
#         for i, e in enumerate(command_output):
#             print(f'{i:>3} : {e}')
#
#     return command_output
#
#
# def parse_netstat(session[1]["prompt"], terminal_rows, display=False):
#     states = ['ESTABLISHED', 'SYN_SENT', 'SYN_RECV', 'FIN_WAIT1', 'FIN_WAIT2', 'TIME_WAIT',
#               'CLOSE', 'CLOSE_WAIT', 'LAST_ACK', 'LISTEN', 'CLOSING', 'UNKNOWN']
#
#     command_output = []
#     for i, e in enumerate(terminal_rows):
#         # print(f'{i} : {e}')
#         for state in states:
#             if e.endswith(state):
#                 command_session.append(terminal_rows[i] + ' ' + terminal_rows[i+1])
#
#     if display:
#         for i, e in enumerate(command_output):
#             print(f'{i:>3} : {e}')
#
#     return command_output
#
#
# def parse_resolv(session[1]["prompt"], terminal_rows, display=False):
#     tmp = []
#     resolv = {}
#
#     command_output = parse_list(session[1]["prompt"], terminal_rows, display=False)
#
#     # command_output = []
#     # for row in terminal_rows:
#     #     if prompt not in row:
#     #         if len(row) == 79:
#     #             command_session.append(row + ' ')
#     #         else:
#     #             command_session.append(row)
#
#     for line in command_output:
#         if not line.startswith('#'):
#             if prompt not in line:
#                 tmp.append(line)
#
#     if len(tmp) > 0:
#         for e in tmp:
#             _ = e.split()
#             resolv[_[0]] = _[1]
#
#     if display:
#         for k, v in resolv.items():
#             print(f'{k:>12} : {v}')
#
#     return resolv
#
#
# def parse_ifconfig(session[1]["prompt"], terminal_rows, display=False):
#     command_output = parse_list(session[1]["prompt"], terminal_rows, display=False)
#     ifconfig = []
#     # command_output = []
#     # for row in terminal_rows:
#     #     # print(f'{row}')
#     #     if prompt not in row:
#     #         if len(row) == 79:
#     #             command_session.append(row + ' ')
#     #         else:
#     #             command_session.append(row)
#
#     interface = {}
#     for i, line in enumerate(command_output):
#         line_array = line.split()
#         # print(f'{i}:{line_array}')
#
#         if 'flags' in line:
#             if len(interface) > 0:
#                 ifconfig.append(interface)
#
#             interface = {}
#             interface['iface'] = line_array[0]
#             interface['flags'] = line_array[1]
#             interface['mtu'] = line_array[3]
#
#         if 'inet' in line:
#             interface['inet'] = line_array[1]
#             interface['netmask'] = line_array[3]
#             if len(line_array) == 6:
#                 interface['broadcast'] = line_array[5]
#
#         if 'ether' in line:
#             interface['ether'] = line_array[1]
#             interface['txqueueln'] = line_array[3]
#
#         if 'RX packets' in line:
#             interface['RX'] = {}
#             interface['RX']['packets'] = line_array[2]
#             interface['RX']['bytes'] = line_array[4]
#
#         if 'RX errors' in line:
#             interface['RX']['errors'] = line_array[2]
#             interface['RX']['dropped'] = line_array[4]
#             interface['RX']['overruns'] = line_array[6]
#             interface['RX']['frame'] = line_array[8]
#
#         if 'TX packets' in line:
#             interface['TX'] = {}
#             interface['TX']['packets'] = line_array[2]
#             interface['TX']['bytes'] = line_array[4]
#
#         if 'TX errors' in line:
#             interface['TX']['errors'] = line_array[2]
#             interface['TX']['dropped'] = line_array[4]
#             interface['TX']['overruns'] = line_array[6]
#             interface['TX']['carrier'] = line_array[8]
#             interface['TX']['collisions'] = line_array[10]
#
#     ifconfig.append(interface)
#
#     if display:
#         # print(f'ifconfig:{ifconfig}')
#         for i, iface in enumerate(ifconfig):
#             print(f'interface : {i}')
#             for k, v, in iface.items():
#                 print(f'{k:>12} : {v}')
#
#     return ifconfig
#
#
# def parse_uname(session[1]["prompt"], terminal_rows, display=False):
#
#     command_output = parse_list(session[1]["prompt"], terminal_rows, display=False)
#     print(f'parse_uname:command_output:{command_output}')
#
#     command_output_string = ''
#     for line in command_output:
#         command_output_string += line + ' '
#         # command_output_string += ' '
#     print(f'parse_uname:command_output_string:{command_output_string}')
#     command_output_string = command_output_string.replace('2020x86_64', '2020 x86_64')
#     command_output_array = command_output_string.split()
#     print(f'parse_uname:command_output_array:{command_output_array}')
#
#     uname = {}
#     uname['kernel_name'] = command_output_array[0]
#     uname['nodename'] = command_output_array[1]
#     uname['kernel_release'] = command_output_array[2]
#     kernel_version = ''
#     for i in range(3, 11, 1):
#         kernel_version += command_output_array[i] + ' '
#     uname['kernel_version'] = kernel_version
#     uname['machine'] = command_output_array[-4]
#     uname['processor'] = command_output_array[-3]
#     uname['hardware_platform'] = command_output_array[-2]
#     uname['operating_system'] = command_output_array[-1]
#
#     if display:
#         for key, value in uname.items():
#             print(f'{key:>20} : {value}')
#
#     return uname
#
#
# def parse_id(session[1]["prompt"], terminal_rows, display=False):
#
#     command_output = parse_list(session[1]["prompt"], terminal_rows, display=False)
#
#     command_output_string = ''
#     for line in command_output:
#         command_output_string += line
#         command_output_string += ' '
#
#     # print(f'parse_id:command_output_string:{command_output_string}')
#
#     command_output_string = command_output_string.replace(' ', '-')
#     command_output_string = command_output_string.replace(')-', ',')
#     # print(f'command_output_string:{command_output_string}')
#
#     command_output_array = command_output_string.split(',')
#     # print(f'command_output_array:{command_output_array}')
#
#     id = {}
#     _ = command_output_array[0]
#     _ = _[8:]
#     _ = _.replace('(', '')
#     _ = _.replace(')', '')
#     id['username'] = _
#
#     id['uid'] = command_output_array[0][4:8]
#     id['gid'] = command_output_array[1][4:8]
#
#     tmp = command_output_array[2:]
#     tmp[0] = tmp[0].replace('groups=', '')
#     id['groups'] = tmp
#
#     if display:
#         for key, value in id.items():
#             if key == 'groups':
#                 print(f'{key:>12} : ')
#                 print('\t\t\t\t', end='')
#                 for i, e in enumerate(value):
#                     if i != 0 and i % 3 == 0:
#                         print(f'{e} ')
#                         print('\t\t\t\t', end='')
#                     else:
#                         print(f'{e} ', end='')
#             else:
#                 print(f'{key:>12} : {value}')
#         print('')
#
#     return id
#

def parse_list(prompt, terminal_rows, display=False):
    """
    turn the terminal row and column output into a string
    line array, taking into account line wraps at column 80

    :param prompt:
    :param terminal_rows:
    :param display:
    :return:
    """
    command_output = []
    # for i, row in enumerate(terminal_rows):
    for i in range(0, len(terminal_rows), 1):
        if i < len(terminal_rows):
            if prompt not in terminal_rows[i]:
                if len(terminal_rows[i]) == 80:
                    # print(f'80 {i:<3} : {terminal_rows[i]} -> {terminal_rows[i+1]}')
                    command_output.append(terminal_rows[i] + terminal_rows[i+1])
                    terminal_rows.pop(i+1)
                    # print(f'80 {i:<3} : {command_output[-1]}')
                else:
                    # print(f'{i:>3} : {terminal_rows[i]}')
                    command_output.append(terminal_rows[i])

    if display:
        for i, e in enumerate(command_output):
            print(f'{i:<3} : {e}')

    return command_output

