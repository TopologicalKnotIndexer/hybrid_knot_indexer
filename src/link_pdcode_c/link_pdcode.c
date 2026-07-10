#include "link_pdcode.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846264338327950288
#endif

typedef struct {
    double x;
    double y;
} point2;

typedef struct {
    int crossing;
    int segment;
    double t;
    double x;
    double y;
    double z;
    int incoming_label;
    int outgoing_label;
} occurrence;

typedef struct {
    int segment_a;
    int segment_b;
    double ta;
    double tb;
    double x;
    double y;
    double za;
    double zb;
    int occ_a;
    int occ_b;
} crossing_work;

typedef struct {
    int label;
    double angle;
    int first;
} half_edge;

typedef struct {
    lp_point3 normal;
    lp_point3 ux;
    lp_point3 uy;
} projection_basis;

static void set_error(char* error, size_t error_size, const char* message) {
    if (error && error_size) {
        snprintf(error, error_size, "%s", message ? message : "unknown error");
    }
}

static double dot3(lp_point3 a, lp_point3 b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

static lp_point3 cross3(lp_point3 a, lp_point3 b) {
    lp_point3 out;
    out.x = a.y * b.z - a.z * b.y;
    out.y = a.z * b.x - a.x * b.z;
    out.z = a.x * b.y - a.y * b.x;
    return out;
}

static double norm3(lp_point3 a) {
    return sqrt(dot3(a, a));
}

static int normalize3(lp_point3* a) {
    double n = norm3(*a);
    if (n <= 0.0 || !isfinite(n)) return 0;
    a->x /= n;
    a->y /= n;
    a->z /= n;
    return 1;
}

static double cross2(point2 a, point2 b) {
    return a.x * b.y - a.y * b.x;
}

static point2 sub2(point2 a, point2 b) {
    point2 out;
    out.x = a.x - b.x;
    out.y = a.y - b.y;
    return out;
}

static point2 lerp2(point2 a, point2 b, double t) {
    point2 out;
    out.x = a.x + (b.x - a.x) * t;
    out.y = a.y + (b.y - a.y) * t;
    return out;
}

static double lerp_double(double a, double b, double t) {
    return a + (b - a) * t;
}

static int adjacent_segments(int a, int b, int n) {
    if (a == b) return 1;
    if ((a + 1) % n == b) return 1;
    if ((b + 1) % n == a) return 1;
    return 0;
}

static int build_basis(lp_point3 normal, projection_basis* basis) {
    lp_point3 helper;
    if (!normalize3(&normal)) return 0;
    if (fabs(normal.x) <= fabs(normal.y) && fabs(normal.x) <= fabs(normal.z)) {
        helper = (lp_point3){1.0, 0.0, 0.0};
    } else if (fabs(normal.y) <= fabs(normal.z)) {
        helper = (lp_point3){0.0, 1.0, 0.0};
    } else {
        helper = (lp_point3){0.0, 0.0, 1.0};
    }

    basis->ux = cross3(normal, helper);
    if (!normalize3(&basis->ux)) return 0;
    basis->uy = cross3(normal, basis->ux);
    if (!normalize3(&basis->uy)) return 0;
    basis->normal = normal;
    return 1;
}

static lp_point3 candidate_direction(int attempt) {
    static const lp_point3 fixed[] = {
        {0.0, 0.0, 1.0},
        {1.0, 1.0, 1.0},
        {1.0, 2.0, 3.0},
        {-2.0, 1.0, 3.0},
        {3.0, -2.0, 1.0},
        {5.0, 7.0, 11.0},
        {-7.0, 11.0, 5.0},
    };
    if (attempt < (int)(sizeof(fixed) / sizeof(fixed[0]))) {
        lp_point3 out = fixed[attempt];
        normalize3(&out);
        return out;
    }

    {
        double k = (double)(attempt + 1);
        double theta = 2.0 * M_PI * fmod(k * 0.6180339887498948482, 1.0);
        double z = 2.0 * fmod(k * 0.4142135623730950488, 1.0) - 1.0;
        double r = sqrt(fmax(0.0, 1.0 - z * z));
        return (lp_point3){r * cos(theta), r * sin(theta), z};
    }
}

static void project_points(const lp_point3* points,
                           size_t count,
                           const projection_basis* basis,
                           point2* out2,
                           double* outz) {
    size_t i;
    for (i = 0; i < count; ++i) {
        out2[i].x = dot3(points[i], basis->ux);
        out2[i].y = dot3(points[i], basis->uy);
        outz[i] = dot3(points[i], basis->normal);
    }
}

static int segment_intersection(point2 p,
                                point2 p2,
                                point2 q,
                                point2 q2,
                                double eps,
                                double* t_out,
                                double* u_out) {
    point2 r = sub2(p2, p);
    point2 s = sub2(q2, q);
    point2 qp = sub2(q, p);
    double denom = cross2(r, s);
    double t;
    double u;
    if (fabs(denom) <= eps) return 0;
    t = cross2(qp, s) / denom;
    u = cross2(qp, r) / denom;
    if (t <= eps || t >= 1.0 - eps || u <= eps || u >= 1.0 - eps) return 0;
    *t_out = t;
    *u_out = u;
    return 1;
}

static int occurrence_cmp(const void* left, const void* right) {
    const occurrence* a = (const occurrence*)left;
    const occurrence* b = (const occurrence*)right;
    if (a->segment != b->segment) return a->segment < b->segment ? -1 : 1;
    if (a->t < b->t) return -1;
    if (a->t > b->t) return 1;
    return 0;
}

static int pd_cmp(const void* left, const void* right) {
    const lp_crossing* a = (const lp_crossing*)left;
    const lp_crossing* b = (const lp_crossing*)right;
    int i;
    for (i = 0; i < 4; ++i) {
        if (a->a[i] != b->a[i]) return a->a[i] < b->a[i] ? -1 : 1;
    }
    return 0;
}

static int half_edge_cmp(const void* left, const void* right) {
    const half_edge* a = (const half_edge*)left;
    const half_edge* b = (const half_edge*)right;
    if (a->angle > b->angle) return -1;
    if (a->angle < b->angle) return 1;
    return 0;
}

static double angle_from(point2 from, point2 center) {
    double a = atan2(from.y - center.y, from.x - center.x);
    if (a < 0.0) a += 2.0 * M_PI;
    return a;
}

static int append_occurrence(occurrence** items, size_t* count, size_t* cap, occurrence value) {
    occurrence* next;
    if (*count == *cap) {
        size_t next_cap = *cap ? *cap * 2 : 16;
        next = (occurrence*)realloc(*items, next_cap * sizeof(**items));
        if (!next) return 0;
        *items = next;
        *cap = next_cap;
    }
    (*items)[(*count)++] = value;
    return 1;
}

static int append_crossing(crossing_work** items, size_t* count, size_t* cap, crossing_work value) {
    crossing_work* next;
    if (*count == *cap) {
        size_t next_cap = *cap ? *cap * 2 : 16;
        next = (crossing_work*)realloc(*items, next_cap * sizeof(**items));
        if (!next) return 0;
        *items = next;
        *cap = next_cap;
    }
    (*items)[(*count)++] = value;
    return 1;
}

static int find_crossings(const lp_point3* points,
                          size_t count,
                          const projection_basis* basis,
                          double eps,
                          point2** projected_out,
                          double** z_out,
                          occurrence** occurrences_out,
                          size_t* occurrence_count_out,
                          crossing_work** crossings_out,
                          size_t* crossing_count_out) {
    point2* projected = NULL;
    double* z = NULL;
    occurrence* occurrences = NULL;
    crossing_work* crossings = NULL;
    size_t occurrence_count = 0, occurrence_cap = 0;
    size_t crossing_count = 0, crossing_cap = 0;
    size_t i, j;

    projected = (point2*)calloc(count, sizeof(*projected));
    z = (double*)calloc(count, sizeof(*z));
    if (!projected || !z) goto fail;
    project_points(points, count, basis, projected, z);

    for (i = 0; i < count; ++i) {
        for (j = i + 1; j < count; ++j) {
            double ti, tj;
            double zi, zj;
            crossing_work cw;
            int id;
            if (adjacent_segments((int)i, (int)j, (int)count)) continue;
            if (!segment_intersection(projected[i], projected[(i + 1) % count],
                                      projected[j], projected[(j + 1) % count],
                                      eps, &ti, &tj)) {
                continue;
            }
            zi = lerp_double(z[i], z[(i + 1) % count], ti);
            zj = lerp_double(z[j], z[(j + 1) % count], tj);
            if (fabs(zi - zj) <= eps) goto fail;

            id = (int)crossing_count;
            cw.segment_a = (int)i;
            cw.segment_b = (int)j;
            cw.ta = ti;
            cw.tb = tj;
            cw.x = lerp_double(projected[i].x, projected[(i + 1) % count].x, ti);
            cw.y = lerp_double(projected[i].y, projected[(i + 1) % count].y, ti);
            cw.za = zi;
            cw.zb = zj;
            cw.occ_a = -1;
            cw.occ_b = -1;
            if (!append_crossing(&crossings, &crossing_count, &crossing_cap, cw)) goto fail;
            if (!append_occurrence(&occurrences, &occurrence_count, &occurrence_cap,
                                   (occurrence){id, (int)i, ti, cw.x, cw.y, zi, 0, 0})) {
                goto fail;
            }
            if (!append_occurrence(&occurrences, &occurrence_count, &occurrence_cap,
                                   (occurrence){id, (int)j, tj, cw.x, cw.y, zj, 0, 0})) {
                goto fail;
            }
        }
    }

    *projected_out = projected;
    *z_out = z;
    *occurrences_out = occurrences;
    *occurrence_count_out = occurrence_count;
    *crossings_out = crossings;
    *crossing_count_out = crossing_count;
    return 1;

fail:
    free(projected);
    free(z);
    free(occurrences);
    free(crossings);
    return 0;
}

static int build_pd_from_projection(size_t point_count,
                                    point2* projected,
                                    occurrence* occurrences,
                                    size_t occurrence_count,
                                    crossing_work* crossings,
                                    size_t crossing_count,
                                    lp_pdcode* out) {
    size_t i;
    lp_crossing* result = NULL;

    if (crossing_count == 0) {
        out->crossings = NULL;
        out->count = 0;
        return 1;
    }

    qsort(occurrences, occurrence_count, sizeof(*occurrences), occurrence_cmp);
    for (i = 0; i < occurrence_count; ++i) {
        occurrence* occ = &occurrences[i];
        occ->incoming_label = (int)i + 1;
        occ->outgoing_label = (int)((i + 1) % occurrence_count) + 1;
        if (crossings[occ->crossing].segment_a == occ->segment &&
            fabs(crossings[occ->crossing].ta - occ->t) < 1e-8) {
            crossings[occ->crossing].occ_a = (int)i;
        } else {
            crossings[occ->crossing].occ_b = (int)i;
        }
    }

    result = (lp_crossing*)calloc(crossing_count, sizeof(*result));
    if (!result) return 0;

    for (i = 0; i < crossing_count; ++i) {
        crossing_work* cw = &crossings[i];
        occurrence* occ_a = &occurrences[cw->occ_a];
        occurrence* occ_b = &occurrences[cw->occ_b];
        occurrence* under = cw->za <= cw->zb ? occ_a : occ_b;
        occurrence* over = cw->za <= cw->zb ? occ_b : occ_a;
        point2 center = {cw->x, cw->y};
        point2 under_left = lerp2(projected[under->segment],
                                  projected[(under->segment + 1) % point_count],
                                  under->t * 0.5);
        point2 under_right = lerp2(projected[under->segment],
                                   projected[(under->segment + 1) % point_count],
                                   (1.0 + under->t) * 0.5);
        point2 over_left = lerp2(projected[over->segment],
                                 projected[(over->segment + 1) % point_count],
                                 over->t * 0.5);
        point2 over_right = lerp2(projected[over->segment],
                                  projected[(over->segment + 1) % point_count],
                                  (1.0 + over->t) * 0.5);
        half_edge edges[4];
        int first = -1;
        int k;

        edges[0] = (half_edge){under->incoming_label, angle_from(under_left, center), 1};
        edges[1] = (half_edge){over->incoming_label, angle_from(over_left, center), 0};
        edges[2] = (half_edge){under->outgoing_label, angle_from(under_right, center), 0};
        edges[3] = (half_edge){over->outgoing_label, angle_from(over_right, center), 0};
        qsort(edges, 4, sizeof(edges[0]), half_edge_cmp);
        for (k = 0; k < 4; ++k) {
            if (edges[k].first) {
                first = k;
                break;
            }
        }
        if (first < 0) {
            free(result);
            return 0;
        }
        for (k = 0; k < 4; ++k) result[i].a[k] = edges[(first + k) % 4].label;
    }

    qsort(result, crossing_count, sizeof(*result), pd_cmp);
    out->crossings = result;
    out->count = crossing_count;
    return 1;
}

void lp_default_options(lp_options* options) {
    if (!options) return;
    options->max_attempts = 256;
    options->epsilon = 1e-10;
    options->prefer_min_crossings = 1;
    options->use_direction = 0;
    options->direction = (lp_point3){0.0, 0.0, 1.0};
}

void lp_free_pdcode(lp_pdcode* pd) {
    if (!pd) return;
    free(pd->crossings);
    pd->crossings = NULL;
    pd->count = 0;
}

int lp_compute_pdcode(const lp_point3* points,
                      size_t count,
                      const lp_options* options_in,
                      lp_pdcode* out,
                      char* error,
                      size_t error_size) {
    lp_options options;
    int attempt;
    int max_attempts;
    lp_pdcode best = {0};
    int have_best = 0;

    if (!out) {
        set_error(error, error_size, "output pointer is null");
        return 0;
    }
    out->crossings = NULL;
    out->count = 0;
    if (!points && count) {
        set_error(error, error_size, "point pointer is null");
        return 0;
    }
    if (count <= 3) return 1;

    lp_default_options(&options);
    if (options_in) options = *options_in;
    if (options.max_attempts <= 0) options.max_attempts = 1;
    if (options.epsilon <= 0.0) options.epsilon = 1e-10;
    max_attempts = options.use_direction ? 1 : options.max_attempts;

    for (attempt = 0; attempt < max_attempts; ++attempt) {
        projection_basis basis;
        point2* projected = NULL;
        double* z = NULL;
        occurrence* occurrences = NULL;
        crossing_work* crossings = NULL;
        size_t occurrence_count = 0;
        size_t crossing_count = 0;
        lp_pdcode pd = {0};
        lp_point3 direction = options.use_direction ? options.direction : candidate_direction(attempt);

        if (!build_basis(direction, &basis)) continue;
        if (!find_crossings(points, count, &basis, options.epsilon, &projected, &z,
                            &occurrences, &occurrence_count, &crossings, &crossing_count)) {
            free(projected);
            free(z);
            free(occurrences);
            free(crossings);
            continue;
        }
        if (!build_pd_from_projection(count, projected, occurrences, occurrence_count,
                                      crossings, crossing_count, &pd)) {
            free(projected);
            free(z);
            free(occurrences);
            free(crossings);
            lp_free_pdcode(&pd);
            continue;
        }
        free(projected);
        free(z);
        free(occurrences);
        free(crossings);

        if (!have_best || pd.count < best.count) {
            lp_free_pdcode(&best);
            best = pd;
            have_best = 1;
            if (!options.prefer_min_crossings) break;
        } else {
            lp_free_pdcode(&pd);
        }
    }

    if (!have_best) {
        set_error(error, error_size, "could not find a generic projection");
        return 0;
    }
    *out = best;
    return 1;
}

int lp_format_pdcode(const lp_pdcode* pd, char* buffer, size_t buffer_size) {
    size_t used = 0;
    size_t i;
    int n;
    if (!pd || !buffer || buffer_size == 0) return -1;
    n = snprintf(buffer + used, buffer_size - used, "[");
    if (n < 0 || (size_t)n >= buffer_size - used) return -1;
    used += (size_t)n;
    for (i = 0; i < pd->count; ++i) {
        const lp_crossing* c = &pd->crossings[i];
        n = snprintf(buffer + used, buffer_size - used, "%s[%d, %d, %d, %d]",
                     i ? ", " : "", c->a[0], c->a[1], c->a[2], c->a[3]);
        if (n < 0 || (size_t)n >= buffer_size - used) return -1;
        used += (size_t)n;
    }
    n = snprintf(buffer + used, buffer_size - used, "]");
    if (n < 0 || (size_t)n >= buffer_size - used) return -1;
    return (int)(used + (size_t)n);
}

int lp_validate_pdcode(const lp_pdcode* pd) {
    int* counts;
    size_t i;
    size_t nlabels;
    if (!pd) return 0;
    if (pd->count == 0) return 1;
    nlabels = pd->count * 2;
    counts = (int*)calloc(nlabels + 1, sizeof(*counts));
    if (!counts) return 0;
    for (i = 0; i < pd->count; ++i) {
        int j;
        for (j = 0; j < 4; ++j) {
            int label = pd->crossings[i].a[j];
            if (label <= 0 || (size_t)label > nlabels) {
                free(counts);
                return 0;
            }
            counts[label] += 1;
        }
    }
    for (i = 1; i <= nlabels; ++i) {
        if (counts[i] != 2) {
            free(counts);
            return 0;
        }
    }
    free(counts);
    return 1;
}
