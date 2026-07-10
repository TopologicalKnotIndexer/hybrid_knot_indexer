#ifndef LINK_PDCODE_H
#define LINK_PDCODE_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    double x;
    double y;
    double z;
} lp_point3;

typedef struct {
    int a[4];
} lp_crossing;

typedef struct {
    lp_crossing* crossings;
    size_t count;
} lp_pdcode;

typedef struct {
    int max_attempts;
    double epsilon;
    int prefer_min_crossings;
    int use_direction;
    lp_point3 direction;
} lp_options;

void lp_default_options(lp_options* options);
void lp_free_pdcode(lp_pdcode* pd);

int lp_compute_pdcode(const lp_point3* points,
                      size_t count,
                      const lp_options* options,
                      lp_pdcode* out,
                      char* error,
                      size_t error_size);

int lp_format_pdcode(const lp_pdcode* pd, char* buffer, size_t buffer_size);
int lp_validate_pdcode(const lp_pdcode* pd);

#ifdef __cplusplus
}
#endif

#endif
