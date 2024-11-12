static int __Pyx_VersionSanityCheck(void) {
  #if CYTHON_COMPILING_IN_CPYTHON
  #if PY_VERSION_HEX < 0x03080000
    if (PySys_GetObject("gettotalrefcount")) {
      #ifndef Py_DEBUG
        PyErr_SetString(
            PyExc_ImportError,
            "Module was compiled with a non-debug version of Python but imported into a debug version."
        );
        return -1;
      #endif
    } else {
      #ifdef Py_DEBUG
        PyErr_SetString(
            PyExc_ImportError,
            "Module was compiled with a debug version of Python but imported into a non-debug version."
        );
        return -1;
      #endif
    }
  #endif // Py_VERSION_HEX < 0x03080000
  #if PY_VERSION_HEX >= 0x030d0000
    if (PyRun_SimpleStringFlags(
      "if "
      #ifdef Py_GIL_DISABLED
        "not "
      #endif
      "__import__('sysconfig').get_config_var('Py_GIL_DISABLED'): raise ImportError",
      NULL
    ) == -1) {
        PyErr_SetString(
            PyExc_ImportError,
      #ifdef Py_GIL_DISABLED
            "Module was compiled with a freethreading build of Python but imported into a non-freethreading build."
      #else
            "Module was compiled with a non-freethreading build of Python but imported into a freethreading build."
      #endif
        );
      return -1;
    }
  #endif // version hex 3.13+
    if (PySys_GetObject("getobjects")) {
      #ifndef Py_TRACE_REFS
        PyErr_SetString(
            PyExc_ImportError,
            "Module was compiled without Py_TRACE_REFS but imported into a build of Python with."
        );
        return -1;
      #endif
    } else {
      #ifdef Py_TRACE_REFS
        PyErr_SetString(
            PyExc_ImportError,
            "Module was compiled with Py_TRACE_REFS but imported into a build of Python without."
        );
        return -1;
      #endif
    }
    const char code[] = "if __import__('sys').getsizeof(object()) != %u: raise ImportError";
    char formattedCode[sizeof(code)+50];
    PyOS_snprintf(formattedCode, sizeof(formattedCode), code, (unsigned int)sizeof(PyObject));
    if (PyRun_SimpleStringFlags(formattedCode, NULL) == -1) {
      PyErr_SetString(
        PyExc_ImportError,
        "Runtime and compile-time PyObject size do not match."
      );
      return -1;
    }
  #endif
    return 0;
}

