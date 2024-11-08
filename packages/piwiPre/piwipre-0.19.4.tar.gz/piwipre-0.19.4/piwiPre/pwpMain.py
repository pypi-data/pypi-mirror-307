# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------

import sys
import os.path
import re
import pprint
import tempfile
import datetime
import socket
import time

from piwiPre.pwpActor import ACTOR, FileInfo, DirInfo, PwpSummary
from piwiPre.pwpParser import PwpParser
from piwiPre.pwpConfig import PwpConfig
from piwiPre.pwpData import PwpJpg, PwpData, PwpVideo
from piwiPre.pwpDir import PwpDirEntry, PwpFileEntry
from piwiPre.pwpErrors import PwpError, PwpConfigError, PwpInternalError, LOGGER
from piwiPre.pwpConfigurator import PwpConfigurator, ThreadConfigurator


# -----------------------------------------------------------------------------------
# Requirements, General behavior
#
# REQ 0001: piwiPre is configured with HOME/.piwiPre.ini and piwiPre.ini files found in the hierarchy of directories
# REQ 0002: piwiPre is also configured by cmdline arguments
# REQ 0003: piwiPre renames .jpg, .mp4, .txt files found in 'triage' (enable-rename) (program_24)
# REQ 0004: piwiPre inserts metadata in .jpg and .mp4 files (enable-metadata)
# REQ 0005: piwiPre generates piwigo metadata (enable-thumbnails)
# REQ 0006: piwiPre synchronizes piwigo albums that were modified (enable-database)
# REQ 0007: piwiPre runs on windows and Linux development stations
# REQ 0008:  --dump-config folder allows to debug the configuration hierarchy (program_2)

# REQ 0009: piwiPre configures automatically album by ADDING piwiPre.ini files (autoconfiguration) (program_6, 7, 8, 9)
# REQ 0010: hand-writing a piwiPre.ini in albums may prevent any modification of files
# REQ 0011: during renaming, the name of .txt files is not changed. They simply go to the appropriate folder
# REQ 0012: tox is run on gitlab, generates html doc and coverage

# REQ 0020: 'enable-XXX' : false: feature is never active
# REQ 0021: 'enable-XXX' : true: feature is done in TRIAGE, and in ALBUMS if the result is not present


# REQ 0049: requirements are parsed from the source and put automatically in doc

# REQ 0050: temporary files are put in a real temporary dir
# REQ 0051: parser: remove trailing / at end of directories, this is common error

# REQ 0100: Renaming is based on the 'names' configuration template
# REQ 0101: Renaming takes into account the date/time of the picture shooting, found in metadata
# REQ 0102: if renaming a file clobber an existing file, piwiPre increments the last numerical field to avoid conflict
# REQ 0103: Configuration is stored in a hierarchy of .ini files
# REQ 0104: The root is $(HOME)/.piwiPre.ini
# REQ 0105: Others are dir/piwiPre.ini
# REQ 0106: *None* denotes a value which is not set. The previous value in the ini file hierarchy is inherited.

# REQ 0200: piwiPre verifies the albums are aligned with configuration (verify-album)
# REQ 0201: piwiPre realigns pictures rotation
# REQ 0202: piwiPre updates metadata
# REQ 0203: piwiPre generates lacking thumbnails from album
# REQ 0204: album modified pictures are saved in 'BACKUP'
# REQ 0205: piwiPre removes useless thumbnails
# REQ 0206: the album to verify is specified by 'verify-album'
# REQ 0207: insert the 'author' metadata
# REQ 0208: use XMP metadata
# REQ 0209: --verify-album on all subdirectories when --recursive-verify-album is set, which is not the default
# REQ 0210: (BUG) if --enable-metadata false, thumbnails have no metadata, IPTCinfo.save() raises an exception  # noqa
# REQ 0211: (BUG) picture 1994-05-Avril-05-Thorigne-010.jpg, date should be found                               # noqa
#

# REQ 0212 :  enable-date-in-filename true/false
#   DOC:
#       If there is a date in the filename, (according to the 'names' argument), then this date is used for metadata
#       Else, if there is a date in metadata, this one is kept
#       Else, the file creation time is used, and written in metadata
#       So, if a file is checked twice, the 2nd run does not perform any change
#
# REQ 0213: --auto-config sets the directory where piwiPre.ini is read recursively: REJECTED

# REQ 0214: during verify-album, if the picture has been changed since last metadata update,
#    or if metadata in db and file are different, then the information in database is reset,
#    and md5 computed again

# REQ 0215: if --enable-metadata-reset true (default : false), metadata is reset to output of current configuration
#           if false, only empty metadata is filled
# REQ 0216: during verify-album, if a video is not inserted in the database, issue a warning
# REQ 0217: --stop-on-warning
# REQ 0218: --trace-malloc
# REQ 0219: --restart-from-dir

# REQ 0221: manage png and other image formats, convert to jpg if enable-rename true
# REQ 0222: manage avi and other video formats, convert to mp4 if enable-rename true
# REQ 0223: video conversion is done with ffmpeg
# REQ 0224: video tag extraction is done with ffprobe
# REQ 0225: ffmpeg-path
# REQ 0226: --piwigo-first-album
# REQ 0228: report the number of files modified, inserted, deleted in filesystem/database
# REQ 0229: special syntax verify-album "*" verifies all the sub albums of the root
# REQ 0230: --enable-conversion
# TODO REQ 0231: BUG: the Android app Piwigo NG hangs while playing video, while browsers play video OK on linux/windows
# REQ 0232:  --language [en, fr], chosen by default with the locale
# REQ 0233: doc in FRENCH
# REQ 0234: --enable-pwg-representative
# REQ 0235: --enable-colors
# REQ 0236: --reset-ini triage/remote/local/default ==> pwpConfigurator
# REQ 0237: --language sets the default value of names and instructions
# REQ 0238: --auto-install
# REQ 0239: --piwiPre-path dir
# REQ 0240: logfile is written in CWD, but if the directory is not writable, writes in HOME
#           (before management of --home and --base)
#           this resolves a disaster when started from ProgramFiles


# REQ 0250: pwpInstaller installes piwiPre, Installer, Configurator, its environment, ffmpeg/ffprobe and MariaDb-CC
# REQ 0251: pwpInstaller builds the shortcuts for GUIs in user application menu
# REQ 0252: pwpInstaller starts in --base or HOME/Downloads
# REQ 0253: pwpInstaller adds environ['PROGRAMFILES(X86)']/piwiPre to the PATH      # noqa
# REQ 0254: pwpInstaller allows to paste URL of online help

# REQ 0260: pwpConfigurator configures .piwiPre.ini
# REQ 0261: Configurator reads,displays,modifies,reset HOME/.piwiPre.ini

# REQ 0270: piwiPre saves the latest starting dir in HOME/.piwiPre.last.hostname
# REQ 0271: piwiPre GUI is started in --base or HOME/.piwiPre.last or HOME
# REQ 0272: piwiPre reads,displays,modifies,reset piwiPre.ini from --base, or changes dir

