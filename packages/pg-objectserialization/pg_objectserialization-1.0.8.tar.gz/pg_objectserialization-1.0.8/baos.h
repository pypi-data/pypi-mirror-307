#ifndef BAOS_H
#define BAOS_H
#include "config.h"

#define BAOS_DEFAULT_SIZE 128

typedef struct baos_t
{
    int length;
    int used;
    string data;
} baos_t;

baos_t *baos_new(void);
int baos_free(baos_t *baos);

int baos_write_byte(baos_t *baos, int value);
int baos_write_short(baos_t *baos, int value);
int baos_write_int(baos_t *baos, int value);
int baos_write_long(baos_t *baos, long value);
int baos_write_double(baos_t *baos, double value);
int baos_write_string(baos_t *baos, string value, int length);

#endif