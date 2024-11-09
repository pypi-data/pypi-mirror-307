#define PY_SSIZE_T_CLEAN
#include<Python.h>
#include<datetime.h>
#include"baos.h"
#include"bais.h"

int __baos_log__(baos_t *baos){
	assert(baos);
	const int len = baos->used;
	fprintf(stdout,"dumps net:");
	int i=0;
	for(; i<len;i++){
		fprintf(stdout, "%hhu,", baos->data[i]);
	}
	fprintf(stdout, "\n");
	return 0;
}

int __bais_log__(bais_t *bais){
    assert(bais);
    const int len = bais->total;
    fprintf(stdout, "loads net:");
    for(int i=0; i<len; i++){
        fprintf(stdout, "%hhu,", bais->buffer[i]);
    }
    fprintf(stdout, "\n");
    return 0;
}

static int _write_len_for_list_or_tuple(baos_t *baos, int len) {
    if (len <= 255) {
        if(baos_write_byte(baos, PY_TYPE_BLIST)==FAILED) return FAILED;
        if(baos_write_byte(baos, len)==FAILED) return FAILED;
    }else{
        if(baos_write_byte(baos, PY_TYPE_SLIST)==FAILED) return FAILED;
        if(baos_write_short(baos, len)==FAILED) return FAILED;
    }
    return SUCCESS;
}