# REQ 0300: piwiPre maintains (in album context) the database structure
# REQ 0301: piwiPre creates (in triage context) the database structure
# REQ 0302: piwiPre uses MD5 checksum to compare local and remote files
# REQ 0303: Compute MD5 checksums and add them directly in the database when doing a synchro
# REQ 0304: piwiPre reorders the piwigo directories with the right order !  (future piwiPre version 2.0)

# REQ 0306: generate an error if HOME/.piwiPre.ini is not protected: CANCELLED, because chmod is limited in windows
# REQ 0307: clean useless directories in THUMBNAILS (useless files are removed while doing verify-album)
# REQ 0308: installer that allows to download piwiPre, ffmpeg and mariaDb
# REQ 0309: graphical UI for installer
# TODO REQ 0310: The installer should propose a simplified view depending on use cases

# TODO REQ 0311 : installer: Check if MariaDB is installed before installing it
#    This seems non trivial: piwiPre works, for the python and exe version, without installing mariaDB
#         This has been tested on a PC that has no reasons to have mariaDB CC installed
#         That being said, maybe some program has installed maria DB...
#    The only reference to MariaDB in the registry is
#         HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\MariaDB Corporation\MariaDB Connector C
#    There is no MariaDB directory in "C:\Program Files (x86)" or "C:\Program Files"
#          or "C:\Users\fabien-local\AppData\Local"
#    Hypothesis: MariaDB CC is required on SOME database connections, not all.
#    Conservative solution: installer still allows to install MariaDB CC, just in case
# DONE: test enable-auto-configuration program 36, 37, 38, 436, 437,438
# REQ 0312: REJECTED if HOME or BASE not configured, MUST Configure it before configuring other directory
# REQ 0313: string editor: manage the length of fields
# REQ 0314: default value for BASE is HOME/Pictures/BASE, in the installer
# REQ 0315: It is possible to change HOME through the Configurator UI, even if this is NOT recommended
# TODO REQ 0316: PiwiPre configurator, [Write Config] is disabled unless the config has changed OR .lnk is lacking
# REQ 0317: BUG: executing program_33, the directory BACKUP is not filled with modified pictures
# TODO REQ 0318: build downloads.rst with the versions that are really available on the server
# REQ 0319:  in PwpInstaller, the action buttons are not green until the async actions are done
# TODO REQ 0320: explain how to manage COMODO
# TODO REQ 0321: installer uses also the date to stamp piwiPre.exe in the Programs directory, like pwpInstaller
# REQ 0322: backup-ed files are writen in BACKUP/time-stamp/
# REQ 0323: in TRIAGE stage, ALL files are backup, this allows to empty TRIAGE if needed
# REQ 0324: BUG: The tmp directories created by tests are not removed
# REQ 0325: BUG: When tmp thumbnails directory is removed and then isdir(), errno 13 is raised.
# -----------------------------------------------------------------------------------
# Requirements, Testing

# REQ 3000: autotest available with tox and pytest
# REQ 3001: piwipre> tests\\pwp_test.py -n number # runs the test number n                          # noqa
# REQ 3002: pwp_test -n 0 # runs all the tests
# REQ 3003: pwp_test can run all the autotests
# REQ 3004: PyCharm tests cases are saved in project files
# REQ 3005: all automatic tests run by pwp_test can be run by anyone on any development server
# REQ 3006: pwp_test assumes a valid configuration in HOME/.piwiPre.ini
# REQ 3007: coverage is run automatically by tox
# REQ 3008: coverage > 92 %
# REQ 3009: tests --dryrun, with triage and album
# REQ 3010: test error generation

# REQ 3100: test jpg files in TRIAGE, with/without rotation and metadata
# REQ 3101: test .txt files in TRIAGE
# REQ 3102: test .mp4 files in TRIAGE with metadata
# REQ 3104: tests end-2-end with piwogo sync (program_13)
# REQ 3105: test --version
# REQ 3106: test --base
# REQ 3107: test --licence
# REQ 3108: autotest of PwpPatcher
# REQ 3109: autotest of PwpPatcher should cover 80% of code
# REQ 3110: autotest of PwpMP4
# REQ 3111: There are no explicit remote locations on server, use config instead
# REQ 3112: someone with a valid config would run the same test on a different configuration
# REQ 3113: test --dump-config folder
# REQ 3114: test PwpError generation (program_26)
# REQ 3115: on argument error, raise an exception , not trapped
# REQ 3116: test the insertion of the 'author' metadata
# REQ 3117: Corrected BUG: program_11 generates a bug in the communication with the
#           SQL server, probably due to its own communication with git.
#           How to reproduce: run program_11 then program_400 in pycharm RUN mode.
#           if the same test programs are run in PyCharm DEBUG mode, no problem.
#           Explanation: stdin was closed, just reopen it!

# REQ 3120: test --enable-rename false  (program_27)
# REQ 3122: test dates (all cases) :  program_24
# REQ 3123: test unsupported (for instance .foo) files in TRIAGE
# REQ 3123: test pattern with {count} : program_36
# REQ 3124: test manual piwiPre.ini in album
# REQ 3125: Corrected BUG: 'en' index contains some french statements !
# REQ 3128: Corrected BUG: there is a race condition in program 908. If UI finishes too early, piwiPre stops.

# DONE: a modified copy of a picture (so same metadata!) is renamed thanks to collision avoiding

# DOC: piwigo user and password in HOME .piwiPre.ini
# Doc: HOME/.piwiPre.ini contains only server-side information
# Doc: warning: .ini files should be written in UTF8 encoding !
# Doc: usage: photo is accessible or synchronized, not thumbnails: this is not an issue, piwigo will generate thumbnails

# REQ 4000: manage remote thumbnails, accessible with ssh
# REQ 4001: setup ssh/sftp session
# REQ 4002: We assume that thumbnails are always coming from the corresponding file in ALBUM
# REQ 4003: a thumbnail is created only if the file in ALBUM is new, or the thumbnail was non-existent
# REQ 4004: thumbnails are created in THUMBNAILS, then copied to REMOTE-THUMBNAILS

# REQ 5001: piwiPre runs on a workstation connected to the piwigo server through ssh, without shared directories

# ----------------------------- FUTURE ROADMAP -------------------------------------
# Future V2.0
#
#
# TODO REQ 9000: piwiPre runs on a synology NAS
# TODO REQ 9001: --report-album: checks what should be done, prints only required changes, does nothing
# TODO REQ 9002: fully implement enable-conversion of images by NOT forcing working to be JPG, CAVEAT : testing...

# TODO REQ 9003: Parse requirements: reorder by REQ number, yell if duplicate number.
# TODO REQ 9100: piwiPre generates synology @eaDir thumbnails to speedup processing

# FIXME DOC: .authorized keys (ssh doc) login is the local ones, i.e. on the PC, not the server

