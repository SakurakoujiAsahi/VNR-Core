
// default includes
#include <shiboken.h>
#include <typeresolver.h>
#include <typeinfo>
#include "pypinyin_python.h"

#include "pinyinconverter_wrapper.h"

// Extra includes
#include <pinyinconv.h>



// Target ---------------------------------------------------------

extern "C" {
static int
Sbk_PinyinConverter_Init(PyObject* self, PyObject* args, PyObject* kwds)
{
    SbkObject* sbkSelf = reinterpret_cast<SbkObject*>(self);
    if (Shiboken::Object::isUserType(self) && !Shiboken::ObjectType::canCallConstructor(self->ob_type, Shiboken::SbkType< ::PinyinConverter >()))
        return -1;

    ::PinyinConverter* cptr = 0;

    // Call function/method
    {

        if (!PyErr_Occurred()) {
            // PinyinConverter()
            PyThreadState* _save = PyEval_SaveThread(); // Py_BEGIN_ALLOW_THREADS
            cptr = new ::PinyinConverter();
            PyEval_RestoreThread(_save); // Py_END_ALLOW_THREADS
        }
    }

    if (PyErr_Occurred() || !Shiboken::Object::setCppPointer(sbkSelf, Shiboken::SbkType< ::PinyinConverter >(), cptr)) {
        delete cptr;
        return -1;
    }
    Shiboken::Object::setValidCpp(sbkSelf, true);
    Shiboken::BindingManager::instance().registerWrapper(sbkSelf, cptr);


    return 1;
}

static PyObject* Sbk_PinyinConverterFunc_addFile(PyObject* self, PyObject* pyArg)
{
    ::PinyinConverter* cppSelf = 0;
    SBK_UNUSED(cppSelf)
    if (!Shiboken::Object::isValid(self))
        return 0;
    cppSelf = ((::PinyinConverter*)Shiboken::Conversions::cppPointer(SbkpypinyinTypes[SBK_PINYINCONVERTER_IDX], (SbkObject*)self));
    PyObject* pyResult = 0;
    int overloadId = -1;
    PythonToCppFunc pythonToCpp;
    SBK_UNUSED(pythonToCpp)

    // Overloaded function decisor
    // 0: addFile(std::wstring)
    if ((pythonToCpp = Shiboken::Conversions::isPythonToCppConvertible(SbkpypinyinTypeConverters[SBK_STD_WSTRING_IDX], (pyArg)))) {
        overloadId = 0; // addFile(std::wstring)
    }

    // Function signature not found.
    if (overloadId == -1) goto Sbk_PinyinConverterFunc_addFile_TypeError;

    // Call function/method
    {
        ::std::wstring cppArg0 = ::std::wstring();
        pythonToCpp(pyArg, &cppArg0);

        if (!PyErr_Occurred()) {
            // addFile(std::wstring)
            PyThreadState* _save = PyEval_SaveThread(); // Py_BEGIN_ALLOW_THREADS
            bool cppResult = cppSelf->addFile(cppArg0);
            PyEval_RestoreThread(_save); // Py_END_ALLOW_THREADS
            pyResult = Shiboken::Conversions::copyToPython(Shiboken::Conversions::PrimitiveTypeConverter<bool>(), &cppResult);
        }
    }

    if (PyErr_Occurred() || !pyResult) {
        Py_XDECREF(pyResult);
        return 0;
    }
    return pyResult;

    Sbk_PinyinConverterFunc_addFile_TypeError:
        const char* overloads[] = {"std::wstring", 0};
        Shiboken::setErrorAboutWrongArguments(pyArg, "pypinyin.PinyinConverter.addFile", overloads);
        return 0;
}

static PyObject* Sbk_PinyinConverterFunc_clear(PyObject* self)
{
    ::PinyinConverter* cppSelf = 0;
    SBK_UNUSED(cppSelf)
    if (!Shiboken::Object::isValid(self))
        return 0;
    cppSelf = ((::PinyinConverter*)Shiboken::Conversions::cppPointer(SbkpypinyinTypes[SBK_PINYINCONVERTER_IDX], (SbkObject*)self));

    // Call function/method
    {

        if (!PyErr_Occurred()) {
            // clear()
            PyThreadState* _save = PyEval_SaveThread(); // Py_BEGIN_ALLOW_THREADS
            cppSelf->clear();
            PyEval_RestoreThread(_save); // Py_END_ALLOW_THREADS
        }
    }

    if (PyErr_Occurred()) {
        return 0;
    }
    Py_RETURN_NONE;
}

static PyObject* Sbk_PinyinConverterFunc_convert(PyObject* self, PyObject* args, PyObject* kwds)
{
    ::PinyinConverter* cppSelf = 0;
    SBK_UNUSED(cppSelf)
    if (!Shiboken::Object::isValid(self))
        return 0;
    cppSelf = ((::PinyinConverter*)Shiboken::Conversions::cppPointer(SbkpypinyinTypes[SBK_PINYINCONVERTER_IDX], (SbkObject*)self));
    PyObject* pyResult = 0;
    int overloadId = -1;
    PythonToCppFunc pythonToCpp[] = { 0, 0, 0, 0 };
    SBK_UNUSED(pythonToCpp)
    int numNamedArgs = (kwds ? PyDict_Size(kwds) : 0);
    int numArgs = PyTuple_GET_SIZE(args);
    PyObject* pyArgs[] = {0, 0, 0, 0};

    // invalid argument lengths
    if (numArgs + numNamedArgs > 4) {
        PyErr_SetString(PyExc_TypeError, "pypinyin.PinyinConverter.convert(): too many arguments");
        return 0;
    } else if (numArgs < 1) {
        PyErr_SetString(PyExc_TypeError, "pypinyin.PinyinConverter.convert(): not enough arguments");
        return 0;
    }

    if (!PyArg_ParseTuple(args, "|OOOO:convert", &(pyArgs[0]), &(pyArgs[1]), &(pyArgs[2]), &(pyArgs[3])))
        return 0;


    // Overloaded function decisor
    // 0: convert(std::wstring,std::wstring,bool,bool)const
    if ((pythonToCpp[0] = Shiboken::Conversions::isPythonToCppConvertible(SbkpypinyinTypeConverters[SBK_STD_WSTRING_IDX], (pyArgs[0])))) {
        if (numArgs == 1) {
            overloadId = 0; // convert(std::wstring,std::wstring,bool,bool)const
        } else if ((pythonToCpp[1] = Shiboken::Conversions::isPythonToCppConvertible(SbkpypinyinTypeConverters[SBK_STD_WSTRING_IDX], (pyArgs[1])))) {
            if (numArgs == 2) {
                overloadId = 0; // convert(std::wstring,std::wstring,bool,bool)const
            } else if ((pythonToCpp[2] = Shiboken::Conversions::isPythonToCppConvertible(Shiboken::Conversions::PrimitiveTypeConverter<bool>(), (pyArgs[2])))) {
                if (numArgs == 3) {
                    overloadId = 0; // convert(std::wstring,std::wstring,bool,bool)const
                } else if ((pythonToCpp[3] = Shiboken::Conversions::isPythonToCppConvertible(Shiboken::Conversions::PrimitiveTypeConverter<bool>(), (pyArgs[3])))) {
                    overloadId = 0; // convert(std::wstring,std::wstring,bool,bool)const
                }
            }
        }
    }

    // Function signature not found.
    if (overloadId == -1) goto Sbk_PinyinConverterFunc_convert_TypeError;

    // Call function/method
    {
        if (kwds) {
            PyObject* value = PyDict_GetItemString(kwds, "delim");
            if (value && pyArgs[1]) {
                PyErr_SetString(PyExc_TypeError, "pypinyin.PinyinConverter.convert(): got multiple values for keyword argument 'delim'.");
                return 0;
            } else if (value) {
                pyArgs[1] = value;
                if (!(pythonToCpp[1] = Shiboken::Conversions::isPythonToCppConvertible(SbkpypinyinTypeConverters[SBK_STD_WSTRING_IDX], (pyArgs[1]))))
                    goto Sbk_PinyinConverterFunc_convert_TypeError;
            }
            value = PyDict_GetItemString(kwds, "tone");
            if (value && pyArgs[2]) {
                PyErr_SetString(PyExc_TypeError, "pypinyin.PinyinConverter.convert(): got multiple values for keyword argument 'tone'.");
                return 0;
            } else if (value) {
                pyArgs[2] = value;
                if (!(pythonToCpp[2] = Shiboken::Conversions::isPythonToCppConvertible(Shiboken::Conversions::PrimitiveTypeConverter<bool>(), (pyArgs[2]))))
                    goto Sbk_PinyinConverterFunc_convert_TypeError;
            }
            value = PyDict_GetItemString(kwds, "capital");
            if (value && pyArgs[3]) {
                PyErr_SetString(PyExc_TypeError, "pypinyin.PinyinConverter.convert(): got multiple values for keyword argument 'capital'.");
                return 0;
            } else if (value) {
                pyArgs[3] = value;
                if (!(pythonToCpp[3] = Shiboken::Conversions::isPythonToCppConvertible(Shiboken::Conversions::PrimitiveTypeConverter<bool>(), (pyArgs[3]))))
                    goto Sbk_PinyinConverterFunc_convert_TypeError;
            }
        }
        ::std::wstring cppArg0 = ::std::wstring();
        pythonToCpp[0](pyArgs[0], &cppArg0);
        ::std::wstring cppArg1 = L" ";
        if (pythonToCpp[1]) pythonToCpp[1](pyArgs[1], &cppArg1);
        bool cppArg2 = true;
        if (pythonToCpp[2]) pythonToCpp[2](pyArgs[2], &cppArg2);
        bool cppArg3 = true;
        if (pythonToCpp[3]) pythonToCpp[3](pyArgs[3], &cppArg3);

        if (!PyErr_Occurred()) {
            // convert(std::wstring,std::wstring,bool,bool)const
            PyThreadState* _save = PyEval_SaveThread(); // Py_BEGIN_ALLOW_THREADS
            std::wstring cppResult = const_cast<const ::PinyinConverter*>(cppSelf)->convert(cppArg0, cppArg1, cppArg2, cppArg3);
            PyEval_RestoreThread(_save); // Py_END_ALLOW_THREADS
            pyResult = Shiboken::Conversions::copyToPython(SbkpypinyinTypeConverters[SBK_STD_WSTRING_IDX], &cppResult);
        }
    }

    if (PyErr_Occurred() || !pyResult) {
        Py_XDECREF(pyResult);
        return 0;
    }
    return pyResult;

    Sbk_PinyinConverterFunc_convert_TypeError:
        const char* overloads[] = {"std::wstring, std::wstring = L\" \", bool = true, bool = true", 0};
        Shiboken::setErrorAboutWrongArguments(args, "pypinyin.PinyinConverter.convert", overloads);
        return 0;
}

static PyObject* Sbk_PinyinConverterFunc_isEmpty(PyObject* self)
{
    ::PinyinConverter* cppSelf = 0;
    SBK_UNUSED(cppSelf)
    if (!Shiboken::Object::isValid(self))
        return 0;
    cppSelf = ((::PinyinConverter*)Shiboken::Conversions::cppPointer(SbkpypinyinTypes[SBK_PINYINCONVERTER_IDX], (SbkObject*)self));
    PyObject* pyResult = 0;

    // Call function/method
    {

        if (!PyErr_Occurred()) {
            // isEmpty()const
            PyThreadState* _save = PyEval_SaveThread(); // Py_BEGIN_ALLOW_THREADS
            bool cppResult = const_cast<const ::PinyinConverter*>(cppSelf)->isEmpty();
            PyEval_RestoreThread(_save); // Py_END_ALLOW_THREADS
            pyResult = Shiboken::Conversions::copyToPython(Shiboken::Conversions::PrimitiveTypeConverter<bool>(), &cppResult);
        }
    }

    if (PyErr_Occurred() || !pyResult) {
        Py_XDECREF(pyResult);
        return 0;
    }
    return pyResult;
}

static PyObject* Sbk_PinyinConverterFunc_size(PyObject* self)
{
    ::PinyinConverter* cppSelf = 0;
    SBK_UNUSED(cppSelf)
    if (!Shiboken::Object::isValid(self))
        return 0;
    cppSelf = ((::PinyinConverter*)Shiboken::Conversions::cppPointer(SbkpypinyinTypes[SBK_PINYINCONVERTER_IDX], (SbkObject*)self));
    PyObject* pyResult = 0;

    // Call function/method
    {

        if (!PyErr_Occurred()) {
            // size()const
            PyThreadState* _save = PyEval_SaveThread(); // Py_BEGIN_ALLOW_THREADS
            int cppResult = const_cast<const ::PinyinConverter*>(cppSelf)->size();
            PyEval_RestoreThread(_save); // Py_END_ALLOW_THREADS
            pyResult = Shiboken::Conversions::copyToPython(Shiboken::Conversions::PrimitiveTypeConverter<int>(), &cppResult);
        }
    }

    if (PyErr_Occurred() || !pyResult) {
        Py_XDECREF(pyResult);
        return 0;
    }
    return pyResult;
}

static PyMethodDef Sbk_PinyinConverter_methods[] = {
    {"addFile", (PyCFunction)Sbk_PinyinConverterFunc_addFile, METH_O},
    {"clear", (PyCFunction)Sbk_PinyinConverterFunc_clear, METH_NOARGS},
    {"convert", (PyCFunction)Sbk_PinyinConverterFunc_convert, METH_VARARGS|METH_KEYWORDS},
    {"isEmpty", (PyCFunction)Sbk_PinyinConverterFunc_isEmpty, METH_NOARGS},
    {"size", (PyCFunction)Sbk_PinyinConverterFunc_size, METH_NOARGS},

    {0} // Sentinel
};

} // extern "C"

