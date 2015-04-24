# bt-sl4a-test

This is an example of using Bluetooth with QPython3 on Android 5.x

There were several changes between Android 4.x and 5.x, and a few between Python 2.x and 3.x and I was unable to find any guides that reflected them.

I suggest using QPython3 (Based on 3.2?) because it asks for all the permissions you need out of the box.

QPython (Based on android 2.7) requests no permissions, so you can't access anything until you recompile the APK with added permissions in the AndroidManifest.xml file.
See: https://shaneormonde.wordpress.com/2014/03/30/qpython-bluetooth-patch/

The older sl4a_r6.apk with PythonForAndroid_r4.apk don't really work any more on Android 5.x.