class PwpMain:
    allowed_chars = r"a-zA-Z0-9\-_.&@~!,;+°()àâäéèêëïîôöùûüÿçñÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÇÑ "    # noqa

    def __init__(self, arguments=None):
        self.initial_cwd = os.getcwd()
        self.configurator: PwpConfigurator or None = None
        self.thread_configurator: ThreadConfigurator or None = None
        self.parser = PwpParser(arguments=arguments, program="piwiPre", with_config=True, piwi_pre=self)
        self.parser_config = self.parser.config
        self.dumped_config = None      # The config reached by --dump-config, used for test only
        self.dirs_to_synchronize = []
        self.expected_thumbnails = []  # list of expected thumbnails, when processing ALBUM. reset for each dir.
        self.expected_representatives = []  # list of expected representatives, when processing ALBUM, reset @ each dir
        if self.parser_config is not None and self.parser_config["backup-test-stamp"] != "":
            self.start_time = self.parser_config["backup-test-stamp"]
        else:
            self.start_time = time.strftime("%Y-%m-%d-%Hh%Mm%S")

    @staticmethod
    def get_base_from_dir(dir_name, p_config):
        base = re.sub(r".jpg$", "", dir_name)
        base = re.sub(r'[^' + PwpMain.allowed_chars + ']', "_", base, re.IGNORECASE)

        # Maybe we are processing a directory which is already the result of a renaming process
        # so its format should be the same then the directory part of 'names'

        template = os.path.basename(os.path.dirname(p_config['names']))
        res = ACTOR.get_info_from_format(template, dir_name)
        if res and res['base'] is not None and res['base'] != '':
            return res['base']
        return base

    @staticmethod
    def build_path(base, common_path: str, path):
        result = base + '/' + common_path + ('' if common_path == '' else '/') + path
        if result[-1] == '/':
            result = result[:-1]
        return result

    def add_to_expected_thumbnails(self, filename: str, config: PwpConfig):
        # we need to get remote_thumbnails_filename BEFORE lower, because it relies
        # on comparing with directories
        remote_file = PwpJpg.get_remote_thumbnails_filename(config, filename)
        # we need to lower(), because files may have been created with a different case
        filename = filename.lower()
        remote_file = remote_file.lower() if remote_file else None
        if filename in self.expected_thumbnails:
            return

        self.expected_thumbnails.append(filename)
        self.expected_thumbnails.append(remote_file)

    def is_expected_thumbnail(self, filename: str):
        return filename.lower() in self.expected_thumbnails

    @staticmethod
    def clean_thumbnails(source_filename: str, config: PwpConfig, common_path: str):
        if config['enable-thumbnails'] is False:
            return  # pragma: no cover

        f = os.path.basename(source_filename)[:-4]  # skip .jpg

        thumbs_base = config['thumbnails'] + '/' + common_path
        thumbs_dir = PwpDirEntry.open(thumbs_base, config, context='thumbnails')

        thumbs = config['piwigo-thumbnails']

        for name, values in thumbs.items():
            thumb_name = name.format(f=f)
            filename = thumbs_base + '/' + thumb_name
            if filename in thumbs_dir.files:
                thumbs_dir.files[filename].remove(father=thumbs_dir, msg="removing old thumbnail")

    def verify_thumbnails(self, source: PwpJpg, config: PwpConfig, common_path: str, stage: str,
                          force_rebuild: bool,
                          summary: PwpSummary):

        # force_rebuild: if true, must rebuild the thumbnail because file HAS changed

        source_filename = source.filename
        if config['enable-thumbnails'] is False:   # pragma: no cover
            LOGGER.debug(f"{stage} {source_filename} enable-thumbnails is False")
            return

        f = os.path.basename(source_filename)[:-4]  # skip .jpg

        thumbs_base = config['thumbnails'] + '/' + common_path
        thumbs_dir = PwpDirEntry.open(thumbs_base, config, context='thumbnails')
        thumbs_dir.read()

        thumbs = config['piwigo-thumbnails']

        for name, values in thumbs.items():
            width = values['width']
            height = values['height']
            crop = values['crop']
            thumb_name = name.format(f=f)

            local_name = thumbs_base + '/' + thumb_name
            self.add_to_expected_thumbnails(local_name, config)

            if config['dryrun']:
                # CAVEAT: conflict management has NOT occurred, because the files are not created in ALBUM
                #         So we do *not* know the exact thumbnail name
                #         hence the message is not accurate
                LOGGER.info(f"Would create Thumbnail {width}x{height} crop={crop} for {source_filename}")
            else:
                source.thumbnail(local_name, width, height, crop, config, force_rebuild, thumbs_dir, summary)

        index_base = 'index.htm'
        local_name = thumbs_base + '/' + index_base
        pwp_index = PwpFileEntry.lookup(local_name, config=config, context='thumbnails')
        self.add_to_expected_thumbnails(local_name, config)

        if pwp_index.is_local:
            pass  # index is already in local or remote, or we do not need to create
        else:
            if config['dryrun']:
                LOGGER.info(f"would create thumbnail html index '{local_name}'")
            else:
                LOGGER.info(f"Create thumbnail html index '{local_name}'")
                ACTOR.mkdirs(os.path.dirname(local_name))
                with ACTOR.open(local_name, 'w') as f:
                    print("Not allowed!", file=f)
                pwp_index.is_local = True
                summary.thumb_index = True

        if pwp_index.put():
            summary.rem_thumb_index = True

    # ------------------------ management of database

    def check_representative(self, source: PwpData, target, config: PwpConfig, summary: PwpSummary):
        """
        if this is a VIDEO, creates the representative picture
        :param source: db description of the source image
        :param target: the path of the file to be inserted
        :param config: current configuration
        :param summary:
        :return: None
        """
        if source.representative is None:
            return
        if not config["enable-pwg-representative"]:
            return  # pragma: no cover

        # so, we have a video
        self.expected_representatives.append(source.representative)     # it is expected, even if it is already here
        rep_dir = os.path.dirname(source.representative)
        ACTOR.mkdirs(rep_dir)

        if ACTOR.isfile(source.representative):
            rep_date = os.path.getmtime(source.representative)
            file_date = os.path.getmtime(target)
            if rep_date >= file_date:
                LOGGER.info(f"Representative {source.representative} is more recent than {target}")
                return
            ACTOR.delete(source.representative)

        # build the representative
        PwpVideo.build_representative(target, source.representative, config=config,
                                      new_author=source.author,
                                      new_copyright=source.copyright,
                                      new_special=source.special,
                                      new_date=source.creation)
        representative_entry = PwpFileEntry.lookup(source.representative, config=config, context='album')
        summary.representative = True
        representative_entry.put()

        source.incr_logger_count("Video representative")

    def insert_in_database(self, source: PwpData, target, sql_filename, config: PwpConfig, summary: PwpSummary):
        """
        insert sql_filename in the sql database.
        if this is a VIDEO, also creates the representative picture
        :param source: db description of the source image
        :param target: the path of the file to be inserted
        :param sql_filename: the path of the file, relative to album
        :param config: current configuration
        :param summary: logger for actions taken
        :return: sql_get_file_info()
        """

        file_info = ACTOR.sql_insert_file(target, sql_filename)
        self.check_representative(source, target, config, summary)

        return file_info

    def verify_database(self, stage, config, source: PwpData, summary: PwpSummary):
        """
        if necessary, updates the JPG metadata of the file inside the DB
        :param stage: current stage
        :param config: current config
        :param source: db description of the source image
        :param summary: summary of actions done
        :return description of what has been updated, or ' db[] ' if no update
        """
        target = source.filename

        self.check_representative(source, target, config, summary)

        if not config['enable-database']:  # pragma: no cover
            LOGGER.debug(f"{stage} {target} enable-database is False")
            return

        if not source.can_be_inserted_in_db:  # pragma: no cover
            LOGGER.debug(f"{stage} {target} is not supported by piwigo: no insertion in database")
            return

        is_modified = False

        sql_filename = target.replace(config['album'], '')
        # example of sql_filename: '/1988/1988-07-Juillet-21-Mariage/1988-03-Mars-15-Rennes-001.jpg'  # noqa

        src_width = source.width
        src_height = source.height

        src_size = int(source.size / 1024)

        sql_file_info: FileInfo = ACTOR.sql_get_file_info(sql_filename)

        if sql_file_info is None:
            # this file is not in the sql database
            sql_file_info = self.insert_in_database(source, target, sql_filename, config, summary)
            summary.db_created = True
            summary.db_size = True
            summary.db_width = True
            summary.db_height = True
            summary.db_md5 = True
            src_md5 = sql_file_info.md5sum
            is_modified = False
        else:
            if sql_file_info.file_size != src_size:
                summary.db_size = True
                is_modified = True

            if sql_file_info.width != src_width:
                summary.db_width = True
                is_modified = True

            if sql_file_info.height != src_height:
                summary.db_height = True
                is_modified = True

            # CAVEAT: lastmodified is the last modification of the database, not of the file            # noqa
            # So, it is under responsibility of programmer to ensure that the data is kept OK
            # NB: changing the md5 also updates lastmodified.                                           # noqa

            # be paranoid: ALWAYS compute MD5 and check
            src_md5 = ACTOR.compute_md5(target)

            if sql_file_info.md5sum != src_md5:
                summary.db_md5 = True
                is_modified = True

        if ((sql_file_info.latitude != source.latitude and source.latitude) or
                (sql_file_info.longitude != source.longitude) and source.longitude):
            summary.db_gps = True
            is_modified = True

        src_author = source.author if source.author else 'NULL'
        if sql_file_info.author != src_author:
            summary.db_author = True
            is_modified = True

        if not is_modified:
            return

        # the file has been modified, let's recompute them and update all data

        source.incr_logger_count("Database")
        ACTOR.sql_set_data(sql_filename, src_md5, src_size, src_width, src_height,
                           source.latitude, source.longitude, source.author,
                           warn_if_no_change=True)
        return

    @staticmethod
    def same_file(f1: str, f2: PwpFileEntry, config: PwpConfig):
        f1_entry = PwpFileEntry.lookup(f1, "local", config)
        if not f1_entry.md5sum:
            f1_entry.md5sum = ACTOR.compute_md5(f1_entry.local)

        if f2.is_local:
            if not f2.md5sum:
                f2.md5sum = ACTOR.compute_md5(f2.local)
            return f1_entry.md5sum == f2.md5sum

        f2_sum = f2.get_remote_md5()
        return f1_entry.md5sum == f2_sum

    @staticmethod
    def rename_allowed(_stage, config):
        if config['enable-rename'] is False:
            return False
        return True

    @staticmethod
    def build_auto_config(src, dst, base, config: PwpConfig):
        # we want to change the {base} component of names to base
        # because this value cannot be guessed from the directory name in ALBUM
        with ACTOR.open(src, 'r') as s:
            lines = s.readlines()
        ACTOR.mkdirs(os.path.dirname(dst), forced=True)
        with ACTOR.open(dst, 'w') as d:
            d.write(f"# file generated by --enable-auto-configuration on {datetime.datetime.now()}\n")
            for li in lines:
                m = re.match(r"names\s*:(.*)", li)
                if m:
                    li = li.replace('{base}', base)
                d.write(li)
        auto_entry = PwpFileEntry.lookup(dst, config=config, context='thumbnails')
        auto_entry.put()

    #     when enable-remote-album is True and remote-album set (and ssh information valid)
    #     album is used as a cache to remote-album
    #     its value SHOULD be set a *local* directory, typically this is 'ALBUM'
    #     after processing triage or album, album and remote-album are coherent (for the processed directories)
    #     so that the user can look inside album to see the state of remote-album
    #     if a file is in album but not in remote-album,
    #     it is considered as abnormal and removed

    def manage_conflict(self, common_path: str, old_file_path: str, new_date: str, new_author: str, base: str,
                        current_file: PwpData, config, stage, summary: PwpSummary):
        """

        :param common_path:
        :param old_file_path:  old_file.local
        :param new_date:
        :param new_author:
        :param base:
        :param current_file: old_file or a copy with metadata and rotation
        :param config:
        :param stage:
        :param summary:
        :return: target, move_to_album, new_filepath
        """
        move_to_album = (stage == 'triage')
        # if True, we need to move the file to album
        # in album stage, we move again to album only if the file has been modified

        if current_file.is_modified:
            move_to_album = True
            if not config['dryrun']:
                # this may happen if the picture was rotated but no modification of metadata
                current_file.save_with_info(config)

        current_file.close()

        file_format = config.format('names')
        file_dico = config.format_dict(new_date, new_author, base=base, suffix=current_file.suffix)

        if self.rename_allowed(stage, config):
            new_filepath = file_format.format(**file_dico)
        else:
            # we do not change the name
            new_filepath = common_path + '/' + os.path.basename(old_file_path)

        if config['enable-conversion']:
            new_filepath = current_file.patch_after_rename(new_filepath)

        # CAVEAT: in ALBUM, the path between ALBUM and the picture is reset by file_format !!!
        # so, common_path is NOT part of new_filepath !

        target = PwpFileEntry.lookup(config['album'] + '/' + new_filepath, context="album", config=config)
        # lookup creates father, the enclosing directory

        to_increment = ACTOR.get_last_numerical_field(config['names'])

        if not target.is_local:
            move_to_album = True  # it is not here, we need to put it

        # if os.path.abspath(target.local) != os.path.abspath(current_file.filename):
        if target.local != current_file.filename:
            move_to_album = True

        summary.action = " Copy"
        while target.exists():  # one file is present in the target directory, with the same name. remote or local

            # first, we clean the relationship between remote and local
            if target.is_local:
                target.local_coherent_with_remote()

            if self.same_file(current_file.filename, target, config):                        # case 1) of conflicts.rst
                if target.local == old_file_path:
                    LOGGER.info(f"File '{old_file_path}' has not changed")
                else:
                    LOGGER.info(f"New file '{old_file_path}' is already in album as '{target.local}'")
                summary.action = " Keep"
                move_to_album = False
                break

            elif target.local == old_file_path:                                              # case 2) of conflicts.rst
                # current_file is a modification of old_file_path with metadata etc. So we need to update old_file_path
                LOGGER.debug(f"Update '{old_file_path}' due to modifications")
                summary.action = "Updat"    # noqa
                move_to_album = True
                break
            elif self.rename_allowed(stage, config):                                         # case 3) of conflicts.rst
                file_dico[to_increment] += 1
                new_filepath = file_format.format(**file_dico)
                if config['enable-conversion']:
                    new_filepath = current_file.patch_after_rename(new_filepath)
                target = PwpFileEntry.lookup(config['album'] + '/' + new_filepath, context="album", config=config)
                move_to_album = True
                summary.action = "Renam"    # noqa
            else:                                                                            # case 4) of conflicts.rst
                LOGGER.debug(f"Clobber '{old_file_path}' because rename not allowed")
                move_to_album = True
                summary.action = "Clobb"    # noqa
                break

        summary.destination = target
        return target, move_to_album, new_filepath

    def run_stage_file(self, stage: str, config: PwpConfig, common_path: str,
                       old_file: PwpFileEntry, base: str):

        LOGGER.debug('')

        summary = PwpSummary(stage, old_file)  # will hold a 1 line summary of actions taken

        LOGGER.debug(f"{stage} file path='{common_path}' filename='{old_file.basename}' base='{base}'")

        backup = self.build_path(config['backup'] + '/' + self.start_time +
                                 '/' + ("TRIAGE" if stage == "triage" else "ALBUM"),
                                 common_path, old_file.basename)
        copy_file_path = self.build_path(config['tmp_dir'], common_path, old_file.basename)

        if not old_file.local_coherent_with_remote():
            backup2 = self.build_path(config['backup'] + '/' + self.start_time + '/ALBUM',
                                      common_path, old_file.basename)
            LOGGER.info(f"backup {old_file.basename} to {backup2}")
            ACTOR.copy(old_file.local, backup2)
            ACTOR.delete(old_file.local)
            # we delete the local version, but will process the remote one
            if not old_file.is_remote:
                # no local and no remote...
                summary.action = "DELET"        # noqa
                summary.backup = backup2
                LOGGER.msg(summary)
                return

        if not old_file.get():
            # LOGGER.msg("Unable to get file from remote location, abort")
            # be silent, get has already generated a warning
            summary.action = "ABORT"
            LOGGER.msg(summary)
            return

        current_file = PwpData.create(old_file.local, config=config, stage=stage,
                                      tmp=copy_file_path, backup=backup)

        if stage == "triage":
            # see 0323: in TRIAGE stage, ALL files are backup-ed, this allows to empty TRIAGE if needed
            current_file.do_backup()
            # LOGGER.info(f"backup {old_file.basename} to {backup}")
            # ACTOR.copy(old_file.local, backup)
            # current_file.backup = None  # so that it is not backup-ed once more
            summary.backup = backup

        current_file.incr_logger_count()
        if current_file.to_abort:  # i.e. PwpAvoided
            # be silent on this type of file
            return

        new_date, new_author = current_file.compute_new_date_author(config)

        summary.author = new_author
        summary.date = PwpData.date_to_str(new_date)

        current_file, _mod = current_file.verify_orientation(stage, config, summary)

        allow_reset = config['enable-metadata-reset']

        # -----------------------------------------------------------------------------------------
        current_file, _mod = current_file.verify_metadata(stage, config, summary,
                                                          new_date=new_date, new_author=new_author,
                                                          enable_reset=allow_reset)
        # -----------------------------------------------------------------------------------------

        # CAVEAT: verify_orientation and verify_metadata MAY change current_file
        #         it MAY be a modified copy in tmp_dir, with new metadata and new rotation
        #

        # -------------------------------------------------------------------------------------------------
        target, move_to_album, new_filepath = self.manage_conflict(common_path, old_file.local,
                                                                   new_date, new_author, base, current_file,
                                                                   config, stage, summary)
        # --------------------------------------------------------------------------------------------------

        target_rel_path = os.path.dirname(new_filepath)

        if move_to_album:

            if stage == 'album':
                current_file.do_backup()

                if current_file.filename != old_file.local:
                    # the original file has been first copied to working,
                    # and then we will copy from working to target
                    # so, we can remove file_path.
                    # if enable-rename is false, target will be the same file thant file_path, so removing is OK
                    # is enable-rename is true, then maybe target is a different file, and we should remove file_path
                    # see program_41 and sample-mov.MOV, which SHOULD be removed.
                    ACTOR.delete(old_file.local)  # if dryrun, does nothing :-)

            if config['dryrun']:
                if old_file.local == target.local:
                    LOGGER.info(f"Would update '{old_file.local}'")
                else:
                    LOGGER.info(f"Would rename '{old_file.local}' : '{target.local}'")
                    # otherwise message is misleading: in reality, we do not rename to itself,
                    # we rename the copy that has been changed
            else:
                if current_file.filename == target.local:
                    raise PwpInternalError(f" '{current_file}' == '{target.local}'")

                self.clean_thumbnails(source_filename=target.local, config=config, common_path=common_path)
                ACTOR.move(current_file.filename, target.local)
                target.is_local = True
                if target.put():
                    summary.remote = True

                current_file.incr_logger_count("Renamed")
                if old_file.local == target.local:
                    LOGGER.info(f"Update '{old_file.local}'")
                else:
                    LOGGER.info(f"RENAME: '{old_file.local}' : '{target.local}'")
        else:
            # i.e. move_to_album False : target is the same file as local or remote,
            # if remote and local exist simultaneously, they have the same md5 (because local_coherent_with_remote)
            # but the file may be absent from local or from remote
            target.synchronize()

        # here, target is always in ALBUM

        # even if the picture is unchanged, maybe the thumbs are not done

        if config['dryrun']:
            target_object = PwpData.create(old_file.local, config=config, stage=stage)
            # We have to cheat, because target is NOT build, so we use file_path !
        else:
            target_object = PwpData.create(target.local, config=config, stage=stage)

        # --------------------------------------------------------------------------------------------
        self.verify_database(stage, config, target_object, summary)
        # --------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------
        self.verify_thumbnails(target_object, config, target_rel_path, stage, move_to_album, summary)
        # --------------------------------------------------------------------------------------------

        if target_object.representative:
            rep_file = PwpData.create(target_object.representative, config=config, stage=stage)
            self.verify_thumbnails(rep_file, config,
                                   target_rel_path + '/pwg_representative',
                                   stage, move_to_album, summary)

        target_object.close()

        if not move_to_album and current_file.filename != old_file.local:
            ACTOR.delete(current_file.filename, forced=True)

        if stage != 'triage':
            LOGGER.msg(summary)
            return

        if not config['enable-auto-configuration']:  # pragma: no cover
            LOGGER.msg(summary)
            return

        this_ini = self.build_path(config[stage], common_path,  'piwiPre.ini')
        config_path = os.path.dirname(new_filepath)
        auto_config_ini = self.build_path(config['thumbnails'], config_path, 'piwiPre.ini')

        if ACTOR.isfile(this_ini) and not ACTOR.isfile(auto_config_ini):
            if config['dryrun']:
                LOGGER.info(f"Would Auto-configure '{this_ini}' to '{auto_config_ini}'")
            else:
                LOGGER.info(f"Auto-configure '{this_ini}' to '{auto_config_ini}'")
                self.build_auto_config(this_ini, auto_config_ini, base, config)
                summary.auto_conf = True
                # if config['enable-remote-thumbnails'] and config['remote-thumbnails']:
                #     remote_ini = auto_config_ini.replace(config['thumbnails'], config['remote-thumbnails'])
                #     ACTOR.remote_put(this_ini, os.path.dirname(remote_ini))   # noqa
                #     summary.rem_auto_conf = True

        LOGGER.msg(summary)

    def remove_useless_thumbnails(self, path, config):
        # test me using program_402
        # if config['dryrun']:
        #     LOGGER.debug("dryrun is True, abort remove_useless_thumbnails")
        #     return
        # if we abort here, many tests will fail
        if not config['enable-thumbnails']:  # pragma: no cover
            LOGGER.debug(f"{path} enable-thumbnails is False, abort remove_useless_thumbnails")
            return
        if not config['enable-thumbnails-delete']:
            LOGGER.debug(f"{path} enable-thumbnails-delete is False, abort remove_useless_thumbnails")
            return

        # We can always erase both local and remote files,
        # because config[thumbnails] CANNOT be the mount point to remote,
        # it must be a temporary folder, e.g. thumbnails.

        # CAVEAT: remove_useless_thumbnails must NOT be recursive with subdirectories,
        # because this is already taken account by run_stage_dir

        thumbs_base = config['thumbnails'] + '/' + path
        father = PwpDirEntry.open(thumbs_base, config, 'thumbnails')

        for file in father.all_entries():
            if self.is_expected_thumbnail(file.local or file.remote):
                pass  # this is normal
            elif file.basename[-4:] == '.ini':
                pass
            else:
                file.remove(father, "when removing extra thumbnail")

        if father.is_empty():
            father.remove(None, "when removing empty thumbnail directory")

        self.expected_thumbnails = []
        return  # because the debugger sometimes has issues with tail return

    # -----------------------------------------------------------------------------------------
    # SQL Database management

    @staticmethod
    def verify_sql_dir(p_config: PwpConfig, path: str):
        if not p_config["enable-database"]:
            return True

        real_path = p_config["album"] + '/' + path

        all_entries = os.listdir(real_path) if os.path.isdir(real_path) else []
        files_list = []
        dirs_list = []
        for item in all_entries:
            if ACTOR.isfile(real_path + '/' + item):
                files_list.append(item)
            else:
                dirs_list.append(item)
        files_list.sort()
        dirs_list.sort()

        dir_info: DirInfo = ACTOR.sql_get_dir_info(path)
        sql_file_descr: dict[FileInfo] = ACTOR.sql_get_dir_file_list(dir_info)

        for file in files_list:
            if file not in sql_file_descr:
                if PwpData.get_type(file) in (PwpData.JPG, PwpData.MP4, PwpData.IMAGE, PwpData.VIDEO):
                    # NB: In ALBUM case, the insertion of lacking files is done BEFORE,
                    # so we should never end up here
                    raise PwpError(f"SQL ERROR: database descriptor for file '{file}' " +
                                   f"should have been inserted in '{path}'")
                else:
                    pass
                    # txt etc files are not managed

        for file in sql_file_descr.keys():
            if file not in files_list:
                # LOGGER.warning(f"database descriptor for file {file} should be deleted from {path}")
                ACTOR.sql_remove_file_from_db(p_config, sql_file_descr[file])

        sql_sons_descr = ACTOR.sql_get_dir_sub_dirs(dir_info)

        rank = 1
        for subdir in dirs_list:

            if subdir not in sql_sons_descr.keys():
                # LOGGER.warning(f"db for dir '{subdir}' should be inserted in '{path}' @ {index}")
                ACTOR.sql_insert_dir_at_rank(subdir, dir_info, rank)
            elif rank != sql_sons_descr[subdir].rank:
                # LOGGER.warning(f"rank of dir '{subdir}' in '{path}' {sql_sons_descr[subdir].rank} -> {index}")
                ACTOR.sql_change_dir_rank(dir_info, sql_sons_descr[subdir], rank)
            rank += 1

        for subdir in sql_sons_descr:

            if subdir not in dirs_list:
                # LOGGER.warning(f"database descriptor for dir {subdir} should be deleted from {path}")
                ACTOR.sql_remove_dir_from_database_recursive(p_config, sql_sons_descr[subdir])

    @staticmethod
    def build_representative_config(config: PwpConfig):
        """
        Creates a new configuration based on the current one, dedicated to processing the representative files
        :param config: current config, MAYBE in triage mode
        :return: new config, in album mode
        """
        new = PwpConfig(filename="Fake for representative",
                        dico={'enable-rename': 'false',
                              'enable-metadata': 'true',
                              'enable-thumbnails': 'true',
                              'triage': None,
                              # verify-album is useless
                              # enable-metadata: keep the current value
                              # enable-rotation: useless, we have never a rotation
                              # enable-database: keep the current value
                              # enable-remote-thumbnails: keep the current value
                              # recursive-verify-album: useless
                              # verify-album: useless
                              # enable-thumbnails-delete: keep the current value
                              }, previous=config)
        new.merge_ini(config)
        return new

    def clean_representatives(self, path):
        if not os.path.isdir(path):
            return
        rep_files = os.listdir(path)
        for file in rep_files:
            file_path = f"{path}/{file}"
            if file_path not in self.expected_representatives:
                LOGGER.msg(f"representative {file_path} is useless: deleted")
                ACTOR.delete(file_path)

    def verify_representatives(self, path, config: PwpConfig):
        if not os.path.isdir(path):
            return
        # If there are some pictures that require a representative, then the directory IS created

        if not path.startswith(config['album']):
            raise PwpInternalError(f"illegal path {path}")

        # le = len(config['album']) + 1  # + 1 to remove /
        # common_path = path[le:]
        self.run_stage_dir("album", config,
                           current_dir=PwpDirEntry.open(path, config=config, context="album"),
                           base="")
        # base can be "", because we use it only for rename

        # TODO: remove rep_dir if empty

    @staticmethod
    def get_common_path(path, stage, config: PwpConfig):
        # common path is the part of path starting just after TRIAGE or ALBUM, without leading /
        root = config[stage]
        if path == root:
            return ''
        if path.startswith(root):
            return path[len(root) + 1:]
        else:
            raise PwpInternalError(f"Illegal path {path} should start with {root}")

    # -----------------------------------------------------------------------------------------
    # run_stage_sir

    def run_stage_dir(self, stage: str, p_config: PwpConfig, current_dir: PwpDirEntry, base: str, recursive=True):
        """
        :param stage: triage,  album
        :param p_config: the configuration **when we entered the directory, before reading the local piwiPre.ini **
        :param current_dir: dir under processing
        :param base: the part of renamed files inherited from common_path
        :param recursive: recursively enter subdirectories
        """

        if re.match(r'(.picasaoriginals.*|.idea.*|@eaDir|.comments)', current_dir.basename):
            # nothing to do here, this directory should not be managed
            return   # pragma: no cover

        if stage == 'triage' and not p_config['triage']:
            raise PwpConfigError("No TRIAGE directory")

        if stage == 'album' and not p_config['album']:
            raise PwpConfigError("No ALBUM directory")

        # common path is the part of path starting just after TRIAGE or ALBUM
        common_path = self.get_common_path(current_dir.local, stage, p_config)

        cur_basename = current_dir.basename

        if stage == "triage":
            config_path = p_config["triage"] + ('' if common_path == '' else '/' + common_path)
        else:
            config_path = p_config['thumbnails'] + ('' if common_path == '' else '/' + common_path)

        new_conf_file = config_path + '/piwiPre.ini'
        new_conf = p_config.push_local_ini(new_conf_file)

        LOGGER.msg('')
        LOGGER.msg(f"------ {stage} dir: common_path='{common_path}' base='{base}'")

        self.expected_thumbnails = []

        new_base = self.get_base_from_dir(cur_basename, new_conf)

        if new_base:
            base = new_base

        all_files, all_dirs = current_dir.read()

        if recursive:
            restart = new_conf['restart-from-dir']
            restart_dir = os.path.basename(restart) if restart and os.path.dirname(restart) == common_path else None

            for item in all_dirs:
                if item.basename == restart_dir:
                    restart_dir = None
                if restart_dir:
                    # we do not manage subdirectories until restart_dir has been seen
                    LOGGER.msg(f"--restart-from-dir '{restart}' excluded '{item}'")
                    continue
                if item.basename == "pwg_representative":
                    continue  # because this directory is special and managed elsewhere
                self.run_stage_dir(stage, new_conf, item, base)

            if restart_dir:
                raise PwpError(f"--restart-from-dir '{restart}' unseen directory: abort")

        self.expected_thumbnails = []
        self.expected_representatives = []
        # if recursive, run_stage_dir has already managed its own remove_useless_thumbnails

        # snapshot1 = ACTOR.trace_malloc_snapshot("start run_stage_file")

        for item in all_files:
            self.run_stage_file(stage, new_conf, common_path, item, base)
            # this should populate expected_thumbnails, even if building it is not necessary

        for item in all_dirs:
            thumbnails_path = new_conf['thumbnails'] + ('' if common_path == '' else '/' + common_path)
            self.add_to_expected_thumbnails(thumbnails_path + '/' + item.basename, p_config)
            # prev line is a hack to ensure simply that subdirectories are kept

        if stage == 'album':
            self.remove_useless_thumbnails(common_path, new_conf)
            # must be done BEFORE representative management,
            # because  remove_useless_thumbnails uses self.expected_representatives
            # which is reset by verify_representatives

        if new_conf['enable-database']:
            rep_dir_set = set([os.path.dirname(f) for f in self.expected_representatives])
            rep_config = self.build_representative_config(new_conf)
            for rep_dir in rep_dir_set:
                self.clean_representatives(rep_dir)  # do cleaning first, because verify will delete expected_rep
            for rep_dir in rep_dir_set:
                self.verify_representatives(rep_dir, rep_config)

        if stage == 'album':
            self.verify_sql_dir(new_conf, common_path)
            # self.remove_useless_thumbnails(common_path, new_conf)

        PwpDirEntry.clean_cache()

        # ACTOR.trace_malloc_snapshot("end run_stage_file", snapshot1, garbage=True)

        # PwpObject.check_leaks()

    # run_stage_sir
    # -----------------------------------------------------------------------------------------

    def combined_config(self, path: str, p_config, caller="dump_config"):
        """
        Goes through the hierarchy of ALBUM, up to path included,
        and merges with the corresponding configuration in THUMBNAILS

        :param path: MUST be a relative path, the code here does NOT manage absolute paths
        :param p_config: current config
        :param caller: string for debug
        :return: the merged configuration
        """

        if p_config["triage"] and path.startswith(p_config["triage"]):
            cur_path = p_config["triage"]
            new_conf = p_config
            new_conf_file = cur_path + '/piwiPre.ini'
            new_conf = new_conf.push_local_ini(new_conf_file)

            length = len(p_config["triage"]) + 1  # +1 to get the following /
            rel_path = path[length:]
            if rel_path:
                dirs = rel_path.split('/')
                for cur_dir in dirs:
                    cur_path += '/' + cur_dir
                    if not os.path.isdir(cur_path):
                        raise PwpConfigError(
                            f"argument of {caller} must exist, and must be a subdir of triage", path)
                    new_conf_file = cur_path + '/piwiPre.ini'
                    new_conf = new_conf.push_local_ini(new_conf_file)
            self.dumped_config = new_conf  # just for test
            return new_conf

        if p_config["album"] and p_config['thumbnails'] and path.startswith(p_config["album"]):
            cur_path_config = p_config['thumbnails']
            cur_album_path = p_config["album"]
            new_conf = p_config
            new_conf_file = cur_path_config + '/piwiPre.ini'
            new_conf = new_conf.push_local_ini(new_conf_file)

            length = len(p_config["album"]) + 1  # +1 to get the following /
            rel_path = path[length:]
            if rel_path:
                dirs = rel_path.split('/')
                for cur_dir in dirs:
                    cur_path_config += '/' + cur_dir
                    cur_album_path += '/' + cur_dir
                    if not os.path.isdir(cur_album_path):
                        raise PwpConfigError(
                            f"argument of {caller} must exist, and must be a subdir of album", path)
                    new_conf_file = cur_path_config + '/piwiPre.ini'
                    new_conf = new_conf.push_local_ini(new_conf_file)
            self.dumped_config = new_conf  # just for test
            return new_conf

        raise PwpConfigError(f"--{caller} : dir not existing in triage or album", path)

    def dump_config(self, path, p_config):
        conf = self.combined_config(path, p_config, caller="dump_config")
        LOGGER.info(f"dump_config({path}): {conf['ini-filename-parsed']}")
        pprint.pprint(conf)

    def run(self, test_scenario=None):
        # --quiet --language --base --home --help --full-help --gui --version --license
        # ... are managed in parse_args_and_ini()
        do_exit = False  # exit is delayed until we have managed all --flag that generate exit

        # We do it HERE because we want to have read the 1st .ini in cwd

        if self.parser_config['dump-config']:
            self.dump_config(self.parser_config['dump-config'], self.parser_config)
            do_exit = True

        if self.parser_config['gui'] and not do_exit:
            # CAVEAT: UGLY Hack.
            # we want to test the Configurator features without the UI.
            # in the test harness, we set --gui true to ensure that the Configurator is called
            # BUT we will not display the UI with the configurator
            self.thread_configurator = ThreadConfigurator(config=self.parser_config, pwp_main=self, logger=LOGGER,
                                                          worker=self.worker, test_scenario=test_scenario)
            # ThreadConfigurator calls worker() in a separate Thread
            # then ThreadConfigurator starts run_or_display(), so returns ony when the UI is closed
            pass
            print("ThreadConfigurator is terminated")
        else:
            self.worker(do_exit)

    def worker(self, do_exit=False):
        # -------------------------------------------------------------
        # SQL CONNECT !
        #
        # has already been done in ACTOR.configure
        ACTOR.configure(self.parser_config)
        LOGGER.configure(self.parser_config)

        _conn, first_album, cause = ACTOR.connect_sql(self.parser_config)
        if self.parser_config['test-sql']:
            LOGGER.msg("Testing SQL ")
            LOGGER.msg(f"sql host  : '{ACTOR.sql_host}'")
            LOGGER.msg(f"sql port  : '{ACTOR.sql_port}'")
            LOGGER.msg(f"sql user  : '{ACTOR.sql_user}'")
            LOGGER.msg(f"1st album : '{first_album}'")
            if first_album:
                LOGGER.info(f"test-sql OK: 1st album = '{first_album}'")
            else:
                LOGGER.info(f"SQL ERROR: {cause}")  # pragma: no cover
            do_exit = True

        # -------------------------------------------------------------e
        # SSH CONNECT !
        #
        # has already been done in ACTOR.configure

        remote, uname, cause, is_error = ACTOR.connect_ssh(self.parser_config)

        if self.parser_config['test-ssh']:
            LOGGER.msg("Testing ssh ")
            LOGGER.msg(f"remote host : '{ACTOR.remote_host}'")
            LOGGER.msg(f"remote port : '{ACTOR.remote_port}'")
            LOGGER.msg(f"remote user : '{ACTOR.remote_user}'")
            LOGGER.msg(f"uname       : '{uname}'")
            if remote:
                result = ACTOR.remote_ls(".")
                LOGGER.info(f"test-ssh OK: ls -l       : '{result}'")
            else:
                LOGGER.info(f"Cannot ssh : {cause}")  # pragma: no cover
            do_exit = True

        if self.parser_config['test-sftp']:
            if not remote:  # pragma: no cover
                LOGGER.msg("sftp test OK : skipped because no remote configuration")
                LOGGER.info("sftp test OK : skipped because no remote configuration")
            else:
                dummy = "dummy.txt"
                dummy_timestamp = ACTOR.build_timestamp(dummy)
                base = os.path.basename(dummy)
                LOGGER.debug("Testing sftp")

                dst = self.parser_config['remote-thumbnails']
                ACTOR.remote_put(dummy, dst)
                result = ACTOR.remote_ls(dst)
                if base not in result:  # pragma: no cover
                    LOGGER.info(f"sftp failed      : '{result}'")
                    LOGGER.msg("sftp test failed")
                else:
                    remote_stamp = ACTOR.timestamp_from_ls(result[base])
                    if remote_stamp == dummy_timestamp:
                        LOGGER.info(f"sftp test OK          : '{result[base]}'")
                        LOGGER.msg("sftp test OK")
                    else:
                        LOGGER.info(f"sftp set time failed      : '{dummy_timestamp}'  '{remote_stamp}")
                        LOGGER.msg("sftp test failed")

                ACTOR.remote_delete(dst + '/' + dummy)
            do_exit = True

        if do_exit:
            LOGGER.msg("Exiting due to cmdline options")
        else:
            self.save_latest_cwd()
            with tempfile.TemporaryDirectory() as tmp_dir:
                self.parser_config['tmp_dir'] = tmp_dir

                if self.parser_config['verify-album']:
                    if self.parser_config['triage']:  # pragma: no cover
                        LOGGER.warning(f"removing target --triage {self.parser_config['triage']} " +
                                       "because --verify-album not empty")
                        self.parser_config['triage'] = None

                    to_verify = self.parser_config['verify-album']
                    if '*' in to_verify:
                        to_verify = [f for f in os.listdir(self.parser_config['album']) if os.path.isdir(f)]

                    item_father = os.path.dirname(to_verify)
                    if item_father == "":
                        father_path = self.parser_config['album']
                    else:
                        father_path = self.parser_config['album'] + '/' + item_father
                    cur_dir = os.path.basename(to_verify)
                    p_config = self.combined_config(father_path, self.parser_config, caller="verify-album")
                    new_base = self.get_base_from_dir(cur_dir, p_config)
                    recursive = self.parser_config['recursive-verify-album'] is True
                    dir_to_verify = PwpDirEntry.open(self.parser_config['album'] + '/' + to_verify,
                                                     config=p_config,
                                                     context='album')
                    self.run_stage_dir('album', p_config, dir_to_verify, new_base, recursive=recursive)

                else:
                    target_dir = PwpDirEntry.open(self.parser_config['triage'],
                                                  config=self.parser_config,
                                                  context='local')
                    self.run_stage_dir('triage', self.parser_config, target_dir, '', recursive=True)

            LOGGER.msg("End of processing")

        LOGGER.end()

        if self.configurator is not None and self.configurator.ui is not None and self.parser_config["test-gui"]:
            self.configurator.ui.suicide = True

        # print_open_file_descriptors()
        os.chdir(self.initial_cwd)

    @staticmethod
    def save_latest_cwd():
        current_host = socket.gethostname()
        current_host = re.sub(r'\W+', "-", current_host)
        filename = f"{os.getcwd()}/.piwiPre.last.{current_host}"
        with ACTOR.open(filename, 'w') as f:
            print(f"{os.getcwd()}\n", file=f)
        LOGGER.msg(f"Saved last run location in {filename}")