static int 
__pack(PyObject *obj, baos_t *baos)
{
    if(obj == Py_None) {
        return baos_write_byte(baos, Py_TYPE_NONE);
    }
    else if (PyBool_Check(obj)) {
        if(baos_write_byte(baos, Py_TYPE_BOOLEAN)==FAILED) return FAILED;
        return baos_write_byte(baos, (Py_False == obj)?0:1);
    }
    else if (PyLong_Check(obj)) {
        int overflow;
        long val = PyLong_AsLongAndOverflow(obj, &overflow);
        if (overflow==0){
            if(val>=-128 && val <=127) {
                if(baos_write_byte(baos, PY_TYPE_BYTE)==FAILED) return FAILED;
                return baos_write_byte(baos, (byte)val);
            }else if(val >= -32768 && val <= 32767) {
                if(baos_write_byte(baos, PY_TYPE_SHORT)==FAILED) return FAILED;
                return baos_write_short(baos, (short)val);
            }
            else if(val >= -2147483647 && val <= 2147483647) {
                if(baos_write_byte(baos, Py_TYPE_INT)==FAILED) return FAILED;
                return baos_write_int(baos, (int)val);
            }else {
                if(baos_write_byte(baos, PY_TYPE_LONG)==FAILED) return FAILED;
                return baos_write_long(baos, val);
            }
        }else{
            double d_val = PyLong_AsDouble(obj);
            PyObject *f_val = PyFloat_FromDouble(d_val);
            if (__pack(f_val, baos)==FAILED) {
                Py_XDECREF(f_val);
                return FAILED;
            }else{
                Py_XDECREF(f_val);
                return SUCCESS;
            }
        }
    }
    else if (PyFloat_Check(obj)) {
        double val = PyFloat_AS_DOUBLE(obj);
        if(baos_write_byte(baos, PY_TYPE_DOUBLE)==FAILED) return FAILED;
        return baos_write_double(baos, val);
    }
    else if (PyDict_Check(obj)) {
        PyObject *_items = PyDict_Items(obj);
        Py_ssize_t len = PyList_Size(_items);

        if ( len <= 255 ) {
            if(baos_write_byte(baos, PY_TYPE_BDICT)==FAILED) goto _except;
            if(baos_write_byte(baos, (int)len)==FAILED) goto _except;
        } else {
            if(baos_write_byte(baos, PY_TYPE_SDICT)==FAILED) goto _except;
            if(baos_write_short(baos, (int)len)==FAILED) goto _except;
        }

        for (int i=0; i<len; i++){
            PyObject *_tuple = PyList_GetItem(_items, i);
            if(__pack(PyTuple_GetItem(_tuple, 0), baos)==FAILED) goto _except;
            if(__pack(PyTuple_GetItem(_tuple, 1), baos)==FAILED) goto _except;
        }
        Py_XDECREF(_items);
        return SUCCESS;
        _except:
            Py_XDECREF(_items);
            return FAILED;
    }
    else if (PyList_Check(obj)) {
        Py_ssize_t len = PyList_Size(obj);
        if(_write_len_for_list_or_tuple(baos, (int)len)==FAILED) return FAILED;
        for(int i=0; i<len; i++){
            PyObject *_item = PyList_GetItem(obj, i);
            if(__pack(_item, baos)==FAILED) return FAILED;
        }
        return SUCCESS;
    }
    else if (PyTuple_Check(obj)) {
        Py_ssize_t len = PyTuple_Size(obj);
        if(_write_len_for_list_or_tuple(baos, (int)len)==FAILED) return FAILED;
        for (int i=0; i<len; i++){
            PyObject *_item = PyTuple_GetItem(obj, i);
            if(__pack(_item, baos)==FAILED) return FAILED;
        }
        return SUCCESS;
    }
//    else if (PyUnicode_Check(obj)) {
//        Py_ssize_t len = PyUnicode_GET_LENGTH(obj);
//        if (len<=255) {
//            if(baos_write_byte(baos, PY_TYPE_BSTR)==FAILED) return FAILED;
//            if(baos_write_byte(baos, (int)len)==FAILED) return FAILED;
//        } else if( len<= 65535 ) {
//            if(baos_write_byte(baos, PY_TYPE_SSTR)==FAILED) return FAILED;
//            if(baos_write_short(baos, (int)len)==FAILED) return FAILED;
//        } else {
//            if(baos_write_byte(baos, PY_TYPE_ISTR)==FAILED) return FAILED;
//            if(baos_write_int(baos, (int)len)==FAILED) return FAILED;
//        }
//
//        if(len==0){
//            return SUCCESS;
//        }
//
//        return baos_write_string(baos, (string)PyUnicode_AsUTF8(obj), (int)len);
//    }
    else if (PyUnicode_Check(obj)) {
        Py_ssize_t len = PyUnicode_GET_LENGTH(obj);
        if(baos_write_byte(baos, PY_TYPE_UNI)==FAILED) return FAILED;
        if(baos_write_short(baos, (int)len)==FAILED) return FAILED;

        if(len==0){
            return SUCCESS;
        }

        const char *_data = PyUnicode_AS_DATA(obj);
        string _target = malloc(sizeof(byte) * (len<<1));
        if(!_target) {
            return FAILED;
        }
        for (int i=0; i<len; i++){
            _target[(i<<1)] = _data[(i<<2)];
            _target[(i<<1)+1] = _data[(i<<2)+1];
        }

        int _ret = baos_write_string(baos, _target, ((int)len)<<1);

        free(_target);

        return _ret;
    }
    else if (PyDateTime_Check(obj)) {
        char buff[50];
        int wlen = 0;
        wlen += sprintf(buff+wlen, "%4d-", PyDateTime_GET_YEAR(obj));
        wlen += sprintf(buff+wlen, "%02d-", PyDateTime_GET_MONTH(obj));
        wlen += sprintf(buff+wlen, "%02d ", PyDateTime_GET_DAY(obj));
        wlen += sprintf(buff+wlen, "%02d:", PyDateTime_DATE_GET_HOUR(obj));
        wlen += sprintf(buff+wlen, "%02d:", PyDateTime_DATE_GET_MINUTE(obj));
        wlen += sprintf(buff+wlen, "%02d.", PyDateTime_DATE_GET_SECOND(obj));
        wlen += sprintf(buff+wlen, "%06d", PyDateTime_DATE_GET_MICROSECOND(obj));
        buff[wlen] = 0;
        PyObject *_datetime = PyUnicode_FromString(buff);
        int _pdt = __pack(_datetime, baos);
        Py_DECREF(_datetime);
        return _pdt;
    }
    else{
        PyErr_SetString(PyExc_SystemError, "dumps not supported this serialize data type.");
        return FAILED;
    }
}

