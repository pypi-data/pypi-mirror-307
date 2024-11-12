#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE PyObject* __Pyx_CallUnboundCMethod1(__Pyx_CachedCFunction* cfunc, PyObject* self, PyObject* arg) {
    if (likely(cfunc->func)) {
        int flag = cfunc->flag;
        if (flag == METH_O) {
            return (*(cfunc->func))(self, arg);
        } else if (flag == METH_FASTCALL) {
            return (*(__Pyx_PyCFunctionFast)(void*)(PyCFunction)cfunc->func)(self, &arg, 1);
        } else if (flag == (METH_FASTCALL | METH_KEYWORDS)) {
            return (*(__Pyx_PyCFunctionFastWithKeywords)(void*)(PyCFunction)cfunc->func)(self, &arg, 1, NULL);
        }
    }
    return __Pyx__CallUnboundCMethod1(cfunc, self, arg);
}
#endif
static PyObject* __Pyx__CallUnboundCMethod1(__Pyx_CachedCFunction* cfunc, PyObject* self, PyObject* arg){
    PyObject *result = NULL;
    if (unlikely(!cfunc->func && !cfunc->method) && unlikely(__Pyx_TryUnpackUnboundCMethod(cfunc) < 0)) return NULL;
#if CYTHON_COMPILING_IN_CPYTHON
    if (cfunc->func && (cfunc->flag & METH_VARARGS)) {
        PyObject *args = PyTuple_New(1);
        if (unlikely(!args)) return NULL;
        Py_INCREF(arg);
        PyTuple_SET_ITEM(args, 0, arg);
        if (cfunc->flag & METH_KEYWORDS)
            result = (*(PyCFunctionWithKeywords)(void*)(PyCFunction)cfunc->func)(self, args, NULL);
        else
            result = (*cfunc->func)(self, args);
        Py_DECREF(args);
    } else
#endif
    {
        result = __Pyx_PyObject_Call2Args(cfunc->method, self, arg);
    }
    return result;
}

