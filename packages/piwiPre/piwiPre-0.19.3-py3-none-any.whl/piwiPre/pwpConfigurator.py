# ---------------------------------------------------------------------------------------------------------------
# piwiPre project
# This program and library is licenced under the European Union Public Licence v1.2 (see LICENCE)
# developed by fabien.battini(at)gmail.com
# ---------------------------------------------------------------------------------------------------------------

import sys
import os
import tkinter
import socket
import termcolor
import platform
import re
import shutil
import threading
import webbrowser
import time
from tkinter import ttk
import tkinter.font

if platform.system() == "Windows":
    import pylnk3

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from piwiPre.pwpVersion import PwpVersion
from piwiPre.pwpParser import PwpParser
from piwiPre.pwpArgsIni import ConstraintHow, ServerSetup, CVS, PwpConstraint, PwpArgType
from piwiPre.pwpGui import GuiLabel, GuiExpandable, PwpGui, GuiStringEditor, GuiDirChooser, GuiButton, GuiRadios, \
    GuiScrollable, GuiFrame, GuiSeparator, GuiValue, GuiGroup, GuiEntry, GuiFolded
from piwiPre.pwpConfig import PwpConfig
from piwiPre.pwpLogoSmall import pwpLogo_png


# REQ 6001: Configurator edits piwiPre.ini files, in text or GUI mode
# REQ 6002: piwiPre has a GUI, that allows to modify args arguments and show the current config file

# REQ 6020: depending on the setup, some configuration items are useless. They are not displayed.
# REQ 6050: String values background is meaningful
#       grey if the unmodified value fromconfig file (aka undo),
#       white if clear
#       green when modified

# REQ 6101: Need to check 'modify' to change values
# REQ 6102: 'directory' fields have a directory chooser UI
# REQ 6103: There is only 1 directory chooser, shared by all usages
# REQ 6104: Need to select 'modify' to modify a value.
# REQ 6105: origin has a button, press to view complete value
# REQ 6106: items are fold-able by category
# REQ 6107: directories are displayed as relative path to CWD
# REQ 6108: when at least 1 item has been modified, "SAVE" and "UNDO" are available, and "Change dir" and "HOME" are not
# REQ 6109: when all items are not modified, "SAVE" and "UNDO" are not available, and "Change dir" and "HOME" are
# REQ 6110 : all widgets have 2 texts: en... , with a global change event.
# REQ 6111: config items window is scrollable with scroll bar and mouse wheel
# REQ 6112:  create piwiPre.bat/sh in the configured directory, with --base and --home
# REQ 6113: verbose/short version of the .ini, depending on --verbose
# REQ 6114: Only 1 setup editor
# REQ 6115: BUG When Configurator is started twice by the test harness, the 2nd time, bold font is bad + an extra window
# REQ 6116: in piwiPre mode, RUN is active even with modification of parameters, but inactive if used once
# REQ 6117: DirChooser: has a "create dir" button
# REQ 6118: DirChooser long directories are managed  with a vertical scrollbar
# REQ 6119: GuiScrollable: has an horizontal scrollbar
# REQ 6120: in piwiPre mode, the cmdline arguments are at the start of screen
# TODO REQ 6121: StringEditor: SHOW/HIDE for passwords
# REQ 6122: the scrollable areas can be scrolled with mouse button when the mouse is over their window
#
# REQ 6124: MINOR bug: messenger is not completely readable through scroll-bar & mouse events
# REQ 6125: when piwiPre is running: run a spinner, disable SAVE, RUN, CANCEL, UNDO

# REQ 6126: Installer can be stopped after launch of Configurator.
# REQ 6127: piwiPre should remember last BASE when config writen (configurator) or piwiPre run
#           When started from main program menu, (or with option --base-last)
#           change dir to that last BASE, otherwise to HOME if BASE does not exist
# REQ 6128: Configurator has an HTML help
# REQ 6129: Backup() use the date (rather than increment numbers).
#
# DONE, by hand: test Configurator and piwiPre GUI without HOME/.piwiPre.ini
# DONE, by hand: test  "pwpInstaller --gui false --mode install --piwipre --ffmpeg "

# --------------------------------------------- GUI Main --------------------------------------------


def equal_path(p1, p2):
    # CAVEAT ! abspath does NOT normalize the character case !
    # so we need to normcase
    return os.path.normcase(os.path.abspath(p1)) == os.path.normcase(os.path.abspath(p2))


class Field:
    def __init__(self, root_gui: 'PwpEditorUI', frm, name: str, constraint: PwpConstraint, row: int, config: PwpConfig):
        self.name = name
        self.frm = frm
        self.root_gui = root_gui
        self.config = config
        self.constraint = constraint

        self.label = GuiLabel(root_gui=root_gui, frm=self.frm, text=name, fr_text=name, column=0, row=row, width=25)

        self.variable = tkinter.StringVar()
        self.change_var = tkinter.StringVar()

        self.how = constraint.how

        self.origin = GuiExpandable(self.frm, column=4, row=row, name=f"Origin of {name}", text="void")

        self.first_value = self.config[self.name]
        self.first_origin = self.config.get_origin(self.name)

        self.prev_value = self.config.get_previous_value(self.name)
        self.prev_origin = self.config.get_previous_origin(self.name)

        self.action_radio = GuiRadios(root_gui=root_gui, frm=self.frm, name=None, fr_name=None,
                                      dico={"undo": "undo", "clear": "inherit", "modify": "modify"},
                                      fr_dico={"undo": "annuler", "clear": "hériter", "modify": "modifier"},
                                      variable=self.change_var, command=self.refresh_value,
                                      column=5, row=row, )

        self.help_label = GuiLabel(root_gui=root_gui, frm=self.frm,
                                   text=constraint.helps, fr_text=constraint.fr_helps,
                                   column=8, row=row, width=self.root_gui.VALUE_WIDTH)

    def suicide(self):
        self.root_gui.remove_widget(self.label)
        self.root_gui.remove_widget(self.action_radio)
        self.root_gui.remove_widget(self.help_label)

    # def show(self, row):
    #     self.label.show(row)
    #     self.origin.show(row)
    #     self.undo_radio.grid(column=5, row=row, sticky="W")
    #     self.clear_radio.grid(column=6, row=row, sticky="W")
    #     self.modify_radio.grid(column=7, row=row, sticky="W")
    #     self.help_label.grid(column=8, row=row, sticky="W")

    @staticmethod
    def create_field(root: 'PwpEditorUI', frm, name: str, row: int,
                     constraint: PwpConstraint,
                     config: PwpConfig):
        if constraint.pwp_type == PwpArgType.BOOL or constraint.pwp_type == PwpArgType.PRESENT:
            res = BoolField(name, row, root, frm, constraint, config)
        elif constraint.pwp_type == PwpArgType.PASSWORD:
            res = PasswordField(root, frm, name, row, constraint, config)
        elif constraint.pwp_type in [PwpArgType.STR, PwpArgType.INT]:  # TODO: add IntField
            res = ValueField(name, row, root, frm, constraint, config)
        elif constraint.pwp_type == PwpArgType.DIR:
            res = DirField(name, row, root, frm, constraint, config)
        else:
            raise OSError
        # We cannot undo() here, because
        # if the server settings have been modified,
        # then the initial values are NOT coming from the file,
        #
        res.first_display()
        return res

    def first_display(self):
        """
        Display the item for the first time after creation is complete
        :return: None
        """
        if self.constraint.origin == 'GUI':
            self.set_value_and_refresh(self.constraint.value, 'GUI', 'modify', refresh=False)
        else:
            self.undo(refresh=False)

    # def pprint(self, val: str):
    #     home = self.root_gui.configurator.home
    #     if val.startswith(home):
    #         return val.replace(home, 'HOME')

    def get_value(self):
        return self.variable.get()

    def get_origin(self):
        return self.origin.get()

    def set_value_and_refresh(self, value, origin, change, refresh=True):
        self.variable.set("true" if value is True else "false" if value is False else str(value))
        self.origin.set(origin)
        self.change_var.set(change)
        if refresh:
            self.root_gui.refresh_main_buttons()

    def undo(self, refresh=True):
        self.set_value_and_refresh(self.first_value, self.first_origin, 'undo', refresh=refresh)

    def clear(self):
        self.set_value_and_refresh(self.prev_value, self.prev_origin, 'clear')

    def modify(self):
        # self.set_value(self.first_value)  # let's keep the existing value, so that we can modify twice
        self.origin.set("GUI")
        self.change_var.set('modify')
        self.root_gui.refresh_main_buttons()

    def refresh_value(self):
        new_mode = self.change_var.get()
        if new_mode == "undo":
            self.undo()
        elif new_mode == "clear":
            self.clear()
        else:
            self.modify()

    # def delete(self):
    #     self.label.destroy()
    #     del self.variable
    #     self.origin.destroy()
    #     if self.change_var:
    #         del self.change_var
    #         self.undo_radio.destroy()
    #         self.clear_radio.destroy()
    #         self.modify_radio.destroy()
    #     self.help_label.destroy()

    # def hide(self):
    #     self.label.grid_forget()
    #     self.origin.grid_forget()
    #     if self.change_var:
    #         self.undo_radio.grid_forget()
    #         self.clear_radio.grid_forget()
    #         self.modify_radio.grid_forget()
    #     self.help_label.grid_forget()


