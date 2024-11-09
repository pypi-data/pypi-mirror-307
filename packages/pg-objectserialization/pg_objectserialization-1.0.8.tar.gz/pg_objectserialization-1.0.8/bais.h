#ifndef BAIS_H
#define BAIS_H
#include "config.h"

typedef struct bais_t {
    int total;
    int readed;
    string buffer;
} bais_t;

bais_t *bais_new(const string buff, int len);
int bais_free(bais_t *bais);

int bais_read_byte(bais_t *bais, byte *val);
int bais_read_ubyte(bais_t *bais, ubyte *val);
int bais_read_short(bais_t *bais, short *val);
int bais_read_ushort(bais_t *bais, ushort *val);
int bais_read_int(bais_t *bais, int *val);
int bais_read_uint(bais_t *bais, uint *val);
int bais_read_long(bais_t *bais, long *val);
int bais_read_ulong(bais_t *bais, ulong *val);
int bais_read_float(bais_t *bais, float *val);
int bais_read_double(bais_t *bais, double *val);
int bais_read_string(bais_t *bais, int len, string val);

#endif