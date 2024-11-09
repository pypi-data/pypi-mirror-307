#ifndef CONFIG_H
#define CONFIG_H

#define DEBUG 1

#define Py_TYPE_NONE 100
#define Py_TYPE_BOOLEAN 99
#define PY_TYPE_BYTE 98
#define PY_TYPE_SHORT 97
#define Py_TYPE_INT 96
#define PY_TYPE_LONG 95
#define PY_TYPE_DOUBLE 94
#define PY_TYPE_BSTR 93
#define PY_TYPE_SSTR 92
#define PY_TYPE_ISTR 91
#define PY_TYPE_UNI 90
#define PY_TYPE_BLIST 89
#define PY_TYPE_SLIST 88
#define PY_TYPE_BDICT 87
#define PY_TYPE_SDICT 86

#define SUCCESS 0
#define FAILED -1

#define BYTE 1
#define SHORT 2
#define INT 4
#define LONG 8
#define FLOAT 4
#define DOUBLE 8

typedef char byte;
typedef unsigned char ubyte;
typedef unsigned short ushort;
typedef unsigned long ulong;
typedef unsigned int uint;
typedef char *string;

#endif