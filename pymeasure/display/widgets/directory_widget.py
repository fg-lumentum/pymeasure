#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2025 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging

from ..Qt import QtCore, QtGui, QtWidgets

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class DirectoryLineEdit(QtWidgets.QLineEdit):
    """
    Widget that allows to choose a directory path.
    A completer is implemented for quick completion.
    A browse button is available.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        completer = QtWidgets.QCompleter(self)
        completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)

        model = QtGui.QFileSystemModel(completer)
        model.setRootPath(model.myComputer())
        model.setFilter(QtCore.QDir.Filter.Dirs |
                        QtCore.QDir.Filter.Drives |
                        QtCore.QDir.Filter.NoDotAndDotDot |
                        QtCore.QDir.Filter.AllDirs)
        completer.setModel(model)

        self.setCompleter(completer)

        browse_action = QtGui.QAction(self)
        browse_action.setIcon(self.style().standardIcon(
            getattr(QtWidgets.QStyle.StandardPixmap, 'SP_DialogOpenButton')))
        browse_action.triggered.connect(self.browse_triggered)

        self.addAction(browse_action, QtWidgets.QLineEdit.ActionPosition.TrailingPosition)

    def _get_starting_directory(self):
        current_text = self.text()
        if current_text != '' and QtCore.QDir(current_text).exists():
            return current_text

        else:
            return '/'

    def browse_triggered(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Directory', self._get_starting_directory())
        if path != '':
            self.setText(path)
