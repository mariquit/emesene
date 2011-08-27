# -*- coding: utf-8 -*-

#    This file is part of emesene.
#
#    emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    emesene is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#    module created by Andrea Stagi stagi.andrea(at)gmail.com
#

from Github import Github
import os

class ExtensionDescriptor(object):

    def __init__(self):
        self.files = {}
        self.todownload = False

    def add_file(self, file_name, blob):
        self.files[file_name] = blob

class Collection(object):

    def __init__(self, theme, dest_folder):
        self.dest_folder = dest_folder
        self.extensions_descs = {}
        self.theme = theme
        self.github = Github("emesene")
    
    def download(self):
        for key in self.extensions_descs:
            element = self.extensions_descs[key]
            for label in element:
                if element[label].todownload:
                    for el, k in element[label].files.items():
                        els = el.split("/")
                        path_to_create = ""
                        for i in range(len(els) - 1):
                            path_to_create = os.path.join(path_to_create, els[i])
                        try:
                            os.makedirs(os.path.join(self.dest_folder , path_to_create))
                        except OSError:
                            pass
                        rq = self.github.get_raw(self.theme, k)
                        f = open(os.path.join(self.dest_folder, el), "wb")
                        f.write(rq)

    def plugin_name_from_file(self, file_name):
        pass


    def fetch(self):
        pass

class PluginsCollection(Collection):

    def plugin_name_from_file(self, file_name):
        ps = file_name.find( "/")

        if ps != -1:
            return file_name[:ps]
        else:
            return ps


    def fetch(self):

        j = self.github.fetch_blob(self.theme)
        type = "plugin"

        for k in j["blobs"]:

            plugin = self.plugin_name_from_file(k)

            if plugin == -1:
                continue

            try:
                extype = self.extensions_descs[type]
            except KeyError:
                extype = self.extensions_descs[type] = {}

            try:
                pl = extype[plugin]
            except KeyError:
                pl = extype[plugin] = ExtensionDescriptor()

            pl.add_file(k, j["blobs"][k])


class ThemesCollection(Collection):

    def plugin_name_from_file(self, file_name):

        ps = file_name.find( "/")
        ps = file_name.find( "/", ps + 1)

        if ps != -1:
            return file_name[:ps]
        else:
            return ps


    def fetch(self):

        j = self.github.fetch_blob(self.theme)

        for k in j["blobs"]:

            plugin = self.plugin_name_from_file(k)

            if plugin == -1:
                continue

            (type, name) = plugin.split("/")

            try:
                extype = self.extensions_descs[type]
            except KeyError:
                extype = self.extensions_descs[type] = {}

            try:
                pl = extype[name]
            except KeyError:
                pl = extype[name] = ExtensionDescriptor()

            pl.add_file(k, j["blobs"][k])

