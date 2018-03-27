# Google breakpad `dump_syms` python server

This server dump the [symbols](https://github.com/google/breakpad/blob/master/docs/getting_started_with_breakpad.md) for your native libraries, you can read [here](https://github.com/google/breakpad/blob/master/docs/getting_started_with_breakpad.md) how google breakpad works.<br/>

Just send a ziped folder(you can include multiple ABIs - server look recurcively for `.so` files) with `.so` files or a single `.so` file as form data.

### Why?
`dump_syms` works only on Linux 😐, so you can easily run ./build_and_run_docker.sh script which builds & runs docker with a server, take a look at [Docker](#docker) section.

### Dependencies
* [Google breakpad(`dump_syms`)](https://chromium.googlesource.com/breakpad/breakpad)
* Python2

*Note: google breakpad `dump_syms` works only on Linux*


### Docker
This repo contains `Dockerfile` inside docker folder, so you need just run `./build_and_run_docker.sh` script which builds a container && start the container with server on **port 4000**

```
>> ./build_and_run_docker.sh

Building docker...
Sending build context to Docker daemon   2.56kB
Step 1/9 : FROM ubuntu
 ---> f975c5035748
...
Successfully built f7b3aaecb0cd
Successfully tagged crashserver:latest
Starting server on port 4000
```

### Usage

```
# Start a server
> python server.py 8003
Started httpserver on port  8003

# Browse a zipped structure
> unzip -l jniLibs.zip
Archive:  jniLibs.zip
 unzip -l jniLibs.zip
Archive:  jniLibs.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  03-26-2018 16:59   jniLibs/
        0  03-26-2018 12:46   jniLibs/armeabi-v7a/
 14166556  03-26-2018 15:10   jniLibs/armeabi-v7a/libFoundation.so
    25664  03-26-2018 15:10   jniLibs/armeabi-v7a/libswiftGlibc.so
  2045828  03-26-2018 15:10   jniLibs/armeabi-v7a/libscui18n.so
  1418788  03-26-2018 15:10   jniLibs/armeabi-v7a/libscuuc.so
     6148  03-26-2018 12:47   jniLibs/armeabi-v7a/.DS_Store
   949372  03-26-2018 15:10   jniLibs/armeabi-v7a/libdispatch.so
 25911876  03-26-2018 15:10   jniLibs/armeabi-v7a/libscudata.so
   501716  03-26-2018 15:10   jniLibs/armeabi-v7a/libXCTest.so
  8896748  03-26-2018 15:10   jniLibs/armeabi-v7a/libswiftCore.so
  3983508  03-26-2018 15:10   jniLibs/armeabi-v7a/libSampleAppCore.so
   683776  03-26-2018 15:10   jniLibs/armeabi-v7a/libswiftSwiftOnoneSupport.so
   132636  03-26-2018 15:10   jniLibs/armeabi-v7a/libbreakpad.so
  2294932  03-26-2018 15:10   jniLibs/armeabi-v7a/libxml2.so
   661056  03-26-2018 15:10   jniLibs/armeabi-v7a/libc++_shared.so
  2321548  03-26-2018 15:10   jniLibs/armeabi-v7a/libcurl.so
        0  03-26-2018 12:46   jniLibs/x86/
 14166556  03-26-2018 15:10   jniLibs/x86/libFoundation.so
    25664  03-26-2018 15:10   jniLibs/x86/libswiftGlibc.so
  2045828  03-26-2018 15:10   jniLibs/x86/libscui18n.so
  1418788  03-26-2018 15:10   jniLibs/x86/libscuuc.so
   949372  03-26-2018 15:10   jniLibs/x86/libdispatch.so
 25911876  03-26-2018 15:10   jniLibs/x86/libscudata.so
   501716  03-26-2018 15:10   jniLibs/x86/libXCTest.so
  8896748  03-26-2018 15:10   jniLibs/x86/libswiftCore.so
  3983508  03-26-2018 15:10   jniLibs/x86/libSampleAppCore.so
   683776  03-26-2018 15:10   jniLibs/x86/libswiftSwiftOnoneSupport.so
   132636  03-26-2018 15:10   jniLibs/x86/libbreakpad.so
  2294932  03-26-2018 15:10   jniLibs/x86/libxml2.so
   661056  03-26-2018 15:10   jniLibs/x86/libc++_shared.so
  2321548  03-26-2018 15:10   jniLibs/x86/libcurl.so

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




