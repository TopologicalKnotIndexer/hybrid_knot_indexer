#include "link_pdcode.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void usage(FILE* out) {
    fprintf(out,
            "Usage: link-pdcode [--direction X Y Z] [--attempts N] [--first-projection] [--epsilon EPS]\n"
            "Reads: n followed by n lines of x y z coordinates on stdin.\n");
}

int main(int argc, char** argv) {
    lp_options options;
    lp_point3* points = NULL;
    lp_pdcode pd = {0};
    char error[512];
    size_t n;
    size_t i;
    int printed;
    size_t buffer_size;
    char* buffer = NULL;

    lp_default_options(&options);
    for (i = 1; i < (size_t)argc; ++i) {
        if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            usage(stdout);
            return 0;
        } else if (strcmp(argv[i], "--attempts") == 0) {
            if (++i >= (size_t)argc) {
                fprintf(stderr, "--attempts needs a value\n");
                return 2;
            }
            options.max_attempts = atoi(argv[i]);
        } else if (strcmp(argv[i], "--epsilon") == 0) {
            if (++i >= (size_t)argc) {
                fprintf(stderr, "--epsilon needs a value\n");
                return 2;
            }
            options.epsilon = atof(argv[i]);
        } else if (strcmp(argv[i], "--first-projection") == 0) {
            options.prefer_min_crossings = 0;
        } else if (strcmp(argv[i], "--direction") == 0) {
            if (i + 3 >= (size_t)argc) {
                fprintf(stderr, "--direction needs X Y Z\n");
                return 2;
            }
            options.use_direction = 1;
            options.direction.x = atof(argv[++i]);
            options.direction.y = atof(argv[++i]);
            options.direction.z = atof(argv[++i]);
        } else {
            fprintf(stderr, "unknown option: %s\n", argv[i]);
            return 2;
        }
    }

    if (scanf("%zu", &n) != 1) {
        fprintf(stderr, "failed to read point count\n");
        return 2;
    }
    points = (lp_point3*)calloc(n ? n : 1, sizeof(*points));
    if (!points) {
        fprintf(stderr, "out of memory\n");
        return 2;
    }
    for (i = 0; i < n; ++i) {
        if (scanf("%lf%lf%lf", &points[i].x, &points[i].y, &points[i].z) != 3) {
            fprintf(stderr, "failed to read point %zu\n", i);
            free(points);
            return 2;
        }
    }

    if (!lp_compute_pdcode(points, n, &options, &pd, error, sizeof(error))) {
        fprintf(stderr, "%s\n", error);
        free(points);
        return 1;
    }
    if (!lp_validate_pdcode(&pd)) {
        fprintf(stderr, "internal error: generated invalid PD code\n");
        lp_free_pdcode(&pd);
        free(points);
        return 1;
    }

    buffer_size = pd.count * 64 + 8;
    buffer = (char*)calloc(buffer_size, 1);
    if (!buffer) {
        fprintf(stderr, "out of memory\n");
        lp_free_pdcode(&pd);
        free(points);
        return 2;
    }
    printed = lp_format_pdcode(&pd, buffer, buffer_size);
    if (printed < 0) {
        fprintf(stderr, "failed to format PD code\n");
        free(buffer);
        lp_free_pdcode(&pd);
        free(points);
        return 1;
    }
    printf("%s\n", buffer);

    free(buffer);
    lp_free_pdcode(&pd);
    free(points);
    return 0;
}
