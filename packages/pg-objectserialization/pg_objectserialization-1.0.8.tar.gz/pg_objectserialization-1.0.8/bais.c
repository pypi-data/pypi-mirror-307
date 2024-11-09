#include<string.h>
#include<assert.h>
#include<stdlib.h>
#include<stdio.h>
#include "bais.h"

bais_t *bais_new(const string buff, int len)
{
    assert(buff);
    bais_t *bais = malloc(sizeof(bais_t));
    if (!bais) {
        return NULL;
    }else{
        bais->buffer = buff;
        bais->readed = 0;
        bais->total = len;
    }
    return bais;
}

int bais_free(bais_t *bais)
{
    assert(bais);
    free(bais);
    return SUCCESS;
}

static int check_size(bais_t *bais, int len) {
    if (bais->readed + len > bais->total) return FAILED;
    return SUCCESS;
}

int bais_read_byte(bais_t *bais, byte *val)
{
    if (check_size(bais, BYTE) == FAILED) return FAILED;
    *val = *(byte *)(&bais->buffer[bais->readed]);
    bais->readed += BYTE;
    return SUCCESS;
}

int bais_read_ubyte(bais_t *bais, ubyte *val)
{
    if (check_size(bais, BYTE) == FAILED) return FAILED;
    *val = *(ubyte *)(&bais->buffer[bais->readed]);
    bais->readed += BYTE;
    return SUCCESS;
}

int bais_read_short(bais_t *bais, short *val) {
    if(check_size(bais, SHORT) == FAILED) return FAILED;
    *val = *(short *)(&bais->buffer[bais->readed]);
    bais->readed += SHORT;
    return SUCCESS;
}

int bais_read_ushort(bais_t *bais, ushort *val) {
    if(check_size(bais, SHORT) == FAILED) return FAILED;
    *val = *(ushort *)(&bais->buffer[bais->readed]);
    bais->readed += SHORT;
    return SUCCESS;
}

int bais_read_int(bais_t *bais, int *val) {
    if(check_size(bais, INT) == FAILED) return FAILED;
    *val = *(int *)(&bais->buffer[bais->readed]);
    bais->readed += INT;
    return SUCCESS;
}

int bais_read_uint(bais_t *bais, uint *val) {
    if(check_size(bais, INT) == FAILED) return FAILED;
    *val = *(uint *)(&bais->buffer[bais->readed]);
    bais->readed += INT;
    return SUCCESS;
}

int bais_read_long(bais_t *bais, long *val) {
    if(check_size(bais, LONG) == FAILED) return FAILED;
    *val = *(long *)(&bais->buffer[bais->readed]);
    bais->readed += LONG;
    return SUCCESS;
}

int bais_read_float(bais_t *bais, float *val) {
    if(check_size(bais, FLOAT) == FAILED) return FAILED;
    *val = *(float *)(&bais->buffer[bais->readed]);
    bais->readed += FLOAT;
    return SUCCESS;
}

int bais_read_double(bais_t *bais, double *val) {
    if(check_size(bais, DOUBLE) == FAILED) return FAILED;
    *val = *(double *)(&bais->buffer[bais->readed]);
    bais->readed += DOUBLE;
    return SUCCESS;
}

int bais_read_string(bais_t *bais, int len, string val) {
    if(check_size(bais, len) == FAILED) return FAILED;
    memcpy(val, bais->buffer+bais->readed, len);
    bais->readed += len;
    return SUCCESS;
}
