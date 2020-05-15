# Anvil Event Propogation
A client module for [Anvil Applications](https://anvil.works) that provides a mechanism
for propogating events between forms in a nested hierarchy.

## Installation
There are two methods to install this module within your own application:

### 1. As a Dependency

  * Create a clone of this application within your own Anvil account using this link:

    [<img src="https://anvil.works/img/forum/copy-app.png" height='40px'>](https://anvil.works/build#clone:VJKO42XKR64QGTTO=CGGP22MNKJPJMNEI6UAEYUBJ)
  
  * At anvil, open the app in which you'd like to include this module, from its settings menu, select 'Events',
    and select your new cloned app in the dropdown.

### 2. By Direct Inclusion

  * In your anvil application, create a new module in the client code section and name it 'events'
  * Copy the entire content of `client_code/events.py` from this repository into your 'events' module
  
## Usage

You can clone a demonstration of this module in use from:

[<img src="https://anvil.works/img/forum/copy-app.png" height='40px'>](https://anvil.works/build#clone:ES5LXZU5YFZ3OIG5=5LVSIJOAKYF5MYLZIER7H6QP)

This module provides a Manager class. Manager instances can then be used to register event
handlers on components, to raise registered events and, optionally, to propogate those
events to the parent and/or children of the component.

The module can also keep a register of manager instances which can be retrieved by name.
This allows manager objects to be passed between forms at different levels in a hierarchy (
rather than, for example, having to call `self.parent.parent.parent...`).

The events and handlers themselves are no different to ordinary anvil events and handlers.
The normal `set_event_handler` and `raise_event` methods can be used in conjunction with
this module and the same handler functions can be used to respond to both.

For events and handlers within the same form, this module offers no extra capability. Just
use anvil's ordinary mechanism.

Whilst it is possible to use this module to propogate events between entirely unrelated
forms, it is strongly suggested that you don't. The manager objects would hold references
to form methods even once those forms have been closed and thus prevent Python's garbage
collection from clearing those objects from memory. Unless you understand this and know
what you're doing, don't use this module in that fashion.

### Creating Managers and Registering events

Create an event manager by importing the module and instantiating the Manager class. e.g.
for a form named 'Demo':

```python
from ._anvil_designer import DemoTemplate
from Events import events

class Demo(DemoTemplate):
  def __init__(self, **properties):
    self.event_manager = events.Manager()
```

Register an event on that manager object:

```python
self.event_manager.register_handler("x-item-selected", self.repeating_panel_1, self.handle_item_selected)
```

### Passing Managers to Forms

To pass a manager object to another form, one option is to register in the events module.
e.g. in the form where the manager was created:

```python
events.register_manager(name="demo", event_manager=self.event_manager)
```

It can then be retrieved in a different form using:

```python
events.get_manager("demo")
```

The manager is an ordinary Python object, so it can also be passed to a form like any other.
e.g. You could use a tag to pass the form to a repeating panel and then retrieve it from
the panel's children.

In the parent form:

```python
self.repeating_panel_1.tag.event_manager = self.event_manager
```

and in the child:

```python
self.demo_event_manager = self.parent.tag.event_manager
```

### Raising Events

You can raise any of a manager's registered events with e.g.:

```python
event_manager.propogate_event("x-item-selected")
```

By default, this will raise the event on the registered component, its parent (if it has one)
and all its children. You can control the parent/child propogation by specifying the up/down
arguments. e.g. to propogate upwards only:

```python
event_manager.propogate_event("x-item-selected", down=False)
```

In the handler function, the usual sender key in the event_args dictionary will be the 
manager object. If you need the originating component itself, you can use the fact that
any additional keyword arguments are passed to the handler. e.g.:

```python
event_manager.propogate_event("x-item-selected", orginator=self)
```
