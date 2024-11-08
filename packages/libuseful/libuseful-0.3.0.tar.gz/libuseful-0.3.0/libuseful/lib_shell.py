############################################################################
#   Author : eunseok, Kim
#   E-mail : es.odysseus@gmail.com
###########################################################################

import os
import time
import psutil
import locale
import platform
import subprocess
from typing import List
from . import lib_path as lpath
from .lib_retry import *
from .exception import *
from . import lib_logger as myLogger
from .lib_logger import *

logger = myLogger.get_instance(level_of_file=CmyLogger.DEBUG_LEVEL)

CODEC: str = locale.getpreferredencoding(True)

class TYPE:
    DIR = "dir"
    FILE = "a file"
    ALL_FILES = "all_files"

class TAR_TYPE:
    GZ = "tar.gz"
    TGZ = "tgz"
    
    @staticmethod
    def all():
        return [ TAR_TYPE.GZ, TAR_TYPE.TGZ ]


def local_shell(command: str, timeout_sec: int=5):
    strout = None
    def get_msg( out ) -> str:
        try:
            if out is None:
                return None
            
            msg = out.decode(CODEC).strip()
        except UnicodeDecodeError as e:
            logger.warn(f"try to get error-msg by UTF8-decoder.")
            msg = out.decode('UTF8').strip()
        except BaseException as e:
            logger.error(e)
            raise e
        finally:
            if msg is not None and len(msg) <= 0:
                msg = None
        return msg
    
    try:
        if command is None:
            raise CENullException("command is None.")
        
        # logger.debug(f"command: {command}")
        strout = subprocess.run(command, timeout=timeout_sec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return get_msg(strout.stdout), get_msg(strout.stderr)
    
    except subprocess.TimeoutExpired as e:
        logger.error("stdout={}, stderr={}".format(get_msg(e.stdout), get_msg(e.stderr)) )
        if strout is not None:
            logger.error("stderr={}".format( get_msg(strout.stderr) ))
        raise e
    except BaseException as e:
        logger.error(e)
        if strout is not None:
            logger.error("stderr={}".format( get_msg(strout.stderr) ))
        raise e

def local_check_process(proc_name: str, user: str=None, kill: bool=False):
    try:
        if proc_name is None:
            raise RuntimeError("'proc_name' is None.")
        
        proc: psutil.Process = None
        psutil.process_iter.cache_clear()       # ver >= 6.0.0 available.
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                command = " ".join(proc.cmdline())
            except psutil.ZombieProcess as e:
                # logger.warn(e)
                continue
            
            if proc_name in command:
                if user is not None and proc.username() != user:
                    break
                
                if kill is True:
                    proc.kill()
                    time.sleep(3.0)
                
                return proc.is_running()
            
        return False
    except BaseException as e:
        logger.error(e)
        raise e

def local_execute_backend(command: str, working_dir: str=None):
    try:
        if command is None:
            raise CENullException("command is None.")
        
        logger.debug(f"command: {command}")
        local_check_process(command, kill=True)
        
        # os.spawnl(os.P_DETACH, command)       # No support for windows
        subprocess.Popen(command, shell=True, cwd=working_dir, env=None)
        return local_check_process(command)
    
    except BaseException as e:
        logger.error(e)
        raise e

def local_kill_adbd():
    try:
        os_name = platform.system()
        if os_name == "Linux":
            command = "adb -L tcp:5037 fork-server server --reply-fd 4"
            if local_check_process(command, kill=True) is True:
                err = "Can not kill 'adb server'"
                logger.warn(err)
                return err
            stdout = "Successful: adb kill-server"
        elif os_name == "Windows":
            stdout, stderr = local_shell("adb kill-server")
        else:
            raise RuntimeError("Not supported OS-type. ({})".format(os_name))
        
        return stdout
    except BaseException as e:
        logger.error(e)
        raise e

@retry( (FileNotFoundError, BaseException), tries=3, delay=.3 )
def local_mkdir(dir_path: str):
    try:
        if dir_path is None:
            raise RuntimeError("dir_path is None.")
        
        os_name = platform.system()
        if os_name == "Linux":
            local_shell("mkdir -p \"{}\"".format(dir_path))
            local_shell("sync")
        elif os_name == "Windows":
            local_shell("mkdir \"{}\"".format(dir_path))
        else:
            raise RuntimeError("Not supported OS-type. ({})".format(os_name))
        
        # check 'DIR' whether it exist or not.
        if os.path.isdir(dir_path) is False:
            raise FileNotFoundError(f"Can not find DIR-path. ({dir_path})")
    except (RuntimeError, FileNotFoundError, BaseException) as e:
        logger.error(e)
        raise e
    
def local_date() -> str:
    try:
        os_name = platform.system()
        if os_name == "Linux":
            date, err = local_shell("date +'%F_%T'")
            date = date.strip()
        elif os_name == "Windows":      # 2023/07/25_ 8:01:07.39   ==>  2023-07-25_08:01:07
            date, err = local_shell("echo %date%_%time%")
            date = date.strip()
            date = date[:date.find(".")]
            date = date.replace("/", "-")
            date = date.replace(" ", "0")
        else:
            raise RuntimeError("Not supported OS-type. ({})".format(os_name))
        
        return date
    except BaseException as e:
        logger.error(e)
        raise e
    
def local_ping(ip: str, cnt: int=5) -> str:
    ret = False
    try:
        if ip is None:
            raise RuntimeError("ip is None. It's invalid.")
        if cnt <= 0:
            raise RuntimeError(f"cnt is invalid-value. ({cnt})")

        # make 'command'
        command = None
        os_name = platform.system()
        if os_name == "Linux":
            command = f"ping -c {cnt} {ip}"
        elif os_name == "Windows":
            command = f"ping -n {cnt} {ip}"
            
        if command is None:
            raise RuntimeError("command is None.")
        
        # execute 'command'
        out, err = local_shell(command, timeout_sec=20)
        if out is None or len(out) <= 0:
            print(f"ping-error= {err}")
        else:
            print(f"{out}")
            if out.find(f"{cnt} packets transmitted, {cnt} received") != -1:
                ret = True
            elif out.find(f"패킷: 보냄 = {cnt}, 받음 = {cnt}") != -1:
                ret = True
            elif out.find(f"{cnt} packets transmitted, 0 received, 100% packet loss") != -1:
                raise ConnectionAbortedError(f"Can not find device's IP({ip}) adress.")
            elif out.find(f"패킷: 보냄 = {cnt}, 받음 = 0") != -1:
                raise ConnectionAbortedError(f"Can not find device's IP({ip}) adress.")
        
    except ConnectionAbortedError as e:
        logger.error(e)
        raise e
    except BaseException as e:
        logger.error(e)
    return ret

def local_copy(src: str, src_type: TYPE, dest: str, dest_type: TYPE=TYPE.DIR):
    try:
        if src is None or dest is None:
            raise RuntimeError(f"Source({src}) or Destination({dest}) path is None.")
        
        # make 'command'
        command = None
        src_opt = ""
        dest_opt = ""
        os_name = platform.system()
        
        
        if os_name == "Linux":
            if src_type == TYPE.DIR:
                src_opt = '/*'
            if dest_type == TYPE.DIR:
                dest_opt = '/'
                
            command = f"cp -Rdp \"{src}\"{src_opt} \"{dest}\"{dest_opt}"
        elif os_name == "Windows":
            command = f"xcopy \"{src}\" /E /Y \"{dest}\""
        
        if command is None:
            raise RuntimeError("command is None.")

        # make 'dest' directory.
        if dest_type == TYPE.DIR:
            local_mkdir( dest )
        
        # execute 'command'
        _, err = local_shell(command=command, timeout_sec=30)
        if err is not None and len(err) > 0:
            raise RuntimeError(f"Can not copy from SRC({src}) to DEST.({dest}): {err}")
        
    except BaseException as e:
        logger.error(e)
        raise e
    
def local_remove(src: str, type: TYPE = TYPE.FILE):
    def run_command(cmd: str):
        if cmd is None:
            raise RuntimeError("command is None.")
        
        # execute 'command'
        _, err = local_shell(command=cmd, timeout_sec=30)
        if err is not None and len(err) > 0:
            raise RuntimeError(f"Can not remove SRC({src}) file: {err}")
        
    try:
        if src is None:
            raise RuntimeError(f"Source({src}) path is None.")
        
        # make 'command'
        os_name = platform.system()
        if os_name == "Linux":
            if type == TYPE.ALL_FILES:
                src = f"{src}/*"
            run_command( f"rm -rf \"{src}\"" )
            
        elif os_name == "Windows":
            if type == TYPE.ALL_FILES:
                run_command( f"del /q \"{src}\*\"" )                            # remove all-files in 'src'
                run_command( f"for /d %x in ({src}\*) do @rd /s /q \"%x\"" )    # remove all-folders in 'src'
            elif type == TYPE.FILE:
                run_command( f"del /q \"{src}\"" )      # remove a file as 'src'
            elif type == TYPE.DIR:
                run_command( f"@rd /s /q \"{src}\"" )   # remove a folder as 'src'

    except BaseException as e:
        logger.error(e)
        raise e

@retry( FileNotFoundError, tries=3, delay=1.0 )
def local_tar_compress( src: List[str], out: str, src_dir: str=None, out_type: TAR_TYPE=TAR_TYPE.GZ, timeout_sec: int=5 ):
    '''
        parameter
            src         [str]       Source-Files name or path
            out         str         Destination-File name or path               default="tar_compress_tempname"
            src_dir     str         Root-directory path for Source-Files.       default=None
            out_type    TAR_TYPE    which tar-file type do you want?            default=TAR_TYPE.GZ
        
        return
            Destination-File's full-path.   str
    '''
    try:
        opt = "-cvzf"
        srcs_path = ""
        if src is None or len(src) <= 0:
            raise RuntimeError("'src' is invalid-data. required it.")
        
        if out_type not in TAR_TYPE.all():
            raise RuntimeError(f"'out_type' is invalid-data. ({out_type})")
        
        
        if out is None:
            out = "tar_compress_tempname"
        out += f".{out_type}"
        
        if src_dir is None:
            src_dir = lpath.get_rootpath()

        if out_type == TAR_TYPE.TGZ:
            opt = "-czf"
            
        if lpath.is_abspath(out) is False:
            out = lpath.join_paths( src_dir, out )
        
        for item in src:
            # srcs_path += f" '{item}'"
            srcs_path += f" \"{item}\""
        
        # compress files
        # cmd = f"tar {opt} '{out}' -C '{src_dir}' {srcs_path}"
        cmd = f"tar {opt} \"{out}\" -C \"{src_dir}\" {srcs_path}"
        logger.info(f"> Tar Compress-CMD: {cmd}")
        _, err = local_shell(cmd, timeout_sec=timeout_sec)
        if err is not None:
            raise RuntimeError(f"Error: {err}")
        
        if lpath.check_exist(out, attribute="file") is False:
            raise FileNotFoundError(f"Can not find Output-File. ({out})")
        
        return out
    except FileNotFoundError as e:
        logger.error(e)
        raise e
    except BaseException as e:
        logger.error(e)
        raise e


# def remote_shell_ssh( user: str, host: str, command: str, passwd: str = None):
#     try:
#         client = paramiko.SSHClient()
#         client.load_system_host_keys()
#         client.connect( host, port=22, username=user, password=passwd)

#         (stdin, stdout, stderr) = client.exec_command( command )
#         cmd_output = stdout.read()
#         logger.info( "[Output]: {}".format(cmd_output) )

#     except BaseException as e:
#         logger.error(e)
#     finally:
#         client.close()

# def connect_to_thing( user: str, host: str, passwd: str = None, m_port=22 ) -> paramiko.SSHClient:
#     try:
#         client = paramiko.SSHClient()
#         client.load_system_host_keys()
#         client.connect( host, port=m_port, username=user, password=passwd)
#         return client
#     except BaseException as e:
#         logger.error(e)
#         client.close()

#     return None