class BoolField(Field):
    def __init__(self, name: str, row: int, root_gui: 'PwpEditorUI', frm, constraint, config: PwpConfig):
        super().__init__(root_gui, frm, name, constraint, row, config)

        if constraint.how == ConstraintHow.CMDLINE:
            self.first_value = constraint.initial == 'true'
            self.prev_value = constraint.initial == 'true'
        # else, the init was correctly done

        self.on_radio = ttk.Radiobutton(self.frm, value="true", text="true", width=self.root_gui.RADIO_WIDTH,
                                        variable=self.variable)
        self.on_radio.grid(column=1, row=row, sticky="W")
        self.off_radio = ttk.Radiobutton(self.frm, value="false", text="false", width=self.root_gui.RADIO_WIDTH,
                                         variable=self.variable)
        self.off_radio.grid(column=2, row=row, sticky="W")

    # def show(self, row):
    #     super().show(row)
    #     self.on_radio.grid(column=1, row=row, sticky="W")
    #     self.off_radio.grid(column=2, row=row, sticky="W")

    # def delete(self):
    #     super().delete()
    #     self.on_radio.destroy()
    #     self.off_radio.destroy()

    # def hide(self):
    #     super().hide()
    #     self.on_radio.grid_forget()
    #     self.off_radio.grid_forget()

    def set_value_and_refresh(self, value, origin, change, refresh=True):
        new_value = "true" if (value is True or value == "true") else "false"
        super().set_value_and_refresh(new_value, origin, change, refresh=refresh)

    def undo(self, refresh=True):
        super().undo(refresh)
        self.on_radio.state(['disabled'])
        self.off_radio.state(['disabled'])

    def modify(self):
        super().modify()
        self.on_radio.state(['!disabled'])
        self.off_radio.state(['!disabled'])

    def clear(self):
        super().clear()
        self.on_radio.state(['disabled'])
        self.off_radio.state(['disabled'])


class ValueField(Field):
    def __init__(self, name: str, row: int, root_gui: 'PwpEditorUI', frm, constraint, config: PwpConfig):
        super().__init__(root_gui, frm, name, constraint, row, config)

        # The 'validate' method to set actually the value is not clear to average users:
        # validation is done only when the widget comes out of focus, which is confusing.
        # a traditional box with OK/Cancel is better.
        # self.validate_cmd = frm.register(self.validate)

        self.item = tkinter.Entry(self.frm, background=PwpGui.GREEN, width=self.root_gui.VALUE_WIDTH,
                                  # validate='focusout',
                                  # validate command=self.validate_cmd,
                                  textvariable=self.variable, state=tkinter.DISABLED)
        self.item.grid(column=1, row=row, sticky="W", columnspan=3)
        self.editor = None

    # def validate(self):
    #     self.father.add_msg(f"'{self.name}' new value = {self.get_value()}\n")
    #     return True

    # def show(self, row):
    #     super().show(row)
    #     self.item.grid(column=1, row=row, sticky="W", columnspan=3)   # noqa

    # def delete(self):
    #     super().delete()
    #     self.item.destroy()

    # def hide(self):
    #     super().hide()
    #     self.item.grid_forget()

    def undo(self, refresh=True):
        super().undo(refresh)
        self.item.configure(disabledbackground=PwpGui.GREY)

    def modify(self, gui=True, x=None, y=None):
        super().modify()
        self.item.configure(disabledbackground=PwpGui.GREY2)  # do this before Editor, otherwise code not reached
        if gui:
            if x is None and y is None:  # x and y are specified while we test
                x, y = self.action_radio.get_xy()
            self.editor = GuiStringEditor(father=self, name=self.name,
                                          initial=self.get_value(), root_gui=self.root_gui,
                                          x=x + 10,
                                          y=y + 10)
            # self.editor.run() this is useless, because the mainloop() is already running

    def clear(self):
        super().clear()
        self.item.configure(disabledbackground=PwpGui.WHITE)


class DirField(ValueField):
    def __init__(self, name: str, row: int, root_gui: 'PwpEditorUI', frm, constraint, config: PwpConfig):
        super().__init__(name, row, root_gui, frm, constraint, config)

    def modify(self, gui=True, x=None, y=None):
        # CAVEAT: we MUST bypass the STRING.modify(), otherwise we end-up in the string editor
        super().modify(gui=False)  # if PwpDirChooser is cancelled, we keep the existing value
        if x is None and y is None:
            x, y = self.action_radio.get_xy()
        GuiDirChooser(self, os.path.abspath(self.variable.get()),
                      self.name, called=self.select_one_dir,
                      home=self.root_gui.initial_home,
                      base=self.root_gui.initial_base,
                      x=x + 10, y=y + 10,
                      language=self.root_gui.language)
        return

    def select_one_dir(self, path):
        self.set_value_and_refresh(path, "GUI", 'modify')


