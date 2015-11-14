## HSReplay

HSReplay is a replay format for [Hearthstone](http://playhearthstone.com/).

It is an XML-based format, with a structure closely mirroring that of the
game's protocol.

The extension for HSReplay files is `.hsreplay`.
The MIME Type is `application/vnd.hearthsim-hsreplay+xml`.


## Implementations

Two reference implementations are currently available: Python and C#.
They each contain capabilities for reading the `Power.log` files generated
by Hearthstone when logging is enabled.

For more information, see
[How to enable logging](https://github.com/jleclanche/fireplace/wiki/How-to-enable-logging).

If you are interested in developing reference implementations in other
languages, please get in touch through our `#hearthsim` channel (see below).


## Community

HSReplay is a [HearthSim](http://hearthsim.info) project. All development
happens on our IRC channel `#hearthsim` on [Freenode](https://freenode.net).


# License

The HSReplay specification (and the specification alone) is licensed
[CC0](https://creativecommons.org/publicdomain/zero/1.0/). That means it is
in the Public Domain, or as close to being in the Public Domain as possible
depending on the applicable laws. The full license text is available in
the `LICENSE` file.

The Python and C# implementations are licensed
[MIT](http://choosealicense.com/licenses/mit/). The full license text is
available in the `LICENSE` file in the respective implementations' folder.
