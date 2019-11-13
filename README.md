# python-hsreplay

[![Build Status](https://travis-ci.com/HearthSim/python-hsreplay.svg?branch=master)](https://travis-ci.com/HearthSim/python-hsreplay)
[![PyPI](https://img.shields.io/pypi/v/hsreplay.svg)](https://pypi.org/project/hsreplay/)

A python module for HSReplay support.

<https://hearthsim.info/hsreplay/>


## Installation

The library is available on PyPI. `pip install hsreplay` will install it.

Dependencies:

* [`hearthstone`](https://github.com/HearthSim/python-hearthstone)
* [`hslog`](https://github.com/HearthSim/python-hslog)
* `lxml` (optional) for faster XML parsing and writing. Will use `xml.etree` if not available.
* `aniso8601` or `dateutil` for timestamp parsing


## Usage

The main document class is `hsreplay.document.HSReplayDocument`.
That class contains all the necessary functionality to import and export HSReplay files.


### Reading/Writing HSReplay XML files

The classmethod `from_xml_file(fp)` takes a file-like object and will return a document.
If you already have an `ElementTree` object, you can call the `from_xml(xml)` classmethod instead.

To export to an HSReplay XML document, the `HSReplayDocument.toxml(pretty=False)` method can be
used to obtain a UTF8-encoded string containing the document.


### Reading directly from a log file

The library integrates directly with the `python-hearthstone` library to produce `HSReplayDocument`
objects directly from a log file or a parser instance.

Use the helper classmethods `from_log_file(fp, processor="GameState", date=None, build=None)` and
`from_parser(parser, build=None)`, respectively.


### Exporting back to a PacketTree

It is possible to export HSReplayDocument objects back into a PacketTree with the `to_packet_tree()`
method. This therefore allows lossless conversion from a PacketTree, into HSReplayDocument, then
back into a PacketTree.

This is especially interesting because of the native functionality in `python-hearthstone` which is
able to export to a Game tree and allows exploring the game state. By converting HSReplayDocument
objects to a PacketTree, it's very easy to follow the replay at a gameplay level, explore the state
of the various entities and even hook into the exporter in order to programmatically analyze it.
