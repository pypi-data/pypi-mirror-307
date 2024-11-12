#ifndef __PYX_HAVE_RT_ImportFunction_3_1_0a1
#define __PYX_HAVE_RT_ImportFunction_3_1_0a1
static int __Pyx_ImportFunction_3_1_0a1(PyObject *module, const char *funcname, void (**f)(void), const char *sig) {
    PyObject *d = 0;
    PyObject *cobj = 0;
    d = PyObject_GetAttrString(module, "__pyx_capi__");
    if (!d)
        goto bad;
    cobj = PyDict_GetItemString(d, funcname);
    if (!cobj) {
        PyErr_Format(PyExc_ImportError,
            "%.200s does not export expected C function %.200s",
                PyModule_GetName(module), funcname);
        goto bad;
    }
    if (!PyCapsule_IsValid(cobj, sig)) {
        PyErr_Format(PyExc_TypeError,
            "C function %.200s.%.200s has wrong signature (expected %.500s, got %.500s)",
             PyModule_GetName(module), funcname, sig, PyCapsule_GetName(cobj));
        goto bad;
    }
    *f = __Pyx_capsule_to_c_func_ptr_3_1_0a1(cobj, sig);
    if (!(*f))
        goto bad;
    Py_DECREF(d);
    return 0;
bad:
    Py_XDECREF(d);
    return -1;
}
#endif

