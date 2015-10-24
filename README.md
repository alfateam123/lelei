Lelei: XML -> WireShark Generic Dissector
=========================================

### Disclaimer ###
PLEASE NOTE THAT THIS PROJECT IS NOT FULLY FUNCTIONAL, SO USE IT AT YOUR OWN RISK. CONSIDER IT TO BE INCOMPLET AND INKORRECT. YOU HAVE BEEN WARNED.

### What is that? ###

Lelei is a [cute sorceress](http://gate-thus-the-jsdf-fought-there.wikia.com/wiki/Lelei_La_Lalena)... no, wait, nevermind.
Lelei is an automatic WireShark Generic Dissector that, starting from an XML description,
generates the `.fdesc` and `.wsgd` files you need to perform network analysis

### How to use ###

1. Define your packet structure in XML
2. `lelei rory.xml`
3. Copy the resulting `rory.fdesc` and `rory.wsgd` to your Wireshark folders
4. Open Wireshark and analyze your net traffic!

### Yet another generator, I see... ###

I don't know if Wireshark offers the same functionality, or other programs that do
the same thing.
If you're interested in alternatives, you may use [Csjark](https://csjark.readthedocs.org/en/latest/),
which translates C structures to Lua-based dissectors.

### Important things: state of work ###

Does it write things yet? **No**.

How much of the grammar has been implemented?  
This is a list of the thing that will be implemented

- Basic Types
  - [x] spare
  - [x] char, schar, uchar
  - [x] bool1, bool8, bool16, bool32
  - [x]  int2 ->  int32,  int40,  int48, int64
  - [x] uint1 -> uint32, uint40, uint48
  - [x] float32, float64
  - [ ] string, string(size)
  - [ ] string_nl, string_nl(size)
  - [ ] raw(size)
  - [x] padding_bits [type = `padding`]

- [ ] No Statement value
- [ ] Transform spec
- [ ] Display spec
- [ ] Constraint spec
- [ ] Local byte order spec
- [ ] Enum
- [ ] Bit Fields

This is a list of things that will be implemented,
but not in the nearest future.

- [ ] Arrays
- [ ] Struct
- [ ] Switch
- [ ] Switch with expression

The rest of the specification may be not implemented, as it may
be difficult to express set/var commands and functions while staying
inside the XML structure, and Lelei is not a tool for that.