static int Sbk_PinyinConverter_traverse(PyObject* self, visitproc visit, void* arg)
{
    return reinterpret_cast<PyTypeObject*>(&SbkObject_Type)->tp_traverse(self, visit, arg);
}
static int Sbk_PinyinConverter_clear(PyObject* self)
{
    return reinterpret_cast<PyTypeObject*>(&SbkObject_Type)->tp_clear(self);
}
// Class Definition -----------------------------------------------
extern "C" {
static SbkObjectType Sbk_PinyinConverter_Type = { { {
    PyVarObject_HEAD_INIT(&SbkObjectType_Type, 0)
    /*tp_name*/             "pypinyin.PinyinConverter",
    /*tp_basicsize*/        sizeof(SbkObject),
    /*tp_itemsize*/         0,
    /*tp_dealloc*/          &SbkDeallocWrapper,
    /*tp_print*/            0,
    /*tp_getattr*/          0,
    /*tp_setattr*/          0,
    /*tp_compare*/          0,
    /*tp_repr*/             0,
    /*tp_as_number*/        0,
    /*tp_as_sequence*/      0,
    /*tp_as_mapping*/       0,
    /*tp_hash*/             0,
    /*tp_call*/             0,
    /*tp_str*/              0,
    /*tp_getattro*/         0,
    /*tp_setattro*/         0,
    /*tp_as_buffer*/        0,
    /*tp_flags*/            Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE|Py_TPFLAGS_CHECKTYPES|Py_TPFLAGS_HAVE_GC,
    /*tp_doc*/              0,
    /*tp_traverse*/         Sbk_PinyinConverter_traverse,
    /*tp_clear*/            Sbk_PinyinConverter_clear,
    /*tp_richcompare*/      0,
    /*tp_weaklistoffset*/   0,
    /*tp_iter*/             0,
    /*tp_iternext*/         0,
    /*tp_methods*/          Sbk_PinyinConverter_methods,
    /*tp_members*/          0,
    /*tp_getset*/           0,
    /*tp_base*/             reinterpret_cast<PyTypeObject*>(&SbkObject_Type),
    /*tp_dict*/             0,
    /*tp_descr_get*/        0,
    /*tp_descr_set*/        0,
    /*tp_dictoffset*/       0,
    /*tp_init*/             Sbk_PinyinConverter_Init,
    /*tp_alloc*/            0,
    /*tp_new*/              SbkObjectTpNew,
    /*tp_free*/             0,
    /*tp_is_gc*/            0,
    /*tp_bases*/            0,
    /*tp_mro*/              0,
    /*tp_cache*/            0,
    /*tp_subclasses*/       0,
    /*tp_weaklist*/         0
}, },
    /*priv_data*/           0
};
} //extern


