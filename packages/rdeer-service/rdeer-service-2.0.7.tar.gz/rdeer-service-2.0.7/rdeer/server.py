#!/usr/bin/env python3


'''
rdeer-socket is the server part of rdeer-service.
It handle Reindeer running in socket mode.

at start up
- rdeer-server listening for the client
- An instance of Rdeer is created
    - launch a thread scanning the root directory of indexes
    - received clients requests


Starting a Reindeer socket
- When index starting:
    - launch Reindeer query in waiting mode on specified port (default: 12800) using subprocess.Popen()
    - add in a dictionnary dict['nom de l'index'] = {'status': 'loading', 'port': 'n°'}
    - scan each second if port is open
    - when port is open
        - connect as client on the Reindeer index
            - check running index
            - update dictionnary entry dict['index name'] = {'status': 'running', 'port': 'n°'}
            - wait to query from rdeer-client
'''

import os
import sys
import pathlib
import socket
import argparse
import threading
import pickle
import shutil
from packaging import version
import tempfile
import signal
import subprocess
import time
from datetime import datetime
from functools import partial

import common as stream
import info



DEFAULT_PORT       = 12800
REINDEER           = 'reindeer_socket'
INDEX_FILES        = ["reindeer_matrix_eqc_info.txt", "reindeer_matrix_eqc_position", "reindeer_matrix_eqc"]
BASE_TMPFILES      = '/tmp'
WATCHER_SLEEP_TIME = 8
ALLOWED_TYPES      = ['list', 'start', 'stop', 'query', 'check', 'status', 'kill']  # REINDEER_SOCKET COMMANDS
class RDSock_Mesg:                                                                  # MESSAGES RETURNED BY REINDEER
    HELP  = b' * HELP'
    INDEX = b'INDEX'
    QUERY = b'DONE'
    QUIT  = b"I'm leaving, see you next time !"
    STOP  = b'See you soon'

timestamp = lambda: datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


def main():
    args = usage()

    ### Localize full path or index directory (verify if rdeer-socket is a symlink)
    args.index_dir = os.path.join(os.getcwd(), args.index_dir.rstrip('/'))

    ### object rdeer manipulate indexes (list, start stop, query, check)
    rdeer = Rdeer(args)

    ### Stops running indexes on exit (Ctrl C, kill -15)
    exit_graceful = partial(exit_gracefully, rdeer=rdeer)
    signal.signal(signal.SIGINT, exit_graceful)
    signal.signal(signal.SIGTERM, exit_graceful)

    ### server listen for clients
    run_server(args, rdeer)


def exit_gracefully(signal, frame, rdeer):
        for index, values in rdeer.indexes.items():
            if values['status'] == 'running':
                getattr(rdeer, 'stop')({'index':index})
        sys.exit(f"{timestamp()}: Server: {socket.gethostname()!r} interrupted by signal {signal}.")


def run_server(args, rdeer):
    """ Launch rdeer-server in listening mode """
    port = args.port
    ### run server
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.bind(('', port))
    except OSError:
        sys.exit(f"Error: Address already in use (port: {port}).")
    conn.listen(10)
    ### timestamps server startup
    print(f"{timestamp()}: Server: {socket.gethostname()!r} listening on port {port}.", file=sys.stdout)

    while True:
        client, addr = conn.accept()
        ### run client query in a separated thread
        threading.Thread(target=handle_client, args=(client, addr, rdeer)).start()

    client.close()
    conn.close()


def handle_client(client, addr, rdeer):
    try:
        ### receive data stream. It won't accept data packet greater than 1024 bytes
        received = stream.recv_msg(client)
        received = pickle.loads(received)
        ### loggin request
        user = received.get('user') or 'unknown'
        if 'index' in received:
            print(f"{timestamp()} client:{addr[0]} type:{received['type']} user:{user} index:{received['index']}", file=sys.stdout)
        else:
            print(f"{timestamp()} client:{addr[0]} type:{received['type']} user:{user}", file=sys.stdout)
    except pickle.UnpicklingError:
        stream.send_msg(client, b"Error: data sent too big.")
        return
    except EOFError:
        stream.send_msg(client, b"Error: ran out of input")
        return
    except TypeError:
        data = "Error: no data to send to Reindeer (Maybe issue comes from client)."
        response = {'type': received['type'], 'status': 'error', 'data': data,}
        stream.send_msg(client, msg.encode())
        return response

    ### CHECK VERSION
    srv_vers = info.VERSION
    clt_vers = received.get('version') or 'unknown'
    if clt_vers=='unknown' or version.parse(clt_vers).major != version.parse(srv_vers).major:
        data = f"Error: server and client do not have the same major version (client: {clt_vers} - server: {srv_vers})."
        response = {'type': received['type'], 'status': 'error', 'data': data,}
        stream.send_msg(client, pickle.dumps(response))
        return response

    ### CALL RDEER METHOD MATCHING TO THE QUERY TYPE
    if received['type'] not in ALLOWED_TYPES:
        msg = f"Error: request type {received['type']!r} not handled. Please contact maintainer"
        response = {'type': received['type'], 'status': 'error', 'data': msg,}
        print(msg, file=sys.stderr)
        stream.send_msg(client, pickle.dumps(response))
        return response
    response = getattr(rdeer, received['type'])(received, addr)

    ## If Error message
    if response['status'] == 'Error':
        print(f"{response['status']}: {response['msg']}", file=sys.stderr, flush=True)
        stream.send_msg(client, pickle.dumps(response))

    ### Send response to client
    stream.send_msg(client, pickle.dumps(response))