def pwp_init(arguments=None):
    """used for tests, when the test harness in test_pwp needs to use the ssh connection
    initializes PwpMain"""

    main = PwpMain(arguments)
    return main


def pwp_run(main: PwpMain, test_scenario=None):
    """
    run main with test scenario
    parameters of main have been passed previously
    for tests, when the test harness in test_pwp needs to use the ssh connection
    :param main:
    :param test_scenario:
    :return: PwpConfig or None
    """

    if main is None:
        raise PwpError("main is None")
    main.run(test_scenario)
    return main.parser_config if main is not None else None


def pwp_main(arguments=None, test_scenario=None):
    """
    run piwiPre with arguments and test_scenario
    :param arguments: list of actual arguments
    :param test_scenario: scenario for test, or None
    :return: PwpMain
    """
    main = PwpMain(arguments)
    if main.parser_config is None:
        return None
    main.run(test_scenario)
    return main


def pwp_toplevel():
    pwp_main(sys.argv[1:])


# def print_open_file_descriptors():
#     fd_types = {
#         'REG': stat.S_ISREG,
#         'FIFO': stat.S_ISFIFO,
#         'DIR': stat.S_ISDIR,
#         'CHR': stat.S_ISCHR,
#         'BLK': stat.S_ISBLK,
#         'LNK': stat.S_ISLNK,
#         'SOCK': stat.S_ISSOCK,
#     }
#     print("Open file descriptors between 0 and 100\n")
#     for fd in range(100):
#         try:
#             s = os.fstat(fd)  # noqa
#         except OSError:
#             continue
#         msg = f"File descriptor {fd:2} struct= {s}  "
#         for mode, mask in fd_types.items():
#             if mask(s.st_mode):
#                 msg += " " + mode
#         print(msg, flush=True)
#     print("end\n")
#     return


def piwipre_console():
    if '--gui' in sys.argv:
        pwp_main(sys.argv[1:])
    else:
        pwp_main(sys.argv[1:] + ['--gui', 'false'])


def piwipre_gui():
    if '--gui' in sys.argv:
        pwp_main(sys.argv[1:])
    else:
        pwp_main(sys.argv[1:] + ['--gui', 'true'])


if __name__ == "__main__":
    piwipre_gui()
    # NB: default for piwiPre is --gui = false
    # so this runs in console mode if --gui is not specified
