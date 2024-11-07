# Copyright (C) 2013 Claudio "nex" Guarnieri (@botherder), Optiv, Inc. (brad.spengler@optiv.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from CAPEsolo.capelib.signatures import Signature


class NetworkBIND(Signature):
    name = "network_bind"
    description = "Starts servers listening on {0}"
    severity = 3
    categories = ["network"]
    authors = ["nex", "Optiv"]
    minimum = "1.0"
    evented = True
    mbcs = ["OB0004", "B0030"]
    mbcs += ["OC0006", "C0001"]  # micro-behaviour

    filter_apinames = set(["bind", "listen"])

    def __init__(self, *args, **kwargs):
        Signature.__init__(self, *args, **kwargs)
        self.binds = []
        self.bindmap = dict()
        self.listens = []

    def on_call(self, call, process):
        # this isn't entirely accurate since we're not tracking sockets properly
        if call["api"] == "bind":
            socket = self.get_argument(call, "socket")
            bind = "{0}:{1}".format(self.get_argument(call, "ip"), self.get_argument(call, "port"))
            self.bindmap[socket] = bind
            if self.pid:
                self.mark_call()
        elif call["api"] == "listen":
            socket = self.get_argument(call, "socket")
            if socket not in self.listens:
                self.listens.append(socket)
                if self.pid:
                    self.mark_call()

    def on_complete(self):
        for socket in self.listens:
            if socket in self.bindmap:
                if self.bindmap[socket] not in self.binds:
                    self.binds.append(self.bindmap[socket])

        if self.binds:
            self.description = self.description.format(", ".join(self.binds))
            return True
