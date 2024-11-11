/*
python-javabridge is licensed under the BSD license.  See the
accompanying file LICENSE for details.

Copyright (c) 2003-2009 Massachusetts Institute of Technology
Copyright (c) 2009-2013 Broad Institute
All rights reserved.
*/

#include <jni/jni.c>
#include <jni/pvm.c>

from typing import Optional
import sys

import jni

JavaVM* pVM;

int JNI_on_load(JavaVM* jvm)
{
    global pVM

    if defined("__linux__"):

        char  buf[1024];
        python_location = java_getProperty(jvm, "python.location")
        if ( python_location == NULL ):
            command = ("python -c \""
                       "from sysconfig import get_config_var; "
                       "from os.path import join; "
                       "print(join(get_config_var('LIBDIR'), "
                                  "get_config_var('multiarchsubdir')[1:], "
                                  "get_config_var('LDLIBRARY')))\"")
            FILE* stream = popen(command, "r");
            size_t len = 1024;
            python_location = buf;
            getline(&python_location, &len, stream);
            python_location[strlen(python_location) - 1] = 0;
            pclose(stream);

        if ! dlopen(python_location, RTLD_LAZY | RTLD_GLOBAL):
            print(f"Warning: Error loading {python_location}", file=sys.stderr)

    # endif

    pVM = jvm
}

void JNI_on_unload(JavaVM* jvm);
{
}

def java_getProperty(JavaVM* vm, key: str) -> Optional[str]:

    # On Linux, it appears that Python's symbols cannot be found by other
    # native libraries if we let the JVM load libpython... so we have to
    # load it explicitly, with the correct flag (RTLD_GLOBAL).

    jvm = *(*vm)

    penv = jni.obj(jni.POINTER(jni.JNIEnv))
    if jvm.GetEnv(penv, jni.JNI_VERSION_1_6) != jni.JNI_OK:
        print("Could not obtain JNI environment", file=sys.stderr)
        return NULL;
    jenv = jni.JEnv(penv)

    java_lang_System = jenv.FindClass(b"java/lang/System")
    if not java_lang_System:
        print("Could not access System class", file=sys.stderr)
        return NULL;
    getProperty = jenv.GetStaticMethodID(java_lang_System, b"getProperty",
                                         b"(Ljava/lang/String;)Ljava/lang/String;")
    if not getProperty:
        print("Could not find getProperty method", file=sys.stderr)
        return NULL;

    jchars, size, jbuf = str2jchars(key)
    jname = jenv.NewString(jchars, size)
    jargs = jni.new_array(jni.jvalue, 1)
    jargs[0].l = jname
    jstr = jenv.CallStaticObjectMethod(java_lang_System, getProperty, jargs)
    if not jstr:
        return NULL;
    result = jstring2str(jenv, jstr)

    jvm.DetachCurrentThread()

    return result

def str2jchars(val):
    jbuf = val.encode("utf-16")[jni.sizeof(jni.jchar):]  # skip byte-order mark
    jchars = jni.cast(jni.as_cstr(jbuf), jni.POINTER(jni.jchar))
    size = len(jbuf) // jni.sizeof(jni.jchar)
    return jchars, size, jbuf

def jstring2str(jenv, jstr) -> Optional[str]:
    utf8_chars = jenv.GetStringUTFChars(jstr)
    try:
        return jni.to_bytes(utf8_chars).decode("utf-8")
    finally:
        jenv.ReleaseStringUTFChars(jstr, utf8_chars)