class PasswordField(ValueField):
    def __init__(self, root_gui: 'PwpEditorUI', frm, name: str, row: int, constraint, config: PwpConfig):
        super().__init__(name, row, root_gui, frm, constraint, config)

        self.item.configure(width=self.root_gui.VALUE_WIDTH - 15, show='*')
        self.item.grid(column=1, row=row, sticky="W", columnspan=3)

        self.show_var = GuiButton(root_gui, self.frm,
                                  text="Show" if self.item['show'] == '*' else "Hide",
                                  fr_text="Voir" if self.item['show'] == '*' else "Cacher",
                                  command=lambda: self.show_password(),
                                  column=3, row=row)

    def suicide(self):
        super().suicide()
        self.root_gui.remove_widget(self.show_var)

    # def show(self, row):
    #     super().show(row)
    #     self.item.grid(column=1, row=row, sticky="W", columnspan=3)     # noqa
    #     self.show_var.grid(column=3, row=row, sticky="W")

    # def delete(self):
    #     super().delete()
    #     self.item.destroy()
    #     self.show_var.destroy()

    # def hide(self):
    #     super().hide()
    #     self.item.grid_forget()
    #     self.show_var.grid_forget()

    def show_password(self):
        self.item['show'] = "*" if self.item['show'] == '' else ''
        self.show_var["text"] = " Show " if self.item['show'] == '*' else " Hide "


# ---------------------------------------------  SettingsUi


class PwpSettingsUi(PwpGui):
    instance = None

    def __init__(self, root_gui: "PwpEditorUI", language, x=None, y=None):
        super().__init__("Server settings", language=language)
        if PwpSettingsUi.instance is not None:
            PwpSettingsUi.instance.exit()
            PwpSettingsUi.instance = None
        PwpSettingsUi.instance = self

        self.father = root_gui
        if x is not None and y is not None:
            self.root.geometry(f"+{int(x + 10)}+{y + 10}")

        self.do_album = tkinter.StringVar()
        self.do_thumbnails = tkinter.StringVar()

        self.do_album.set(self.father.album_value.get())
        self.do_thumbnails.set(self.father.thumbnails_value.get())

        row = 0

        self.set_column_sizes([15, 15, 15, 15, 15])
        self.logo = pwpLogo_png.tk_photo()

        self.logo_label = tkinter.Label(self.frm, image=self.logo)
        self.logo_label.grid(column=0, row=row, sticky="W")

        row += 1

        GuiLabel(self, self.frm, column=0, row=row, text=" Action", fr_text="Action", bold=True)

        GuiButton(self, self.frm, column=1, row=row, text="OK", fr_text="OK", command=self.choose)

        GuiButton(self, self.frm, column=2, row=row, text="Undo", fr_text="Annuler", command=self.undo,
                  background=PwpGui.ORANGE)

        GuiButton(self, self.frm, column=3, row=row, text="Exit", fr_text="Abandonner", command=self.exit,
                  background="red")

        # -------------- album
        row += 1
        self.album_radio = GuiRadios(self, self.frm, row=row, column=0,
                                     name="album",
                                     fr_name="album",
                                     variable=self.do_album,
                                     command=self.set_values_from_setup,
                                     dico={"local": "local", "remote": "remote"},
                                     fr_dico={"local": "local", "remote": "distant"},
                                     width=20)
        GuiLabel(self, self.frm, column=6, row=row,
                 text="pictures/video folder after handling",
                 fr_text="dossier des photos/vidéos après traitement",
                 width="", )

        # -------------- thumbnails

        row += 1
        self.thumbnails_radio = GuiRadios(self, self.frm, row=row, column=0,
                                          name="thumbnails",
                                          fr_name="miniatures",
                                          variable=self.do_thumbnails,
                                          command=self.set_values_from_setup,
                                          dico={"local": "local", "remote": "remote", "unused": "unused"},
                                          fr_dico={"local": "local", "remote": "distant", "unused": "inutile"},
                                          width=20)

        GuiLabel(self, self.frm, column=6, row=row,
                 text="thumbnails specific to piwigo server",
                 fr_text="miniatures spécifiques du serveur piwigo",
                 width="", )

    def choose(self):
        album = self.do_album.get()
        thumbnails = self.do_thumbnails.get()

        if self.father:
            self.father.gui_set_album_thumbnails(album, thumbnails)

        print(f"Chose album='{album}', thumbnails='{thumbnails}'")
        self.exit()

    def undo(self):
        album = self.father.initial_album
        thumbnails = self.father.initial_thumbnails
        self.do_album.set(album)
        self.do_thumbnails.set(thumbnails)
        print(f"Reset to album='{album}', thumbnails='{thumbnails}'")
        if self.father:
            self.father.gui_set_album_thumbnails(album, thumbnails)
        # self.exit()

    def set_values_from_setup(self):
        pass


# ---------------------------------------------  PwpEditorUI