class Rdeer:
    """
    Maintain indexes information in 'indexes' dict
    Store sockets information in 'socket' dict
    Methods:
      - start: launch an index in a free port
      - stop, check, query: prepares the command to reindeer_socket and transmit to _ask_index()
      - list: display list of indexes, with status [available|loading|running|error]
      - _watcher: thread to maintain 'indexes' and 'socket' dicts and connect to loading index
    """

    def __init__(self, args):
        """ Class initialiser """
        self.index_dir = args.index_dir
        self.args = args
        ### controls if Reindeer found
        if not shutil.which(REINDEER):
            sys.exit(f"Error: {REINDEER!r} not found")
        ### watcher : loop to maintain index info, connect to index, check indexes
        self.indexes = {}               # states of all indexes
        self.sockets = {}               # opened sockets
        self.procs = {}                 # reindeer indexes processus

        watcher = threading.Thread(target=self._watcher, name='watcher')
        watcher.daemon = True
        watcher.start()


    def _watcher(self):
        """
        start threading to scan available Reindeer indexes.
        needed :
            - index directory (args)
            - representative index file
        """
        path = self.index_dir
        try:
            os.listdir(path)
        except FileNotFoundError:
            sys.exit(f"Error: directory {path!r} not found.")
        while True:
            ### find available indexes
            found_dirs = []                                     # candidate indexes
            index_list = [index for index in self.indexes]      # list of current indexes
            ### find all available indexes
            for dir in os.listdir(path):
                subpath = os.path.join(path, dir)
                if os.path.isdir(subpath) and all([f in os.listdir(subpath) for f in INDEX_FILES ]):
                    found_dirs.append(dir)
            ### find for new available indexes
            for dir in found_dirs:
                if not dir in self.indexes:
                    self.indexes[dir] = {'status':'available', 'port':None}
                    print(f"Index found: {dir}")
            ### find for removed indexes
            for dir in index_list:
                if not dir in found_dirs:
                    self.indexes.pop(dir)
                    print(f"Removed index: {dir!r}")

            ### check for running or loading indexes
            for index, value in self.indexes.items():
                port = value['port']
                if value['status'] == 'loading': # and self._port_open(port):
                    # ~ print(f"{index} IS MARKED AS 'loading' --> CHECK IF RUNNING")
                    # Connection to index
                    try:
                        self._connect_index(index, port)
                    except Exception:
                        a, b, c = sys.exc_info()
                        print(f"{a.__name__}: {b} (at line {c.tb_lineno})")

                elif value['status'] == 'running':
                    pass
                    # ~ print("TODO: ADD CHECK CONTROL")
                    ### ask to 'INDEX'.
                    ### If return is blank
                        ### Send a message
                        ### if port not running
                            ### Send a message
                            ### try a start

                elif value['status'] == 'error':
                    ### TRY TO KILL THE PROCESS
                    self.procs[index].kill()
                    ### RESTART INDEX
                    received = {'type': 'start', 'index': index, 'port': None,}
                    self.start(received)
                    ### TODO: send email"

            time.sleep(WATCHER_SLEEP_TIME)


    def list(self, received, addr=None):
        response = {'type': received['type'], 'status': 'success', 'data': self.indexes}
        return response


    def status(self, received, addr=None):
        index = received['index']
        if not index in self.indexes:
            print(f"{timestamp()} Error: unable get index {index} from {addr[0]} (not found).", file=sys.stdout)
            return {'type': received['type'], 'status': 'error', 'data': f'Index {index} not found.'}
        status = self.indexes[index]['status']
        response = {'type': received['type'], 'status': 'success', 'data': status}
        return response


    def start(self, received, addr=None):
        '''
        Start a Reindeer Index
        '''
        index = received['index']
        ### Check if index is in list and no still started
        if not index in self.indexes:
            print(f"{timestamp()} Error: unable to start index {index} from {addr[0]} (not found).", file=sys.stdout)
            return {'type':'start', 'status':'error', 'data':f'Index {index} not found.'}
        if self.indexes[index]['status'] in ['running', 'loading']:
            print(f"{timestamp()} Error: unable to start index {index} from {addr[0]} (still running or loading).", file=sys.stdout)
            return {'type':'start', 'status':'error', 'data':f'index {index} still running or loading.'}
        ### PICK FREE PORT NUMBER
        sock = socket.socket()
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        del(sock)
        ### Launch new instance of Reindeer
        cmd = f'{REINDEER} -l {os.path.join(self.args.index_dir, index)} -p {port} &'.split(' ')
        ### EXECUTE REINDEER_SOCKET on the specified index
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            msg = f"Error: index {index} could not be loaded"
            return {'type': received['type'], 'status':'error', 'data': msg}

        ### CHANGE STATUS AND RETURN RESPONSE TO CLIENT
        print(f"{timestamp()} Index:{index} status:loading  port:{port}", file=sys.stdout)

        self.indexes[index]['port'] = port
        self.procs[index] = proc
        self.sockets[index] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.indexes[index]['status'] = 'loading'

        data = self.indexes[index]
        return {'type': received['type'], 'status':'success', 'data': data}


    def stop(self, received, addr=None):
        index = received['index']
        response = self._ask_index(index, b'QUIT', RDSock_Mesg.QUIT)
        response = self._ask_index(index, b'STOP', RDSock_Mesg.STOP)
        if response['status'] == 'success':
            self.sockets[index].shutdown(socket.SHUT_RDWR)
            self.sockets[index].close()
            del(self.sockets[index])
            self.indexes[index]['status'] = 'available'
            self.indexes[index]['port'] = None
            self.procs[index].kill()
            self.procs.pop(index)
            print(f'{timestamp()} Index:{index} status:available', file=sys.stdout)
            return {'type':'stop', 'status':'success','data':f"Index {index!r} sent: {response['data']!r}."}
        else:
            return {'type':'stop', 'status':'error','data':response['data']}


    def query(self, received, addr=None):
        index = received['index']
        ### define/create tmp dir/files
        tmp_dir = tempfile.mkdtemp(prefix="rdeer-", dir=BASE_TMPFILES)
        infile = os.path.join(tmp_dir, 'query.fa')
        outfile = os.path.join(tmp_dir, 'reindeer.out')
        ### create query fasta file
        with open(infile, 'w') as fh:
            fh.write(received['query'])

        ### BUILD QUERY
        threshold = ':THRESHOLD:' + received['threshold'] if received['threshold'] else ''
        mesg = f"FILE:{infile}{threshold}:OUTFILE:{outfile}:FORMAT:{received['format']}".encode()

        ### ASK REINDEER
        response = self._ask_index(index, mesg, RDSock_Mesg.QUERY)

        ### IF REINDEER RETURN ERROR
        if not response['status'] == 'success':
            shutil.rmtree(tmp_dir, ignore_errors=True)  # delete tempory files
            if response['data'] == "Unknow message returned by Reindeer (b'').":
                self.indexes[index]['status'] = 'error'
            return {'type':'query', 'status':'error', 'data':response['data']}

        ### REINDEER OUTFILE TO tsv
        outfile = os.path.join(os.path.dirname(infile), 'reindeer.out')
        try:
            with open(outfile) as fh:
                data = fh.read()
        except FileNotFoundError:
            time.sleep(.5)
            with open(outfile) as fh:
                data = fh.read()
        shutil.rmtree(tmp_dir, ignore_errors=True)  # delete tempory files
        ### RESPONSE TO CLIENT
        return {'type':'query', 'status':response['status'], 'data':data}


    def kill(self, received, addr=None):
        index = received['index']
        if index not in self.indexes:
            return {'type':'kill', 'status':'error','data':f'Index {index!r} not found'}
        elif self.indexes[index]['status'] == 'available':
            return {'type':'kill', 'status':'error','data':f'Index {index!r} not started'}
        if index in self.sockets:
            ### kill the process and updates info
            self.procs[index].kill()
            self.indexes[index] = {'status':'available', 'port':None}
            del self.sockets[index]
            del self.procs[index]
            msg = f"Index {index!r} is now stopped"
            return {'type':'kill', 'status':'success','data':msg}
        else:
            print(f'{timestamp()} Error: type:kill index {index} found in self.indexes'
                  f"with status {self.indexes[index]['status']!r}"
                  "but not in self.sockets", file=sys.stderr)
            return {'type':'kill', 'status':'error','data':f'unexpecting error to kill the {index!r} Index'}
        

    def check(self, received, addr=None):
        index = received['index']
        response = self._ask_index(index, b'INDEX', RDSock_Mesg.INDEX)
        if response['status'] == 'success':
            return {'type':'check', 'status':'success','data': f"{index} responds to queries"}
        else:
            # ~ if response['data'] == "Unknow message returned by Reindeer (b'').":
                # ~ self.indexes[index]['status'] = 'error'
            return {'type':'check', 'status':'error','data':response['data']}


    def _ask_index(self, index, mesg, control):
        """ Function doc """
        # ~ print(f"MESG SEND TO REINDEER: {mesg} (index {index!r}).")
        if index in self.indexes:
            if self.indexes[index]['status'] == 'running':
                try:
                    self.sockets[index].send(mesg)
                    recv = self.sockets[index].recv(1024)
                except:
                    return {'status':'error','data':f'Unable to query the {index!r} index.'}
                if recv.startswith(control):
                    return {'status':'success','data':recv}
                elif self._index_is_crashed(index):
                    msg = f"the index {index!r} crashed during the query"
                    print(f"{timestamp()} Error: {msg}", file=sys.stdout)
                    return {'status':'error', 'data':msg}
                else:
                    return {'status':'error','data':f'Unknow message returned by Reindeer ({recv!r}).'}
            else:
                return {'status':'error','data':f"Index not running (status: {self.indexes[index]['status']!r})"}
        else:
            return {'status':'error','data':f'Index {index!r} not found'}


    def _index_is_crashed(self, index):
        ### check if Reindeer process running, otherwise, probably it is crashed
        port = self.indexes[index]['port']
        cmd = f'{REINDEER} -l {os.path.join(self.args.index_dir, index)} -p *{port}'
        proc = subprocess.run(f"ps -ef | grep '{cmd}'", shell=True, stdout=subprocess.PIPE)
        if proc.returncode:
            self.indexes[index]['status'] = 'error'
            return True
        return False


    def _connect_index(self, index, port):
        """ Function doc """

        if self._index_is_crashed(index):
            print(f'{timestamp()} Error: index {index} crashed during loading', file=sys.stdout)

        ### try to connect
        try:
            ### Try to connect to loading Index (It returns 0 whis success, else an other number )
            self.sockets[index].connect_ex(('', int(port)))
            ### Try to get WELCOME message
            self.sockets[index].settimeout(1)
            welcome = self.sockets[index].recv(1024)
            self.sockets[index].settimeout(None)
            ### Change index statut
            self.indexes[index]['status'] = 'running'
            print(f'{timestamp()} Index:{index} status:running port:{port}', file=sys.stdout)
        except TimeoutError:
            ### While Reindeer Index is not loaded, a TimeoutError appear at s.recv() message
            pass
        ### TODO DELETE ALL COMMENTS
        # ~ except ConnectionRefusedError:
            # ~ ### try to connect during loading time  (with s.connect(('', int(port)))
            # ~ pass
        # ~ except OSError:
            # ~ ### try to connect during loading time  (with s.connect(('', int(port)))
            # ~ pass

def usage():
    """
    Help function with argument parser.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("index_dir",
                        type=_dir_path,
                        help="base directory of Reindeer indexes",
                        metavar=('index_dir'),
                       )
    parser.add_argument("-p", "--port",
                        help=f"port on which the server is listening (default: {DEFAULT_PORT})",
                        metavar="port",
                        default=DEFAULT_PORT,
                        type=int,
                       )
    parser.add_argument('-v', '--version',
                        action='version',
                        version=f"{parser.prog} v{info.VERSION}",
                       )
    parser.add_argument('--help',
                        action='help',
                        default=argparse.SUPPRESS,
                        help=argparse._('show this help message and exit')
                        )
    ### Go to "usage()" without arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    return parser.parse_args()


def _dir_path(string):
    ### for usage(), test if argument is a directory
    if os.path.isdir(string):
        return string
    else:
        sys.exit(f"NotADirectoryError ({string}).")


if __name__ == "__main__":
    main()
