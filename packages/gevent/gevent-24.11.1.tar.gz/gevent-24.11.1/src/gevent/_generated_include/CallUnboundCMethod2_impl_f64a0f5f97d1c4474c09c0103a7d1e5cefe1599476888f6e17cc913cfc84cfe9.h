#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject *__Pyx_CallUnboundCMethod2(__Pyx_CachedCFunction *cfunc, PyObject *self, PyObject *arg1, PyObject *arg2) {
    if (likely(cfunc->func)) {
        PyObject *args[2] = {arg1, arg2};
        if (cfunc->flag == METH_FASTCALL) {
            return (*(__Pyx_PyCFunctionFast)(void*)(PyCFunction)cfunc->func)(self, args, 2);
        }
        if (cfunc->flag == (METH_FASTCALL | METH_KEYWORDS))
            return (*(__Pyx_PyCFunctionFastWithKeywords)(void*)(PyCFunction)cfunc->func)(self, args, 2, NULL);
    }
    return __Pyx__CallUnboundCMethod2(cfunc, self, arg1, arg2);
}
#endif
static PyObject* __Pyx__CallUnboundCMethod2(__Pyx_CachedCFunction* cfunc, PyObject* self, PyObject* arg1, PyObject* arg2){
    PyObject *result = NULL;
    if (unlikely(!cfunc->func && !cfunc->method) && unlikely(__Pyx_TryUnpackUnboundCMethod(cfunc) < 0)) return NULL;
#if CYTHON_COMPILING_IN_CPYTHON
    if (cfunc->func && (cfunc->flag & METH_VARARGS)) {
        PyObject *args = PyTuple_New(2);
        if (unlikely(!args)) return NULL;
        Py_INCREF(arg1);
        PyTuple_SET_ITEM(args, 0, arg1);
        Py_INCREF(arg2);
        PyTuple_SET_ITEM(args, 1, arg2);
        if (cfunc->flag & METH_KEYWORDS)
            result = (*(PyCFunctionWithKeywords)(void*)(PyCFunction)cfunc->func)(self, args, NULL);
        else
            result = (*cfunc->func)(self, args);
        Py_DECREF(args);
        return result;
    }
#endif
    {
        PyObject *args[4] = {NULL, self, arg1, arg2};
        return __Pyx_PyObject_FastCall(cfunc->method, args+1, 3 | __Pyx_PY_VECTORCALL_ARGUMENTS_OFFSET);
    }
}

