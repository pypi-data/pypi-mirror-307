static PyObject* __Pyx_Method_ClassMethod(PyObject *method) {
#if CYTHON_COMPILING_IN_PYPY && PYPY_VERSION_NUM <= 0x05080000
    if (PyObject_TypeCheck(method, &PyWrapperDescr_Type)) {
        return PyClassMethod_New(method);
    }
#else
#if CYTHON_COMPILING_IN_PYPY
    if (PyMethodDescr_Check(method))
#else
    if (__Pyx_TypeCheck(method, &PyMethodDescr_Type))
#endif
    {
#if CYTHON_COMPILING_IN_LIMITED_API
        return PyErr_Format(
            PyExc_SystemError,
            "Cython cannot yet handle classmethod on a MethodDescriptorType (%S) in limited API mode. "
            "This is most likely a classmethod in a cdef class method with binding=False. "
            "Try setting 'binding' to True.",
            method);
#elif CYTHON_COMPILING_IN_GRAAL
        PyTypeObject *d_type = PyDescrObject_GetType(method);
        return PyDescr_NewClassMethod(d_type, PyMethodDescrObject_GetMethod(method));
#else
        PyMethodDescrObject *descr = (PyMethodDescrObject *)method;
        PyTypeObject *d_type = descr->d_common.d_type;
        return PyDescr_NewClassMethod(d_type, descr->d_method);
#endif
    }
#endif
#if !CYTHON_COMPILING_IN_LIMITED_API
    else if (PyMethod_Check(method)) {
        return PyClassMethod_New(PyMethod_GET_FUNCTION(method));
    }
    else {
        return PyClassMethod_New(method);
    }
#else
    {
        PyObject *types_module, *method_type=NULL, *func=NULL;
        PyObject *builtins, *classmethod, *result=NULL;
        types_module = PyImport_ImportModule("types");
        if (!types_module) {
            return NULL;
        }
        method_type = PyObject_GetAttrString(types_module, "MethodType");
        if (!method_type) goto bad;
        if (__Pyx_TypeCheck(method, method_type)) {
            func = PyObject_GetAttrString(method, "__func__");
            if (!func) goto bad;
        } else {
            func = method;
            Py_INCREF(func);
        }
        builtins = PyEval_GetBuiltins(); // borrowed
        if (!builtins) goto bad;
        classmethod = PyDict_GetItemString(builtins, "classmethod");
        if (!classmethod) goto bad;
        result = PyObject_CallFunctionObjArgs(classmethod, func, NULL);
        bad:
        Py_XDECREF(func);
        Py_XDECREF(method_type);
        Py_DECREF(types_module);
        return result;
    }
#endif
}