class PwpEditorUI(PwpGui):

    def __init__(self, father: "PwpConfigurator", config: PwpConfig or None = None):
        super().__init__("piwiPre", father.language)

        self.en_url = "https://fabien_battini.gitlab.io/piwipre/html/usage/How-to-configure.html"
        self.fr_url = "https://fabien_battini.gitlab.io/piwipre/html/fr/configurer.html"

        self.configurator: PwpConfigurator = father
        self.config = config
        self.suicide = False  # used only with --test-gui, is set to True when it's time to end the UI

        self.do_language = tkinter.StringVar()
        self.do_dir_to_configure = tkinter.StringVar()

        self.do_home = tkinter.StringVar()
        self.do_home_configured = tkinter.StringVar()

        self.do_base = tkinter.StringVar()
        self.do_base_configured = tkinter.StringVar()

        self.do_bat = tkinter.StringVar()

        self.do_verbosity = tkinter.StringVar()

        self.password = None
        self.off_var = None
        self.label_font = tkinter.font.Font(size=9, family="Helvetica", weight="bold")
        row = 0
        PwpSettingsUi.instance = None

        self.initial_home = str(self.configurator.home)
        self.initial_base = str(self.configurator.base)
        self.initial_album = str(self.configurator.album)
        self.initial_thumbnails = str(self.configurator.thumbnails)
        # self.setup_different_from_initial = False   # if True, we need to save the current configuration

        self.set_column_sizes([29, 15, 15, 15, 15, 15, 15, 15, 15])

        # CAVEAT: logo MUST be stored in an attribute, otherwise it is garbage collected !
        self.logo = pwpLogo_png.tk_photo()

        self.logo_label = tkinter.Label(self.frm, image=self.logo)
        self.logo_label.grid(column=0, row=row, sticky="W")

        title_font = tkinter.font.Font(size=14, family="Helvetica", weight="bold")

        lab = ttk.Label(self.frm, font=title_font,
                        text=f" piwiPre  version {PwpVersion.spec} \n")
        lab.grid(column=3, row=row, columnspan=8, sticky="W")

        # -------------- language
        row += 1
        self.language_radio = GuiRadios(self, self.frm, name="Language", fr_name="Langue",
                                        dico={"en": "en", "fr": "fr"},
                                        fr_dico={"en": "en", "fr": "fr"},
                                        command=self.__gui_set_language,
                                        variable=self.do_language,
                                        column=0, row=row)

        self.help_button = GuiButton(self, self.frm, column=5, row=row, text="Help", fr_text="Aide",
                                     background="blue",
                                     command=lambda: webbrowser.open(self.en_url if self.language == "en"
                                                                     else self.fr_url), )

        GuiLabel(self, self.frm, column=6, row=row,
                 text="Online Help",
                 fr_text="Aide en ligne",
                 width=55)

        # -------------- BASE
        row += 1
        GuiLabel(self, self.frm, column=0, row=row, text="BASE", fr_text="BASE", bold=True)

        self.do_base.set(self.configurator.base)
        self.base_entry = tkinter.Entry(self.frm, width=PwpGui.VALUE_WIDTH,
                                        textvariable=self.do_base, state=tkinter.DISABLED)
        self.base_entry.grid(column=1, row=row, sticky="W", columnspan=3)

        # TODO: add a button to change BASE among the registered BASES in HOME/.piwiPre.history
        # self.set_base_button = GuiButton(self, self.frm, row=row, column=5,
        #                                  text="Change BASE",
        #                                  fr_text="Changer BASE", command=self.launch_change_base)
        # self.parameters_menu.add_item(self.set_base_button)

        GuiLabel(self, self.frm, column=6, row=row,
                 text="You can configure another BASE and switch to it",
                 fr_text="On peut configurer une autre BASE, et s'y déplacer",
                 width="")

        # -------------- Execute

        row += 1
        GuiLabel(self, self.frm, text="Run piwiPre", fr_text="Exécuter piwiPre",
                 bold=True, column=0, row=row, width="")

        self.run_button = GuiButton(self, self.frm, column=1, row=row,
                                    text="Run", fr_text="Exécuter",
                                    command=self.__run)

        self.spinner = ttk.Progressbar(self.frm, orient="horizontal", maximum=50,
                                       mode="indeterminate", length=240)
        self.spinner.grid(column=2, row=row, sticky="W", columnspan=3, )
        # self.spinner.start(0)

        GuiButton(self, self.frm, column=5, row=row, text="Quit", fr_text="Quit",
                  command=self.exit, background="red")

        GuiLabel(self, self.frm, column=6, row=row,
                 text="Stop current processing",
                 fr_text="Arrêter le travail courant",
                 width=55)
        # -------------- Configure

        row += 1
        GuiLabel(self, self.frm, text="Change config", fr_text="Changer la configuration",
                 bold=True, column=0, row=row, width="")

        self.configure_params_button = GuiButton(self, self.frm, row=row, column=5,
                                                 text="Parameters",
                                                 fr_text="Paramètres", command=self.__gui_change_parameters)

        GuiLabel(self, self.frm, column=6, row=row,
                 text="Change the configuration temporarily or definitely",
                 fr_text="Changer la configuration de façon temporaire ou définitive",
                 width=55)
        # --------------------------------------------------------------------
        # -------------- Separator    : Parameters Menu

        row += 1

        self.parameters_menu = GuiFolded(self.frm, width=1440, height=0, row=row,
                                         column_sizes=self.column_sizes, columnspan=9)
        sub_row = 0

        self.sep0 = GuiSeparator(self, self.parameters_menu, row=sub_row,
                                 text="Change parameters",
                                 fr_text="Changer les paramètres")

        sub_row += 1

        GuiLabel(self, self.parameters_menu, column=0, row=sub_row,
                 text="Cancel configuration", fr_text="Annuler la configuration",
                 width="", bold=True)

        self.undo_button = GuiButton(self, self.parameters_menu, column=3, row=sub_row,
                                     text="Cancel Param",
                                     fr_text="Annuler Param",
                                     command=lambda: self.parameters_menu.hide() or self.configure_menu.hide(),
                                     background=PwpGui.ORANGE)

        sub_row += 1
        GuiLabel(self, self.parameters_menu, column=0, row=sub_row,
                 text="...", fr_text="...",
                 width="", bold=True)

        # --------------------------------------------------------------------------------
        # -------------- Separator    : Configure Menu
        # Configure Menu starts hidden

        self.configure_menu = GuiGroup()

        row += 1
        self.sep1 = GuiSeparator(self, self.frm, row=row,
                                 text="Configure a directory",  # CAVEAT: text will be dynamically changed
                                 fr_text="Configurer un dossier")
        self.configure_menu.add_item(self.sep1)

        # -------------- Dir to configure

        row += 1
        label1 = GuiLabel(self, self.frm, column=0, row=row, bold=True,
                          text="Directory",
                          fr_text="dossier")
        self.configure_menu.add_item(label1)
        self.do_dir_to_configure.set(self.configurator.dir_to_configure)

        entry1 = GuiEntry(self.frm, width=PwpGui.VALUE_WIDTH,
                          textvariable=self.do_dir_to_configure, column=1, row=row, columnspan=3)
        self.configure_menu.add_item(entry1)

        self.save_button = GuiButton(self, self.frm, column=4, row=row, text="Write config", fr_text='Écrit config',
                                     command=self.__save)
        self.configure_menu.add_item(self.save_button)

        self.exec_no_save_button = GuiButton(self, self.frm, column=5, row=row,
                                             text="Exec no save", fr_text="Exec sans sauve",
                                             command=self.__run_no_save)
        self.configure_menu.add_item(self.exec_no_save_button)

        # ----------------------------------------------------------
        row += 1

        radios2 = GuiRadios(self, self.frm,
                            name="Verbosity of ini file",
                            fr_name="Verbosité du fichier .ini",
                            row=row,
                            dico={'true': "on", "false": "off"},
                            fr_dico={'true': "oui", "false": "non"},
                            command=lambda: True,  # self.set_values_from_setup,  # no need to compute again the setup
                            variable=self.do_verbosity,
                            width=20)
        self.configure_menu.add_item(radios2)

        label3 = GuiLabel(self, self.frm, column=6, row=row,
                          text="if true, .ini is really self documented, else minimal doc",
                          fr_text="si 'oui', le fichier .ini est très documenté, sinon minimal",
                          width=55)
        self.configure_menu.add_item(label3)

        # ----------------------------------------------------------
        row += 1

        self.bat_radio = GuiRadios(self, self.frm, row=row, column=0,
                                   name="build local shortcuts",
                                   fr_name="Raccourcis locaux",
                                   variable=self.do_bat,
                                   command=self.__from_ui_to_python_to_ui,
                                   dico={"true": "true", "false": "false"},
                                   fr_dico={"true": "oui", "false": "non"},
                                   width=20)
        self.configure_menu.add_item(self.bat_radio)

        self.bat_radio_label = GuiLabel(self, self.frm, column=6, row=row,
                                        text="Allows to start piwiPre from the file explorer",
                                        fr_text="Permet de démarrer piwiPre depuis l'explorateur de fichiers",
                                        width=55)
        self.configure_menu.add_item(self.bat_radio_label)

        # -------------- Album settings

        row += 1
        self.album_label = GuiLabel(self, self.frm, text="Album", fr_text="Album",
                                    column=0, row=row, bold=True, width="")
        self.configure_menu.add_item(self.album_label)

        self.album_value = GuiValue(self, self.frm, column=1, row=row, width=10,
                                    dico={"local": "local", "remote": "remote"},
                                    fr_dico={"local": "local", "remote": "distant"})
        self.configure_menu.add_item(self.album_value)

        self.thumbnails_label = GuiLabel(self, self.frm, text="Thumbnails", fr_text="Miniatures",
                                         column=2, row=row, bold=True, width="")
        self.configure_menu.add_item(self.thumbnails_label)

        self.thumbnails_value = GuiValue(self, self.frm, column=3, row=row, width=10,
                                         dico={"local": "local", "remote": "remote", "unused": "unused"},
                                         fr_dico={"local": "local", "remote": "distant", "unused": "inutile"})
        self.configure_menu.add_item(self.thumbnails_value)

        self.settings_ui = None
        self.modify_button = GuiButton(self, self.frm, text="modify", fr_text="modifier",
                                       command=self.__run_settings,
                                       column=4, row=row)
        self.configure_menu.add_item(self.modify_button)

        # -------------- Separator
        # row += 1
        # self.sep3 = GuiSeparator(frm=self.frm, row=row, text="Change settings")

        # -------------- Variable items
        row += 1
        self.max_common_row = row
        self.multi_level = None
        self.enclosing = None

        sizes = [25, 21, 18, 13, 35, 20, 10, 10, ]
        all_sizes = sizes + [200 - sum(sizes)]

        self.enclosing = GuiFrame(self.frm, width=1410, height=410, row=row, column=0,
                                  column_sizes=all_sizes,
                                  columnspan=9)
        self.configure_menu.add_item(self.enclosing)

        # caveat: columns in multilevel are managed in multilevel, NOT here !

        GuiLabel(self, self.enclosing, column=0, row=0, text="item", fr_text="item", bold=True, width="")
        GuiLabel(self, self.enclosing, column=1, row=0, text="value", fr_text="valeur", bold=True, width="")
        GuiLabel(self, self.enclosing, column=4, row=0, text="origin", fr_text="origine", bold=True, width="")
        GuiLabel(self, self.enclosing, column=5, row=0, text="action", fr_text="action", bold=True, width="")
        GuiLabel(self, self.enclosing, column=6, row=0, text="help", fr_text="aide", bold=True, width="")
        # -------------- messages
        row += 1
        self.add_messager(row=row, title="Messages", fr_title="Messages", height=10)

        # ======================================= Self Test

        if father.do_tests:
            self.spinner.start(10)
            self.root.after(1000, self.__scenario_0)
        self.__from_python_to_ui()

    def __gui_change_parameters(self):
        hierarchy = self.config.get_hierarchy()
        # hierarchy it the list of configuration FILES? not directories.
        # CAVEAT: is BASE is not configured, it will be not int hierarchy
        base = self.configurator.base + '\\piwiPre.ini'
        if base not in hierarchy:
            hierarchy.append(base)
        row = 2

        self.parameters_menu.delete_all()

        for item in hierarchy:
            if item == 'DEFAULT':
                pass
            else:
                if item == self.configurator.home + '\\.piwiPre.ini':
                    txt = 'HOME'
                elif item == self.configurator.base + '\\piwiPre.ini':
                    txt = "BASE"
                else:
                    txt = "OTHER"
                label = GuiLabel(self, self.parameters_menu, column=0, row=row,
                                 text=txt, fr_text=txt,
                                 width="", bold=True)
                self.parameters_menu.add_item(label)

                path = os.path.dirname(item)
                value = GuiLabel(self, self.parameters_menu, column=1, row=row,
                                 text=path, fr_text=path,
                                 width="", relief=True)
                self.parameters_menu.add_item(value)

                if os.path.isfile(item):
                    conf_val_fr = "Configuré"
                    conf_val_gb = "Configured"
                else:
                    conf_val_fr = "NON Configuré"
                    conf_val_gb = "NOT Configured"

                conf = GuiLabel(self, self.parameters_menu, column=2, row=row,
                                text=conf_val_fr, fr_text=conf_val_gb,
                                width=16, relief=True)
                self.parameters_menu.add_item(conf)

                action = GuiButton(self, self.parameters_menu, column=3, row=row,
                                   text="Configure", fr_text="Configurer",
                                   command=lambda: self.__launch_configure(path))

                self.parameters_menu.add_item(action)
                row += 1

        label2 = GuiLabel(self, self.parameters_menu, column=0, row=row,
                          fr_text="Sous-dossier",
                          text="Sub-directory",
                          width="", bold=True)
        self.parameters_menu.add_item(label2)

        conf2 = GuiLabel(self, self.parameters_menu, column=1, row=row,
                         text="value to choose", fr_text="Valeur à choisir",
                         width="")
        self.parameters_menu.add_item(conf2)

        action2 = GuiButton(self, self.parameters_menu, column=3, row=row,
                            text="Chose", fr_text="Choisir",
                            command=lambda: self.__launch_configure_other(action2))
        self.parameters_menu.add_item(action2)
        help2 = GuiLabel(self, self.parameters_menu, column=4, row=row,
                         text="CAVEAT: BASE must be configured before its sub-dirs",
                         fr_text="ATTENTION: il faut configurer BASE avant ses sous-dossiers éventuels",
                         width=55)
        self.parameters_menu.add_item(help2)

        if not self.configurator.base_is_configured:
            action2.disable()
            # cannot configure a subdirectory unless BASE is configured

        self.parameters_menu.show()  # un-hide the change parameters menu

    def __run_settings(self):
        self.settings_ui = PwpSettingsUi(self, language=self.language,
                                         x=self.modify_button.winfo_rootx(),
                                         y=self.modify_button.winfo_rooty())

    def msg(self, line):
        self.configurator.msg(line)

    def __scenario_0(self):
        val_field: ValueField = self.multi_level.all_lines['ssh-user']
        self.root.after(2 * 1000, self.__scenario_0p1)
        val_field.modify(x=50, y=50)

    def __scenario_0p1(self):
        val_field: ValueField = self.multi_level.all_lines['ssh-user']
        editor: GuiStringEditor = val_field.editor
        editor.choose()
        self.root.after(1000, self.__scenario1)

    def __scenario1(self):
        modify_setting = self.modify_button
        modify_setting.invoke()
        self.root.after(1 * 1000, self.settings_ui.undo)
        self.root.after(2 * 1000, self.settings_ui.choose)
        self.root.after(3 * 1000, self.__scenario2)

    def __scenario2(self):
        album = self.multi_level.all_lines['album']
        origin: GuiExpandable = album.origin
        origin.show_info(event=None, x=10, y=10)
        self.root.after(1 * 1000, origin.hide_info)
        self.root.after(2 * 1000, lambda: GuiDirChooser.running_chooser.enter('..'))
        self.root.after(3 * 1000, lambda: GuiDirChooser.running_chooser.select('ALBUM'))
        self.root.after(4 * 1000, self.__scenario3)
        album.modify()

    def __scenario3(self):
        thumbnails = self.multi_level.all_lines['thumbnails']
        self.root.after(3 * 1000, lambda: GuiDirChooser.running_chooser.enter('..'))
        self.root.after(4 * 1000, lambda: GuiDirChooser.running_chooser.select('thumbnails'))
        self.root.after(5 * 1000, self.__run)
        self.root.after(5500, self.__scenario_suicide)
        thumbnails.modify()

    def __scenario_suicide(self):
        if self.suicide:
            # this is set to True when piwiPre is finished
            self.exit()
        else:
            self.root.after(200, self.__scenario_suicide)

    def __display_multilevel(self, start_row):
        if self.multi_level is not None:
            self.multi_level.suicide()
            del self.multi_level

        self.multi_level = GuiScrollable(self, self.enclosing, row=start_row + 1, name="multilevel",
                                         column_sizes=[25, 20, 18, 12, 18, 10, 10, 10, 38])
        row = 0
        level_0_shown = False
        level_1_shown = False
        level_2_shown = False

        if equal_path(os.path.dirname(self.do_dir_to_configure.get()), self.configurator.base):
            my_range = range(0, 3)
        else:
            my_range = range(1, 3)

        for stage in my_range:
            row += 1

            for name in self.configurator.current_constraints:
                father: 'PwpConfigurator' = self.configurator
                constraint: PwpConstraint = father.get_constraint(name)

                if constraint.how == ConstraintHow.HIDDEN:
                    continue

                if stage == 0:
                    if constraint.how != ConstraintHow.CMDLINE:
                        continue
                if stage == 0 and not level_0_shown:
                    self.multi_level.add_level(row=row,
                                               label="Items only on cmdline, cannot be saved in .ini",
                                               fr_label="Items seulement en argument, pas écrits en .ini")
                    level_0_shown = True
                    row += 1

                if stage == 1:
                    if constraint.how == ConstraintHow.FORCED:
                        continue
                    elif constraint.how == ConstraintHow.CMDLINE:
                        continue
                if stage == 1 and not level_1_shown:
                    self.multi_level.add_level(row=row,
                                               label="Items that can be saved in .ini",
                                               fr_label="Items qui peuvent être écrits dans .ini")
                    row += 1
                    level_1_shown = True

                if stage == 2:
                    if constraint.how != ConstraintHow.FORCED:
                        continue

                if stage == 2 and not level_2_shown:
                    self.multi_level.add_level(row=row,
                                               label="Items forced by the server setup",
                                               fr_label="Items forcés par le setup du serveur")
                    row += 1
                    level_2_shown = True

                self.multi_level.add_item(Field.create_field(root=self, frm=self.multi_level.frm,
                                                             name=name, row=row,
                                                             constraint=constraint, config=self.config),
                                          name)
                row += 1

    def gui_set_album_thumbnails(self, album, thumbnails):
        self.album_value.set(album)
        self.thumbnails_value.set(thumbnails)
        self.__from_ui_to_python_to_ui()

    def refresh_main_buttons(self):
        # modified is True when the configuration of the directory being managed has changed
        # the goal is to know if we have to save it
        modified = False

        self.parameters_menu.refresh()

        for field in self.multi_level.all_lines.values():
            st = field.change_var.get()
            if st != "undo":
                modified = True
                break
            # NB: here, we are paranoid.
            #     we say modified as soon as status != undo
            #     so that it is clear to the user that "UNDO" or "SAVE"
            #     must be explicitly used to exit from the edition mode

        # The following if/then/else is not really useful
        # maybe we should ALWAYS allow to write file and exec without saving
        if modified:
            self.save_button.enable()
            self.exec_no_save_button.enable()
        else:
            self.save_button.disable()
            self.exec_no_save_button.disable()

        # run_button
        if equal_path(self.do_dir_to_configure.get(), self.configurator.base):
            # we are editing config file in CWD, run is possible
            self.run_button.enable()
        else:
            self.run_button.disable()

        if equal_path(self.do_dir_to_configure.get(), self.configurator.home):
            self.sep1.set(text="Configure a directory : [HOME]",
                          fr_text="Configurer un dossier : [HOME]")
        elif equal_path(self.do_dir_to_configure.get(), self.configurator.base):
            self.sep1.set(text="Configure a directory : [BASE]",
                          fr_text="Configurer un dossier : [BASE]")
        else:
            self.sep1.set(text="Configure a sub-directory of BASE",
                          fr_text="Configurer un sous-dossier de BASE")

        # This was RE Q 01312
        # but, if no secrets are used, there is NO reason to have HOME configured.
        #
        # if equal_path(self.do_dir_to_configure.get(), self.configurator.base) and self.configure_menu.on:
        #     self.bat_radio.show()
        #     self.bat_radio_label.show()
        #     self.exec_no_save_button.show()
        # else:
        #     self.bat_radio.hide()
        #     self.bat_radio_label.hide()
        #     self.exec_no_save_button.hide()

        self.msg(f"HOME               : '{self.configurator.home}'")
        self.msg(f"HOME is configured : '{self.configurator.home_is_configured}'")
        self.msg(f"BASE               : '{self.configurator.base}'")
        self.msg(f"BASE is configured : '{self.configurator.base_is_configured}'")

        self.do_dir_to_configure.set(self.configurator.dir_to_configure)

    def __gui_set_dir(self, path):
        self.do_dir_to_configure.set(path)
        self.__from_ui_to_python_to_ui()

    def __launch_configure_other(self, button):
        # Here, we change the directory being configured, but we do not change HOME or BASE
        # First, select the directory to be configured, starting from BASE
        # then, configure it
        self.__gui_set_dir(self.do_base.get())
        x = button.winfo_rootx()
        y = button.winfo_rooty()
        GuiDirChooser(self, os.path.abspath(self.do_dir_to_configure.get()),
                      "Other directory",
                      home=self.initial_home,
                      base=self.initial_base,
                      called=self.__continue_configure_other,
                      x=x + 10, y=y + 10,
                      language=self.language)

    def __continue_configure_other(self, path):
        # caveat: path is relative to BASE
        abs_path = os.path.abspath(self.configurator.base + '/' + path)
        self.__gui_set_dir(abs_path)
        self.configure_menu.show()

    def __launch_configure(self, path):
        self.configure_menu.show()
        self.__gui_set_dir(path)

    def __gui_set_language(self):
        self.set_language(self.do_language.get())

    def set_language(self, language):
        self.configurator.language = language
        super().set_language(language)

    def __from_ui_to_python_to_ui(self):
        self.__from_ui_to_python()
        self.__from_python_to_ui()

    def __from_ui_to_python(self):
        new_language = self.do_language.get() or 'en'
        new_album: CVS = CVS.from_str(self.album_value.get())  # LOCAL, REMOTE
        new_thumbnails: CVS = CVS.from_str(self.thumbnails_value.get())  # LOCAL, REMOTE, UNUSED
        new_home = self.do_home.get()
        new_cwd = self.do_base.get()
        new_dir_to_configure = self.do_dir_to_configure.get()

        if self.configurator.language != new_language:
            self.configurator.language = new_language
            self.set_language(new_language)

        config_has_changed = (self.configurator.dir_to_configure != new_dir_to_configure or
                              self.configurator.home != new_home or
                              self.configurator.base != new_cwd)
        # if config_has_changed, we need to read again the config

        self.configurator.setup_has_changed = (
                self.configurator.dir_to_configure != new_dir_to_configure or
                self.configurator.album != new_album or
                self.configurator.thumbnails != new_thumbnails or
                self.configurator.home != new_home or
                self.configurator.base != new_cwd)
        # if setup_has_changed, we will compute again the constraints
        # in from python_to_ui

        self.configurator.dir_to_configure = new_dir_to_configure
        self.configurator.album = new_album
        self.configurator.thumbnails = new_thumbnails
        self.configurator.home = new_home
        self.configurator.base = new_cwd

        self.configurator.home_is_configured = os.path.isfile(self.configurator.home + '/.piwiPre.ini')
        self.configurator.base_is_configured = os.path.isfile(self.configurator.base + '/piwiPre.ini')

        # We want to force to configure directories in a logical order: HOME - BASE - SUB-DIRS
        # BUT we do not do it at this level,
        # because this cannot be understood by the user
        # instead, we do it at the UI level.

        # if self.configurator.home_is_configured:
        #     if not self.configurator.base_is_configured:
        #         self.configurator.dir_to_configure = self.configurator.base
        # else:
        #     self.configurator.dir_to_configure = self.configurator.home

        self.configurator.bat = self.do_bat.get() == "true"
        self.configurator.verbose = self.do_verbosity.get() == "true"

        # copy the values from the multi_level in the GUI to python
        for name, field in self.multi_level.all_lines.items():
            self.configurator.set_value(name, field.get_value(), field.get_origin())

        if config_has_changed:
            self.configurator.set_dir_and_config(self.configurator.dir_to_configure, None)
        self.configurator.compute_constraints()

    def __from_python_to_ui(self):
        self.set_language(self.configurator.language)

        self.do_language.set(self.configurator.language)
        self.album_value.set(str(self.configurator.album))
        self.thumbnails_value.set(str(self.configurator.thumbnails))
        self.do_bat.set("true" if self.configurator.bat else 'false')
        self.do_verbosity.set("true" if self.configurator.verbose else 'false')

        self.do_home.set(self.configurator.home)

        self.do_base.set(self.configurator.base)

        self.do_dir_to_configure.set(self.configurator.dir_to_configure)
        self.config = self.configurator.config

        self.__display_multilevel(self.max_common_row)
        self.refresh_main_buttons()

    def undo(self):
        #  Go back to all previous values for the dir to configure
        self.album_value.set(self.initial_album)
        self.thumbnails_value.set(self.initial_thumbnails)
        # self.do_home.set(self.initial_home)
        # self.do_cwd.set(self.initial_cwd)

        for name, field in self.multi_level.all_lines.items():
            field.undo()
        self.__from_ui_to_python_to_ui()

    def __run(self):
        # TODO: BUG: __run() and __run_no_save() are identical, which is NOT possible !
        self.__from_ui_to_python()
        self.configurator.run()

    def __run_no_save(self):
        # TODO: Verify that we take into account unsaved arguments
        self.__from_ui_to_python()
        self.configurator.run()

    def __save(self):
        self.__from_ui_to_python()
        self.configurator.save()