static PyObject *
dumps(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char* kwlist[] = {"o", "p", NULL};
    PyObject *_obj;
    int p_log=0;
//    if (!PyArg_ParseTuple(args, "O", &_obj)) {
//        PyErr_SetString(PyExc_SystemError, "dumps can't parse parameter.");
//        return NULL;
//    }
    if (!PyArg_ParseTupleAndKeywords(args,kwargs,"O|p",kwlist,&_obj,&p_log)) {
        PyErr_SetString(PyExc_SystemError, "dumps can't parse parameter.");
        return NULL;
    }
    baos_t *_baos = baos_new();
    if ( !_baos ) {
        PyErr_SetString(PyExc_SystemError, "dumps lack of memory.");
        return NULL;
    }
    if( __pack(_obj, _baos) == FAILED ) {
        baos_free(_baos);
        PyErr_SetString(PyExc_SystemError, "dumps parse error.");
        return NULL;
    }
    if(p_log) __baos_log__(_baos);
    PyObject *_ret = Py_BuildValue("y#", _baos->data, _baos->used);
    baos_free(_baos);
    return _ret;
}

static PyObject *
__load_unicode(bais_t *bais) {
    ushort _unicodeLen;
    if(bais_read_ushort(bais, &_unicodeLen)==FAILED) {
        return NULL;
    }
    string _utarget = malloc(sizeof(byte)*(_unicodeLen<<2));
    if(!_utarget){
        return NULL;
    }

    if(bais->readed+(_unicodeLen<<1) > bais->total) {
        free(_utarget);
        return NULL;
    }
    memset(_utarget, 0, (_unicodeLen<<2));
    for(int i=0;i<_unicodeLen;i++){
        _utarget[(i<<2)] = bais->buffer[bais->readed+((i<<1))];
        _utarget[(i<<2)+1] = bais->buffer[bais->readed+((i<<1)+1)];
    }
    bais->readed += (_unicodeLen<<1);
    PyObject *_retunicode = PyUnicode_FromWideChar((const wchar_t *)_utarget, (_unicodeLen));
    free(_utarget);
    return _retunicode;
}

