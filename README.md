# Google breakpad `dump_syms` python server

This server dump the [symbols](https://github.com/google/breakpad/blob/master/docs/getting_started_with_breakpad.md) for your native libraries, you can read [here](https://github.com/google/breakpad/blob/master/docs/getting_started_with_breakpad.md) how google breakpad works.<br/>

Just send a ziped folder with `.so` files or single `.so` file as form data.

### Usage

```
# Start a server
> python server.py 8003
Started httpserver on port  8003

# Browse a zipped structure
> unzip -l libs.zip
Archive:  libs.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
 14166556  03-23-2018 19:44   libFoundation.so
    25664  03-23-2018 19:44   libswiftGlibc.so
  2045828  03-23-2018 19:44   libscui18n.so
  1418788  03-23-2018 19:44   libscuuc.so
   949372  03-23-2018 19:44   libdispatch.so
 25911876  03-23-2018 19:44   libscudata.so
   501716  03-23-2018 19:44   libXCTest.so
  8896748  03-23-2018 19:44   libswiftCore.so
  3982184  03-23-2018 19:44   libSampleAppCore.so
   683776  03-23-2018 19:44   libswiftSwiftOnoneSupport.so
   132636  03-23-2018 19:44   libbreakpad.so
  2294932  03-23-2018 19:44   libxml2.so
   661056  03-23-2018 19:44   libc++_shared.so
  2321548  03-23-2018 19:44   libcurl.so
---------                     -------
 63992680                     14 files

# Send libs
> curl --form file=@libs.zip http://localhost:8001/dump_syms -o symbols.zip

# Browse result
> unzip -l symbols.zip
Archive:  symbols.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
   185049  03-26-2018 10:19   symbols/libswiftSwiftOnoneSupport.so/92F5363BC1E6D6D044F82EDE14811DD20/libswiftSwiftOnoneSupport.so.sym
  2052099  03-26-2018 10:19   symbols/libFoundation.so/57D9582878DC08D5992E51407B7954F20/libFoundation.so.sym
  2011646  03-26-2018 10:19   symbols/libswiftCore.so/5C2A2448F04AA9D69DF6CB2DDC6CDB420/libswiftCore.so.sym
    85843  03-26-2018 10:19   symbols/libXCTest.so/0FAA4F99F240783EA0192E56074B82F50/libXCTest.so.sym
   411972  03-26-2018 10:19   symbols/libscui18n.so/2ABAB3F595A6E38E88BAF23A977671E90/libscui18n.so.sym
  2285911  03-26-2018 10:19   symbols/libSampleAppCore.so/1D2C2CF442340B1048DFB40CCA89840C0/libSampleAppCore.so.sym
   175365  03-26-2018 10:19   symbols/libc++_shared.so/64030F2C2390EB4BF1F8A1B8B39520DF0/libc++_shared.so.sym
     5291  03-26-2018 10:19   symbols/libswiftGlibc.so/0C443D297541033BF29F320004543A050/libswiftGlibc.so.sym
   203946  03-26-2018 10:19   symbols/libcurl.so/C64871F3D18B2C0E9F53C57DD086EB370/libcurl.so.sym
   156721  03-26-2018 10:19   symbols/libscuuc.so/FC3FAD67F7199BD738D27B03669D08B70/libscuuc.so.sym
   164316  03-26-2018 10:19   symbols/libdispatch.so/0C9FC1DF741FFA3114F3061342AA37E50/libdispatch.so.sym
    18196  03-26-2018 10:19   symbols/libbreakpad.so/644BE00C6993386888558317B260518C0/libbreakpad.so.sym
   152364  03-26-2018 10:19   symbols/libxml2.so/FEA6CC63F333D9EDAF6168BE4B2230080/libxml2.so.sym
---------                     -------
```



### Dependencies
* [Google breakpad(`dump_syms`)](https://chromium.googlesource.com/breakpad/breakpad)
* Python2

*Note: google breakpad `dump_syms` works only on Linux*
