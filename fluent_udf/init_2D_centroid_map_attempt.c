#include "udf.h"
#include <stdio.h>
#include <math.h>

#define CSV_FILE "Finaluds.txt"
#define N 10000

float bfield_data[N][3]; // [x, y, B]
int num_points = 0;

DEFINE_INIT(init_bfield, domain)
{
    FILE *fp = fopen(CSV_FILE, "r");
    if (!fp) {
        Message("ERROR: Failed to open %s\n", CSV_FILE);
        return;
    }

    float x, y, B;
    num_points = 0;
    while ((fscanf(fp, "%f	%f	%f", &x, &y, &B) == 3 && != EOF) && num_points < N) {
        bfield_data[num_points][0] = x;
        bfield_data[num_points][1] = y;
        bfield_data[num_points][2] = B;
        num_points++;
    }
    fclose(fp);
    Message("Loaded %d B-field points from file.\n", num_points);

    /* Assign nearest B to UDS[0] */
    Thread *t;
    cell_t c;
    thread_loop_c(t, domain) {
        begin_c_loop(c, t) {
            real xc[ND_ND];
            C_CENTROID(xc, c, t);
            float min_dist = 10e9;
            float B_nearest = 0.0;

            for (int i = 0; i < num_points; i++) {
                float dx = xc[0] - bfield_data[i][0];
                float dy = xc[1] - bfield_data[i][1];
                float dist = dx*dx + dy*dy;
                if (dist < min_dist) {
                    min_dist = dist;
                    B_nearest = bfield_data[i][2];
                }
            }
            C_UDSI(c, t, 0) = B_nearest;
        }
        end_c_loop(c, t)
    }
}
