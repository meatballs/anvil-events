#    Anvil Event Management
#    Copyright 2020 Owen Campbell
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#   This program is published at https://github.com/meatballs/anvil-events
_event_managers = {}

class Manager:
    """A class to handle events on components"""  
    
    def __init__(self):
        self.events = {}
        
    def register_handler(self, event, component, handler):
        """Regsiter the handler function for a given event on a given component"""
        if event not in self.events:
            self.events[event] = []
        self.events[event].append(component)
        component.set_event_handler(event, handler)
      
    def propogate_event(self, event, up=True, down=True, **kwargs):
        """Raise a given event on all components for which it has been registered"""
        for component in self.events[event]:
            component.raise_event(event, **kwargs)
            if up and component.parent is not None:
                component.parent.raise_event(event, **kwargs)
            if down:
                component.raise_event_on_children(event, **kwargs)

            
def register_manager(name, event_manager):
    _event_managers[name] = event_manager
    

def get_manager(name):
    return _event_managers[name]