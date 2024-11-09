#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "baos.h"

baos_t *baos_new() {
    baos_t *baos = malloc(sizeof(baos_t));
    if ( !baos ) {
        return NULL;
    } else {
        baos->used = 0;
        baos->length = BAOS_DEFAULT_SIZE;
        baos->data = malloc(sizeof(byte)*baos->length);
        if ( !baos->data ) {
            free(baos);
            baos = NULL;
            return baos;
        }

        memset(baos->data, 0, sizeof(byte)*baos->length);
    }
    return baos;
}

int baos_free(baos_t *baos) {
    assert(baos);
    free(baos->data);
    baos->data = NULL;
    free(baos);
    baos = NULL;
    return SUCCESS;
}

static int check_size(baos_t *baos, int len) {
    assert(baos);
    assert(len>0);
    if ( baos->used + len > baos->length ) {
        int needs = BAOS_DEFAULT_SIZE;
        if ( needs < len ) {
            int i = 1;
            do {
                i++;
            } while ( (needs * i) < len );
            needs = BAOS_DEFAULT_SIZE * i;
        }

        int new_len = needs + baos->length;
        string data = realloc(baos->data, sizeof(byte)*new_len);
        if( !data ) {
            baos_free(baos);
            return FAILED;
        }

        baos->data = data;
        memset(baos->data + baos->length, 0, sizeof(byte) * needs);
        baos->length = new_len;
    }
    return SUCCESS;
}

int baos_write_byte(baos_t *baos, int value) {
    if ( check_size(baos, BYTE) == SUCCESS ) {
        baos->data[baos->used++] = (value&0xFF);
        return SUCCESS;
    }
    return FAILED;
}

int baos_write_short(baos_t *baos, int value) {
    if ( check_size(baos, SHORT ) == SUCCESS ) {
        baos->data[baos->used++] = (value & 0xFF);
        baos->data[baos->used++] = (value>>8) & 0xFF;
        return SUCCESS;
    }
    return FAILED;
}

static int baos_memcpy(baos_t *baos, int len, string value) {
    if ( check_size(baos, len) == SUCCESS ) {
        memcpy(baos->data + baos->used, value, len);
        baos->used += len;
        return SUCCESS;
    }
    return FAILED;
}

int baos_write_int(baos_t *baos, int value) {
    string val = (string) &value;
    return baos_memcpy(baos, INT, val);
}

int baos_write_long(baos_t *baos, long value) {
    string val = (string) &value;
    return baos_memcpy(baos, LONG, val);
}

int baos_write_double(baos_t *baos, double value) {
    string val = (string) &value;
    return baos_memcpy(baos, DOUBLE, val);
}

int baos_write_string(baos_t *baos, string value, int length) {
    return baos_memcpy(baos, length, value);
}