static PyObject *
__unpack(bais_t *bais, int *ret)
{
    *ret = SUCCESS;
    byte _type;
    if (bais_read_byte(bais, &_type)==FAILED) {
        *ret = FAILED;
        Py_RETURN_NONE;
    }
    switch (_type)
    {
    case Py_TYPE_NONE:
        Py_RETURN_NONE;
    case Py_TYPE_BOOLEAN:
    case PY_TYPE_BYTE:;
        byte _valb;
        if(bais_read_byte(bais, &_valb)==FAILED){
            *ret = FAILED;
            Py_RETURN_NONE;
        }
        return PyLong_FromLong(_valb);
    case PY_TYPE_SHORT:;
        short _vals;
        if(bais_read_short(bais, &_vals)==FAILED) {
            *ret = FAILED;
            Py_RETURN_NONE;
        }
        return PyLong_FromLong(_vals);
    case Py_TYPE_INT:;
        int _vali;
        if(bais_read_int(bais, &_vali)==FAILED) {
            *ret = FAILED;
            Py_RETURN_NONE;
        }
        return PyLong_FromLong(_vali);
    case PY_TYPE_BLIST:
    case PY_TYPE_SLIST:;
        int _len;
        if(_type==PY_TYPE_SLIST){
            ushort _valus;
            if(bais_read_ushort(bais, &_valus)==FAILED) {
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            _len = _valus;
        }else{
            ubyte _valub;
            if(bais_read_ubyte(bais, &_valub)==FAILED){
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            _len = _valub;
        }
        PyObject *_retlist = PyList_New(0);
        for(int i=0;i<_len;i++){
            int _reti;
            PyObject *_item = __unpack(bais, &_reti);
            if(_reti==FAILED){
                Py_DECREF(_item);
                Py_DECREF(_retlist);
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            PyList_Append(_retlist, _item);
            Py_DECREF(_item);
        }
        return _retlist;
    case PY_TYPE_BSTR:
    case PY_TYPE_SSTR:
    case PY_TYPE_ISTR:;
        int len;
        if(_type==PY_TYPE_BSTR){
            ubyte _valub;
            if(bais_read_ubyte(bais, &_valub)==FAILED) {
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            len = _valub;
        }else if(_type==PY_TYPE_SSTR){
            ushort _valus;
            if(bais_read_ushort(bais, &_valus)==FAILED){
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            len = _valus;
        }else{
            uint _valui;
            if(bais_read_uint(bais, &_valui)==FAILED) {
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            len = _valui;
        }
        string _target = malloc(sizeof(byte)*len);
        if(!_target){
            *ret = FAILED;
            Py_RETURN_NONE;
        }
        if(bais_read_string(bais, len, _target)==FAILED) {
            free(_target);
            *ret = FAILED;
            Py_RETURN_NONE;
        }
        PyObject *_ret = PyUnicode_FromStringAndSize(_target, len);
        free(_target);
        return _ret;
    case PY_TYPE_UNI:;
        PyObject *_retVal = __load_unicode(bais);
        if(!_retVal){
            *ret = FAILED;
            Py_RETURN_NONE;
        }
        return _retVal;
    case PY_TYPE_LONG:;
        long _vall;
        if(bais_read_long(bais, &_vall)==FAILED){
            *ret = FAILED;
            Py_RETURN_NONE;
        }
        return PyLong_FromLong(_vall);
    case PY_TYPE_BDICT:
    case PY_TYPE_SDICT:;
        int _lendict;
        if(_type==PY_TYPE_BDICT){
            ubyte _valub;
            if(bais_read_ubyte(bais, &_valub)==FAILED){
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            _lendict = _valub;
        }else{
            ushort _valus;
            if(bais_read_ushort(bais, &_valus)==FAILED) {
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            _lendict = _valus;
        }
        PyObject *_dict = PyDict_New();
        for(int i=0;i<_lendict;i++){
            int _retval;
            PyObject *_key = __unpack(bais, &_retval);
            if(_retval==FAILED){
                Py_DECREF(_key);
                Py_DECREF(_dict);
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            PyObject *_item = __unpack(bais, &_retval);
            if(_retval==FAILED){
                Py_DECREF(_key);
                Py_DECREF(_item);
                Py_DECREF(_dict);
                *ret = FAILED;
                Py_RETURN_NONE;
            }
            PyDict_SetItem(_dict, _key, _item);
            Py_DECREF(_key);
            Py_DECREF(_item);
        }
        return _dict;
    case PY_TYPE_DOUBLE:;
        double _valf;
        if(bais_read_double(bais, &_valf)==FAILED) {
            *ret = FAILED;
            Py_RETURN_NONE;
        }
        return PyFloat_FromDouble(_valf);
    }
    *ret = FAILED;
    Py_RETURN_NONE;
}

static PyObject *
loads(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char* kwlist[] = {"o", "p", NULL};
    string _str=NULL;
    int len;
    int p_log = 0;
//    if (!PyArg_ParseTuple(args, "y#", &_str, &len)) {
//        PyErr_SetString(PyExc_SystemError, "loads can't parse parameter.");
//        return NULL;
//    }
    if (!PyArg_ParseTupleAndKeywords(args,kwargs,"y#|p",kwlist,&_str, &len, &p_log)) {
        PyErr_SetString(PyExc_SystemError, "loads can't parse parameter.");
        return NULL;
    }
    bais_t *bais = bais_new(_str, len);
    if(!bais) {
        PyErr_SetString(PyExc_MemoryError, "loads lack of memory.");
        return NULL;
    }
    if(p_log) __bais_log__(bais);
    int _ret;
    PyObject *rv = __unpack(bais, &_ret);
    if(_ret==FAILED){
        PyErr_SetString(PyExc_SystemError, "loads unpack error.");
        bais_free(bais);
        Py_DECREF(rv);
        return NULL;
    }
    bais_free(bais);
    return rv;
}

static PyMethodDef pg_objectserialization_methods[] = {
    {"dumps", (PyCFunction)dumps, METH_VARARGS | METH_KEYWORDS, "dumps a python object to stream."},
    {"loads", (PyCFunction)loads, METH_VARARGS | METH_KEYWORDS, "loads a python object from stream."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef pg_objectserialization_module = {
    PyModuleDef_HEAD_INIT,
    "pg_objectserialization",
    "python game object serialization module",
    -1,
    pg_objectserialization_methods
};

PyMODINIT_FUNC PyInit_pg_objectserialization(void)
{
    PyDateTime_IMPORT;
    return PyModule_Create(&pg_objectserialization_module);
}
