# -*- coding: utf-8 -*-

VERSION = "0.1"

from gi.repository import Gtk, Gedit, GObject, Gdk

class TabPgUpPgDownPlugin(GObject.Object, Gedit.WindowActivatable):
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self.id_name = 'FocusBottomPanePluginID'
 
    def do_activate(self):
        l_ids = []
        # Signals to attach to - Only key-press-event
        # at the moment.
        for signal in ('key-press-event',):
            method = getattr(self, 'on_window_' + signal.replace('-', '_'))
            l_ids.append(self.window.connect(signal, method))
        self.window.set_data(self.id_name, l_ids)

    def do_deactivate(self):
        l_ids = self.window.get_data(self.id_name)

        for l_id in l_ids:
            self.window.disconnect(l_id)

    def on_window_key_press_event(self, window, event):
        key = Gdk.keyval_name(event.keyval)
        if event.state & Gdk.ModifierType.CONTROL_MASK and key in ('Tab', 'ISO_Left_Tab'):
           active_view = window.get_active_view()
           if active_view.has_focus():
                window.get_bottom_panel().grab_focus()
           else:
                active_view.grab_focus()

           return True