# ------------------------------------------------------------------------------------------
# class PwpConfigurator
# ------------------------------------------------------------------------------------------


class PwpConfigurator:
    def __init__(self,
                 config: PwpConfig or None = None,
                 pwp_main=None,
                 logger=None,
                 action=None,
                 test_scenario=None):

        self.ui: PwpEditorUI or None = None
        self.pwp_main = pwp_main
        self.logger = logger
        self.action = action
        self.config = config
        self.language = config['language']

        self.file_to_configure = None
        self.dir_to_configure = None

        self.home = os.path.abspath(config['home'] or os.path.expanduser("~"))
        self.base = os.getcwd()  # initially, piwiPre has done a chdir, so BASE is always os.getcwd()  # noqa

        self.build_for_home = None  # means dir_to_configure == HOME
        self.home_is_configured = os.path.isfile(self.home + '/.piwiPre.ini')
        self.base_is_configured = os.path.isfile(self.base + '/piwiPre.ini')

        self.album = CVS.LOCAL  # will be set by set_dir_and_config
        self.thumbnails = CVS.UNUSED  # will be set by set_dir_and_config

        self.do_tests = config["test-gui"]
        self.do_gui = config["gui"]
        self.bat = True
        self.verbose = False
        self.setup_has_changed = False
        target = '.'
        if self.home_is_configured:
            if not self.base_is_configured:
                target = self.base
        else:
            target = self.home

        self.test_scenario = test_scenario
        if test_scenario:
            if "album-setup" in test_scenario:
                self.album = CVS.from_str(test_scenario["album-setup"])
            if "thumbnails-setup" in test_scenario:
                self.thumbnails = CVS.from_str(test_scenario["thumbnails-setup"])
            if "gui" in test_scenario:
                self.do_gui = test_scenario["gui"]

        self.current_constraints: dict[str, PwpConstraint] = {}
        self.parser = PwpParser(program="piwiPre", parse_args=False, with_config=False)
        self.set_dir_and_config(target, config)

    def run_or_display(self):
        if self.test_scenario:
            if self.ui:
                self.ui.spinner.start(10)
            self.setup_has_changed = True
            self.compute_constraints()
            if self.test_scenario:
                # CAVEAT: Here, we know that the UI is not managed,
                # so, we modify directly the data inside the constraints
                # if the UI was to be used, we would need to modify the UI data instead
                if "set album" in self.test_scenario:
                    self.set_value("album", self.test_scenario["set album"], "GUI")
                if "set thumbnails" in self.test_scenario:
                    self.set_value('thumbnails', self.test_scenario["set thumbnails"], "GUI")

                if "save" in self.test_scenario and self.test_scenario["save"] == 'true':
                    self.save()
                if "run" in self.test_scenario and self.test_scenario["run"] == 'true':
                    self.__run()
                if "exit" in self.test_scenario and self.test_scenario["exit"] == 'true':
                    self.exit()
                if self.ui:
                    self.ui.spinner.stop()
        elif not self.do_gui:
            self.run()
        else:
            self.setup_has_changed = True
            self.compute_constraints()
            self.ui = PwpEditorUI(self, self.config)
            if self.logger:
                self.logger.add_gui(self.ui)
            if self.ui.root is None:  # pragma: no cover : defensive code
                self.ui = None
                self.msg("unable to start TK")
                return
            self.ui.mainloop()

            if self.logger:
                self.logger.add_gui(None)

    def exit(self):
        if self.ui:
            self.ui.exit()
        if self.logger:
            self.logger.add_gui(None)

    def set_dir_and_config(self, path, config):
        path = os.path.abspath(path)
        self.build_for_home = equal_path(path, self.home)
        self.dir_to_configure = path
        pp = path + ('/' if platform.system() != "Windows" else '\\')
        self.file_to_configure = pp + ('.' if self.build_for_home else '') + 'piwiPre.ini'

        self.msg(f"target directory   : '{self.dir_to_configure}'")
        if self.build_for_home:
            self.bat = False
            self.msg("target file          : HOME/.piwiPre.ini with confidential information")
        else:
            self.bat = True
            self.msg(f"target file        : '{self.file_to_configure}' ")

        # if config is set, then we do not need to parse the configuration file again
        self.config = config or self.parser.parse_for_dir(path, self.home, self.base, self.language)

        self.album = CVS.REMOTE if self.config['enable-remote-album'] else CVS.LOCAL
        self.thumbnails = (CVS.UNUSED if self.config['enable-thumbnails'] is False
                           else CVS.REMOTE if self.config['enable-remote-thumbnails']
                           else CVS.LOCAL)

    def build_config(self, home, cwd, path):
        cwd = os.path.abspath(cwd)
        path = os.path.abspath(path)
        if not path.startswith(cwd):
            self.warning(f"CWD                    = '{cwd}'")
            self.warning(f"directory to configure = '{path}'")
            self.warning("path is NOT a sub-directory of CWD : ABORT")
            return self.config
        return self.parser.parse_for_dir(path, home, cwd, self.language)

    def get_constraint(self, name) -> PwpConstraint:
        """
        get_values(self, name):
        :param name:
        :return: PwpConstraint
        """
        return self.current_constraints[name]

    def set_value(self, name: str, value: str, origin: str):
        self.current_constraints[name].value = value
        self.current_constraints[name].origin = origin

    def compute_constraints(self):
        if not self.setup_has_changed:
            return

        self.warning("Applying constraints from album/thumbnail setup ")
        self.msg(f"HOME       : {str(self.home)}")
        self.msg(f"BASE       : {str(self.base)}")
        self.msg(f"ALBUM      : {str(self.album)}")
        self.msg(f"THUMBNAILS : {str(self.thumbnails)}")
        setup = ServerSetup(album=self.album, thumbnails=self.thumbnails)

        self.current_constraints = self.parser.get_constraints_for_setup(setup=setup,
                                                                         config=self.config)
        self.setup_has_changed = False

    def copy(self, src, dst):
        """
        copy src to dst, unless dryrun is True
        :param src: file to copy
        :param dst: destination filename
        :return: None
        """
        base = os.path.dirname(dst)
        if not os.path.isdir(base):
            os.makedirs(base, exist_ok=True)

        if not os.path.isfile(src):
            self.warning(f"FAILED copy '{src}' ->  '{dst}' : non existing source")

        shutil.copy2(src, dst)  # preserve metadata

        if os.path.isfile(dst):
            self.msg(f"copy '{src}' ->  '{dst}'")
        else:
            self.warning(f"copy '{src}' ->  '{dst}'")

    def backup(self, filename):
        if not os.path.isfile(filename):
            return

        bak = filename + time.strftime("-%Y-%m-%d-%Hh%M-%S.bak")
        # m1 = re.match(r"(.*)\.bak$", filename)
        # m2 = re.match(r"(.*)\.bak-(\d*)$", filename)
        # if m1:
        #     bak = f"{m1.group(1)}.bak-1"
        # elif m2:
        #     num = int(m2.group(2))
        #     bak = f"{m2.group(1)}.bak-{num + 1}"
        # else:
        #     bak = filename + '.bak'
        #
        # self.backup(bak)
        self.copy(filename, bak)

    def compute_new_config(self):
        dico = {}
        # let's compute the value of config parameters we want to write in the config file
        # CAVEAT: We want to keep the values from the current config file that have NOT been modified
        #         by the GUI. For instance the 'names' item.
        # CAVEAT: when the parameter is inherited from a previous config
        # - in the GUI, we display the previous value (and the previous origin)
        # - in the saved config file, we want to not set the value,
        #   so that, in the case we change the previous config file, that new value will be inherited.
        #   The alternative would be to write again the previous value,
        #   in this case, any change of the previous file is NOT inherited,

        for name in self.config:
            if name in self.current_constraints:
                cc: PwpConstraint = self.current_constraints[name]
                uv = cc.value

                if cc.how == ConstraintHow.CMDLINE:
                    # we do not put CMDLINE items in the config files.
                    continue

                if cc.origin == "GUI":  # NB: "GUI" is always higher case.
                    pass  # we will write  it in the config file
                elif uv is None or not equal_path(cc.origin, self.config.filename):
                    # it means that the value is inherited from a previous config
                    # so, we will NOT write the value in the config file
                    continue

                val = (uv if uv in ["", 'true', 'false', 'TRIAGE', 'BACKUP', 'ALBUM', 'THUMBNAILS', 'fr', 'en']
                       else int(uv) if cc.pwp_type == PwpArgType.INT
                       else os.path.abspath(uv) if cc.pwp_type == PwpArgType.DIR
                       else f'{uv}')
                dico[name] = val
            else:
                # this is a config item not managed by the GUI
                if equal_path(self.config.origin[name], self.config.filename):
                    # it was set on THIS config file, we keep its value,
                    dico[name] = self.config[name]
                else:
                    pass
                    # otherwise we keep it unset in order to enable inheritance

        new_config = PwpConfig(filename="GUI", dico=dico, previous=self.config.previous)
        return new_config

    def run(self):
        # run piwiPre in BASE
        if self.ui:
            self.ui.spinner.start(10)
        new_config = self.compute_new_config()

        if self.ui:
            self.ui.save_button.disable()
        self.pwp_main.parser_config = new_config.merge_ini(self.pwp_main.parser_config)
        self.action()
        if self.ui:
            self.ui.spinner.stop()
        return

    def save(self):
        # save config file being edited
        new_config = self.compute_new_config()

        self.backup(self.file_to_configure)
        base = os.path.dirname(self.file_to_configure)
        if not os.path.isdir(base):
            os.makedirs(base, exist_ok=True)

        prologue = f"""
# file generated by piwiPre Configurator
#
# file       :  '{self.file_to_configure}'
#
# album      :  '{self.album}'
# thumbnails :  '{self.thumbnails}'
# language   :  '{self.language}'
#
"""

        self.parser.write_ini_file(self.file_to_configure, lang=self.language, config=new_config,
                                   verbose=self.verbose, prologue=prologue)

        self.msg(f"Generated  '{self.file_to_configure}' ")

        if self.bat:
            piwipre_path = (os.environ['PROGRAMFILES(X86)'] + '\\piwiPre\\'  # noqa
                            if platform.system() == "Windows" else "")

            def build_file(file_name, program, gui_flag):
                if platform.system() == "Windows" and gui_flag:
                    pylnk3.for_file(f'{piwipre_path}{program}.exe',
                                    file_name, arguments='--gui true', window_mode="Minimized")
                    return

                with open(file_name, "w", encoding="utf8") as f:
                    if platform.system() != "Windows":
                        f.write("#!/bin/sh \n")

                    cur_dir = self.base
                    home = os.path.relpath(self.home, cur_dir)
                    f.write("# file generated by pwpConfigurator\n")
                    f.write("#\n")
                    f.write(f"# file       =  '{self.file_to_configure}'\n")
                    f.write("#\n")
                    f.write(f"# album      =  '{self.album}'\n")
                    f.write(f"# thumbnails =  '{self.thumbnails}'\n")
                    f.write("#\n")
                    flag = "true" if gui_flag else "false"
                    if platform.system() == "Windows":
                        f.write(f'"{piwipre_path}{program}.exe" --gui {flag} --base "{cur_dir}" --home "{home}" %*\n')
                    else:
                        f.write(f'{program} --gui {flag} --base "{cur_dir}" --home "{home}"  &\n')
                    f.write("\n")
                    self.msg(f"Generated  '{file_name}' ")

            filename = base + ("\\piwiPreCmd.bat" if platform.system() == "Windows" else '/piwiPreCmd.sh')
            build_file(filename, "piwiPre", False)

            filename = base + ("\\piwiPreGui.lnk" if platform.system() == "Windows" else '/piwiPreGui.sh')
            build_file(filename, "piwiPre", True)

        if not self.build_for_home:
            self.save_latest_cwd()

    def msg(self, line):
        if self.ui:
            self.ui.gui_msg(line)
        print(f"msg     {line}")

    def warning(self, line):
        if self.ui:
            self.ui.gui_warning(line)

        print(termcolor.colored("WARNING : " + line, color='red', force_color=True))

    def save_latest_cwd(self):
        current_host = socket.gethostname()
        current_host = re.sub(r'\W+', "-", current_host)
        filename = f"{os.getcwd()}/.piwiPre.last.{current_host}"
        with open(filename, 'w', encoding='utf8') as f:
            f.write(f"{os.getcwd()}\n")
        self.msg(f"Saved last run location in {filename}")


class ThreadConfigurator:

    def __init__(self,
                 config: PwpConfig,
                 pwp_main,
                 logger,
                 worker,
                 test_scenario=None):
        self.worker = worker

        self.son = None
        self.configurator = PwpConfigurator(config=config, pwp_main=pwp_main,
                                            logger=logger, action=self.spawn_worker,
                                            test_scenario=test_scenario)
        pwp_main.configurator = self.configurator
        self.configurator.run_or_display()

    def spawn_worker(self):
        self.son = threading.Thread(target=self.run_worker, args=[], daemon=True)
        self.son.start()

    def run_worker(self):
        self.worker()
