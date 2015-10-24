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