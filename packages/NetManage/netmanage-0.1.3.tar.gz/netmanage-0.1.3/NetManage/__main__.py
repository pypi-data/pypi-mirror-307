import argparse
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from utils import SSH_CONNECTION, TELNET_CONNECTION, COM_CONNECTION, TFTP_CONNECTION, read_nmconn, create_nmconn


def read_config(connection: str, output_file: str | None, show_config: bool | None):
    connection = read_nmconn(connection)

    if connection.METHOD != "TFTP":
        connection_data = connection.getNetmikoConnDict()

        net_connect = ConnectHandler(**connection_data)

        if (connection_data['device_type'].startswith('cisco_') or
            connection_data['device_type'].startswith('juniper_') or
            connection_data['device_type'].startswith('fortinet_')) and \
                connection_data['secret']:
            net_connect.enable()

        if connection_data['device_type'].startswith('cisco_'):
            command = 'show running-config'
        elif connection_data['device_type'].startswith('juniper_'):
            command = 'show configuration'
        elif connection_data['device_type'].startswith('hp_'):
            command = 'display current-configuration'
        elif connection_data['device_type'].startswith('fortinet_'):
            command = 'show'
        elif connection_data['device_type'].startswith('ubiquiti_'):
            command = 'show configuration'
        elif connection_data['device_type'].startswith('mikrotik_'):
            command = '/export'
        elif connection_data['device_type'].startswith('paloalto_'):
            command = 'show config running'
        else:
            raise ValueError("Unsupported device type")

        output = net_connect.send_command(command)
        if show_config:
            print(output)

        if output is not None:
            with open(output_file, 'w+') as f:
                f.write(output)

        net_connect.disconnect()

def create_connection(name, output, method, device, ip, port, username, password, exec, baudrate):
    try:
        if not((method == "COM" and port is not None and baudrate is not None) or ((method == "SSH" or method == "TELNET") and ip is not None and port is not None and (username is not None or method == "TELNET") and password is not None)):
            raise AttributeError("Method must be either COM or SSH or TELNET and certain data need to be provided.")
        create_nmconn(name, output, method, device, ip, port, username, password, exec, baudrate)
        print("Success")
    except Exception as e:
        print(e)
        print("Fail")

def test_connection(connectionFile):
    conn = read_nmconn(connectionFile)
    connection_data = conn.getNetmikoConnDict()

    try:
        connection = ConnectHandler(**connection_data)
        print("Success")
        connection.disconnect()

    except NetmikoTimeoutException:
        print("Error: request timed out")

    except NetmikoAuthenticationException:
        print("Error: wrong login or password")

    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='NetManage')
    subparsers = parser.add_subparsers(dest='command')

    # Read conf
    parser_read_config = subparsers.add_parser('read-config', help='Read config file')
    parser_read_config.add_argument('-c', '--connection', type=str, required=True, help='Path to .nmconn file')
    parser_read_config.add_argument('-o', '--output', type=str, required=False, help='Path to output .txt file')
    parser_read_config.add_argument('-s', '--show-config', type=bool, required=False, help='Show output in console')

    # create .nmconn file

    parser_create_connection = subparsers.add_parser('create-conn', help='Create connection')
    parser_create_connection.add_argument('-n', '--name', type=str, required=True, help='Connection name')
    parser_create_connection.add_argument('-o', '--output', type=str, required=True, help='Path to .nmconn file')
    parser_create_connection.add_argument('-m', '--method', type=str, required=True, help='Method: SSH, TELNET, COM, TFTP')
    parser_create_connection.add_argument('-d', '--device', type=str, required=True, help='Device_type z bilbioteki netmiko')
    parser_create_connection.add_argument('-i', '--ip', type=str, required=False, help='[SSH/TELNET] Host')
    parser_create_connection.add_argument('-po', '--port', type=str, required=False, help='[SSH/TELNET/COM] PORT')
    parser_create_connection.add_argument('-b', '--baudrate', type=int, required=False, help='[COM] Baudrate')
    parser_create_connection.add_argument('-u', '--username', type=str, required=False, help='[SSH/TELNET] Username')
    parser_create_connection.add_argument('-pa', '--password', type=str, required=False, help='[SSH/TELNET] Password')
    parser_create_connection.add_argument('-e', '--exec', type=str, required=False, help='[SSH/TELNET/COM] EXEC')

    # test connection

    parser_test_connection = subparsers.add_parser('test-conn', help='Test connection')
    parser_test_connection.add_argument('-c', '--connection', type=str, required=True, help='Path to .nmconn file')

    args = parser.parse_args()

    if args.command == "read-config":
        print(
            args.connection, args.output, args.show_config
        )

        read_config(args.connection, args.output, args.show_config)
    elif args.command == "create-conn":
        print(
            args.name, args.output, args.method, args.device, args.ip, args.port, args.username, args.password, args.exec, args.baudrate
        )

        create_connection(args.name, args.output, args.method, args.device, args.ip, args.port, args.username, args.password, args.exec, args.baudrate)
    elif args.command == "test-conn":
        test_connection(args.connection)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
