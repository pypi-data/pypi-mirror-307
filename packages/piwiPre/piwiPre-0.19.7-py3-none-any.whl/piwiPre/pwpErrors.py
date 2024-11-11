# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini@gmail.com
# ---------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------
# Management of exceptions for piwiPre
# ---------------------------------------------------------------------------------------------------------------

# raise PwpError(): prints a message and generate an exception


import inspect
import time
import datetime
import sys

import termcolor
import platform
import os


class PwpLog:
    def __init__(self):
        self.cwd = os.getcwd()  # this is read at the init of the module, so BEFORE any chdir
        self.gui = None         # if there is a GUI, we will print there
        self.quiet = True
        self.logfile = None
        self.start_time = datetime.datetime.now()
        self.stop_on_warning = False
        self.print_debug = False
        self.colors = True
        self.data = {           # normal logs are not stored
            'info': [],         # logs that are stored for tests
            'Warning': [],      # a problem that do not require stopping the program
            'ERROR': [],        # under normal circumstances, stops the program. Can be trapped for test
        }
        self.started = False
        self.files_processed = {}
        if platform.system() == "Windows":
            os.system('color')

    def start_logging(self):
        logfile_name = time.strftime("piwiPre_%Y_%m_%d.log")
        try:
            self.logfile = open(logfile_name, "a", encoding="utf-8")
            print(f"Opened log file '{os.path.abspath(logfile_name)}'")
        except OSError:
            print(f"Can not open '{logfile_name}', defaulting to HOME")
            logfile_name = os.path.expanduser("~") + '/' + logfile_name
            try:
                self.logfile = open(logfile_name, "a", encoding="utf-8")
            except OSError:
                self.logfile = None
                print(f"Can not open '{logfile_name}' in HOME !, no log file.")

    def start(self):
        if self.started:
            return
        self.start_logging()
        self.quiet = False
        self.started = True
        self.msg(f"---- piwiPre start {self.start_time}")
        self.msg('')
        self.msg(f"BASE (i.e. cwd)           = '{self.cwd}'")
        self.msg(f"System                    = '{platform.system()}'")
        self.msg(f"HOME                      = '{os.path.expanduser('~')}'")
        if platform.system() == "Windows":
            self.msg(f"Exe Install Directory     = '{os.environ['PROGRAMFILES(X86)']}' /piwiPre /ffmpeg")  # noqa
            self.msg(f"Processor Architecture    = '{os.environ['PROCESSOR_ARCHITECTURE']}'")

        self.msg('')

        self.msg('--------------- Help on logs:')
        self.msg('')

        self.msg('LR[LR]')
        self.msg('     L  : Local file')
        self.msg('     R  : Remote file')
        self.msg('')

        self.msg('A[author]')
        self.msg('')

        self.msg('D[date]')
        self.msg('')

        self.msg('Rot[rf]')
        self.msg('   --  : nothing'),
        self.msg('   |-  : FLIP_LEFT_RIGHT'),  # 2
        self.msg('   ^-  : ROTATE_180'),  # 3
        self.msg('   V-  : FLIP_TOP_BOTTOM'),  # 4
        self.msg('   <|  : ROTATE_270'),  # 5
        self.msg('   <-  : ROTATE_270 + flip'),  # 6
        self.msg('   >|  : ROTATE_90 + flip'),  # 7
        self.msg('   >-  : ROTATE_90')
        self.msg('')

        self.msg('meta[diac]: information changed in the metadata of the file (EXIF or IPTC)')  # noqa
        self.msg('     d  : date')
        self.msg('     i  : instructions')
        self.msg('     a  : author')
        self.msg('     c  : copyright')
        self.msg('')

        self.msg('rep[R]  : Representative picture for video')
        self.msg('')

        self.msg('th[STMCI] : thumbnail')       # noqa
        self.msg('     S  : _sq.jpg')
        self.msg('     T  : _th.jpg')
        self.msg('     M  : _me.jpg')
        self.msg('     C  : _cu_250.jpg')
        self.msg('     I  : _index.jpg')
        self.msg('')

        self.msg('rth[stmci] : Remote thumbnail')       # noqa
        self.msg('     s  : _sq.jpg')
        self.msg('     t  : _th.jpg')
        self.msg('     m  : _me.jpg')
        self.msg('     c  : _cu_250.jpg')
        self.msg('     i  : _index.jpg')
        self.msg('')

        self.msg('db[CSWH5GA]: information changed in the piwigo SQL database')  # noqa
        self.msg('     C  : Created in the db')
        self.msg('     S  : Size')
        self.msg('     W  : Width')
        self.msg('     H  : Height')
        self.msg('     5  : md5')
        self.msg('     G  : GPS info')
        self.msg('     A  : Author')
        self.msg('')

        self.msg('Actions:[album filename] ')
        self.msg('  Keep  : file was already in album, keep that value')
        self.msg('  Renam : Rename to a new filename because of conflict, and copy to album')              # noqa
        self.msg('  Copy  : copy file to album, there was no previous file')
        self.msg('  Updat : update the file in album with new value')                                      # noqa
        self.msg('  Clobb : Clobber previous version in album, rename was not allowed')                    # noqa
        self.msg('  DELET : File was deleted from local album because no corresponding remote file')       # noqa
        self.msg('  ABORT : Processing of file is aborted, because no remote file')
        self.msg('')

        self.msg('Back:[backup filename] ')
        self.msg('', flush=True)
        # self.test_msg("This is a message generated by test harness")
        # self.warning("This is a warning")

    def __del__(self):
        if self.logfile:
            self.logfile.close()
        if self.quiet:
            return
        print('---- piwiPre End ')

    def configure(self, config):
        self.print_debug = config['debug']
        self.stop_on_warning = config['stop-on-warning']
        self.colors = config['enable-colors']

    def reset_data(self):
        self.start_time = datetime.datetime.now()
        self.data = {
            'info': [],
            'Warning': [],
            'ERROR': [],
        }
        old = self.files_processed
        self.files_processed = {}
        return old

    def msg_nb(self, level):
        return len(self.data[level])

    def end(self):
        if self.quiet:
            self.msg('', flush=True)
            return
        end = datetime.datetime.now()
        self.msg(f"--- start         = {self.start_time} ---")
        self.msg(f"--- end           = {end} ---")
        self.msg(f"--- duration      = {end - self.start_time}")
        files = 0
        for k in self.files_processed:
            self.msg(f"--- {k:14} = {self.files_processed[k]} ")
            files += self.files_processed[k]
        if files:
            self.msg(f"--- duration/file = {(end - self.start_time) / files}")
        self.msg("------------------------------------", flush=True)

    def incr_picture(self, category):
        self.files_processed[category] = 1 if category not in self.files_processed \
            else self.files_processed[category] + 1

    def add_gui(self, gui):
        self.gui = gui

    def do_msg(self, msg, context=None, level='msg', flush=False, color=None):
        if context is not None:
            if level not in ['debug', 'info'] or self.print_debug:
                print(f"{level:7} {context}", flush=True)
                if self.logfile:
                    self.logfile.write(f"{level:7} {context}\n")
                if self.gui:
                    self.gui.gui_msg(f"{level:7} {context}",)

        if level not in ['debug', 'info'] or self.print_debug:
            line = f"{level:7} {msg}"
            if color and self.colors:
                print(termcolor.colored(line, color=color, force_color=True))
            else:
                print(line, flush=True)
            if self.gui:
                self.gui.gui_msg(line, color)

            if self.logfile:
                self.logfile.write(line + '\n')
                if flush:
                    self.logfile.flush()
            if flush:
                sys.stdout.flush()

        if level != 'msg' and level != 'debug':
            self.data[level].append(msg)

        if level == 'Warning' and self.stop_on_warning:
            raise PwpError("Stop on warning")

        if level == 'Warning' and self.msg_nb('Warning') > 20:
            raise PwpError("Too much warnings")

        if level == 'ERROR' and self.msg_nb('ERROR') > 20:
            raise PwpFatal("Too much errors, aborting")

    def warning(self, msg, context=None):        # warning is always kept for test, and ALWAYS printed
        self.do_msg(msg, context=context, level='Warning', flush=True, color="red")

    def msg(self, msg, context=None, color=None, flush=False):           # msg is NOT kept for test, and ALWAYS printed
        if not self.quiet:
            self.do_msg(msg, context=context, level='msg', color=color, flush=flush)

    def test_msg(self, msg, context=None):
        self.do_msg("    Test: " + msg, context=context, level='msg', color='blue')

    def info(self, msg, context=None):          # info is always kept for test, and printed only if --debug
        self.do_msg(msg, context=context, level='info', flush=True)

    def debug(self, msg, context=None):         # debug is NOT kept for test, and printed only if --debug
        self.do_msg(msg, context=context, level='debug', flush=True)

    # error must NOT be declared, it is mandatory to go through PwpError
    # def error(self, msg, context=None):
    #     self.do_msg(msg, context=context, level='ERROR', flush=True)


class PwpError(Exception):
    def __init__(self, msg, context=None):
        LOGGER.do_msg(msg, level='ERROR', context=context, flush=True, color="magenta")


class PwpInternalError(PwpError):
    def __init__(self, msg: str):  # pragma: no cover
        previous_frame = inspect.currentframe().f_back
        (filename, line_number, _function_name, _lines, _index) = inspect.getframeinfo(previous_frame)
        context = f"{filename}:{line_number:3}"
        super().__init__("INTERNAL " + msg, context=context)


class PwpConfigError(PwpError):
    def __init__(self, msg, context="Cmd-line/configuration "):
        super().__init__(msg, context=context)


# class PwpExit(PwpError):
#     def __init__(self, msg):
#         super().__init__(msg, context="Exiting from main")


class PwpFatal(Exception):  # pragma: no cover      # should not be trapped
    def __init__(self, msg):
        LOGGER.do_msg(msg, level='FATAL', flush=True)


LOGGER = PwpLog()
