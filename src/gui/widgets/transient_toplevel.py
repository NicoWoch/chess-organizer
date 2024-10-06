import logging
import tkinter as tk


logger = logging.getLogger(__name__)


class TransientToplevel(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.transient(parent)

        try:
            self.attributes('-toolwindow', True)
        except tk.TclError as e:
            logger.debug(f'(normal) TclError: {e}')

        try:
            self.attributes('-type', 'utility')
        except tk.TclError as e:
            logger.debug(f'(normal) TclError: {e}')
