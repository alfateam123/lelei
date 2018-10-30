Lelei: XML -> WireShark Generic Dissector
=========================================

### Disclaimer ###
[![Build Status](https://travis-ci.org/alfateam123/lelei.svg?branch=master)](https://travis-ci.org/alfateam123/lelei)

### What is that? ###

Lelei is a [cute sorceress](http://gate-thus-the-jsdf-fought-there.wikia.com/wiki/Lelei_La_Lalena)... no, wait, nevermind.
Lelei is a [WireShark Generic Dissector](http://wsgd.free.fr/) generator: starting from an XML description of the structure you want to capture in Wireshark, it generates the `.fdesc` and `.wsgd` files you need to perform network analysis.

Please note that Lelei is not a validating generator: it means it may generate generic
dissectors that violate the WSGD grammar or context (using basic types incorrectly, 
passing wrong values to transform specifications, ...). If you have a problem,
please open an issue and we'll help you sorting it out.

### How to use ###

1. Define your packet structure in XML (see the _test_data_ folder for some examples)
2. Generate the generic dissectors: `lelei <packet_structure.xml> <output>`
3. Copy the resulting `output.fdesc` and `output.wsgd` to your Wireshark folders
4. Open Wireshark and analyze your net traffic!

### Yet another generator, I see... ###

I don't know if Wireshark offers the same functionality, or other programs that do
the same thing.
If you're interested in alternatives, you may use [Csjark](https://csjark.readthedocs.org/en/latest/),
which translates C structures to Lua-based dissectors.

### Important things: state of work ###

- Basic Types
  - [x] spare
  - [x] char, schar, uchar
  - [x] bool1, bool8, bool16, bool32
  - [x]  int2 ->  int32,  int40,  int48, int64
  - [x] uint1 -> uint32, uint40, uint48
  - [x] float32, float64
  - [x] string, string(size)
  - [x] string_nl, string_nl(size)
  - [x] raw(size)
  - [x] padding_bits [type = `padding`]

- [x] Struct
- [x] Local byte order spec
- [x] Enum
- [x] Arrays
- [x] Multiple structures support

I don't need this project at my day job anymore, so the rest of the
specification is probably not going to be implemented.
If you need something that is not implemented yet, please feel free to contribute
with a Pull Request via Github, or [contact me](https://wintermade.it).