// Type conversion functions.

// Python to C++ pointer conversion - returns the C++ object of the Python wrapper (keeps object identity).
static void PinyinConverter_PythonToCpp_PinyinConverter_PTR(PyObject* pyIn, void* cppOut) {
    Shiboken::Conversions::pythonToCppPointer(&Sbk_PinyinConverter_Type, pyIn, cppOut);
}
static PythonToCppFunc is_PinyinConverter_PythonToCpp_PinyinConverter_PTR_Convertible(PyObject* pyIn) {
    if (pyIn == Py_None)
        return Shiboken::Conversions::nonePythonToCppNullPtr;
    if (PyObject_TypeCheck(pyIn, (PyTypeObject*)&Sbk_PinyinConverter_Type))
        return PinyinConverter_PythonToCpp_PinyinConverter_PTR;
    return 0;
}

// C++ to Python pointer conversion - tries to find the Python wrapper for the C++ object (keeps object identity).
static PyObject* PinyinConverter_PTR_CppToPython_PinyinConverter(const void* cppIn) {
    PyObject* pyOut = (PyObject*)Shiboken::BindingManager::instance().retrieveWrapper(cppIn);
    if (pyOut) {
        Py_INCREF(pyOut);
        return pyOut;
    }
    const char* typeName = typeid(*((::PinyinConverter*)cppIn)).name();
    return Shiboken::Object::newObject(&Sbk_PinyinConverter_Type, const_cast<void*>(cppIn), false, false, typeName);
}

void init_PinyinConverter(PyObject* module)
{
    SbkpypinyinTypes[SBK_PINYINCONVERTER_IDX] = reinterpret_cast<PyTypeObject*>(&Sbk_PinyinConverter_Type);

    if (!Shiboken::ObjectType::introduceWrapperType(module, "PinyinConverter", "PinyinConverter*",
        &Sbk_PinyinConverter_Type, &Shiboken::callCppDestructor< ::PinyinConverter >)) {
        return;
    }

    // Register Converter
    SbkConverter* converter = Shiboken::Conversions::createConverter(&Sbk_PinyinConverter_Type,
        PinyinConverter_PythonToCpp_PinyinConverter_PTR,
        is_PinyinConverter_PythonToCpp_PinyinConverter_PTR_Convertible,
        PinyinConverter_PTR_CppToPython_PinyinConverter);

    Shiboken::Conversions::registerConverterName(converter, "PinyinConverter");
    Shiboken::Conversions::registerConverterName(converter, "PinyinConverter*");
    Shiboken::Conversions::registerConverterName(converter, "PinyinConverter&");
    Shiboken::Conversions::registerConverterName(converter, typeid(::PinyinConverter).name());



}
