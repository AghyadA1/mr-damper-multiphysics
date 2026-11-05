/* Draft UDFs exactly as written in UDF-UDS.docx (2025-08-03).
   Kept for history: Bingham viscosity (DEFINE_PROPERTY), piston motion, 3D nearest-neighbour init,
   and the moving-field DEFINE_ON_DEMAND + DEFINE_ADJUST idea. Not the compiled final versions. */

#include "udf.h"
#define A_CONST 30.0     // Pa/T
#define B_CONST 150.0    // Pa/T^2
#define PLASTIC_VISC 0.02 // Pa·s
DEFINE_PROPERTY(field_dependent_viscosity, c, t)
{
    real B = C_UDSI(c, t, 0);  // Read B from UDS 0
    real shear_rate = C_STRAIN_RATE_MAG(c, t);  // Shear rate
    real tau_y = A_CONST * B + B_CONST * B * B;
    if (shear_rate < 1e-6)
        shear_rate = 1e-6;  // Avoid division by zero
    return tau_y / shear_rate + PLASTIC_VISC;
}
#include "udf.h"
#define AMP 0.01    // Amplitude [m]
#define FREQ 2.0    // Frequency [Hz]
#define OMEGA (2.0 * M_PI * FREQ)
DEFINE_CG_MOTION(piston_motion, dt, cg_vel, cg_omega, time, dtime)
{
    cg_vel[0] = 0.0;
    cg_vel[1] = AMP * OMEGA * cos(OMEGA * time);  // Velocity in Y-direction
    cg_omega[2] = 0.0;
}
#include "udf.h"
DEFINE_INIT(init_bfield, domain)
{
    Thread *t;
    cell_t c;
    FILE *fp = fopen("bfield_data.txt", "r");
    real x[ND_ND], b_value, file_x, file_y, file_z, file_b;
    real min_dist, dist;
    int i, n_points = 10000;  // Adjust based on number of centroids
    real *coords = (real *)malloc(n_points * 3 * sizeof(real));
    real *b_values = (real *)malloc(n_points * sizeof(real));
    /* Read B-field data */
    if (fp != NULL)
    {
        for (i = 0; i < n_points; i++)
        {
            fscanf(fp, "%lf %lf %lf %lf", &file_x, &file_y, &file_z, &file_b);
            coords[i * 3] = file_x;
            coords[i * 3 + 1] = file_y;
            coords[i * 3 + 2] = file_z;
            b_values[i] = file_b;
        }
        fclose(fp);
    }
    /* Assign B-field to cells */
    thread_loop_c(t, domain)
    {
        begin_c_loop(c, t)
        {
            C_CENTROID(x, c, t);
            min_dist = 1e10;
            b_value = 0.0;
            /* Find nearest neighbor */
            for (i = 0; i < n_points; i++)
            {
                dist = sqrt(pow(x[0] - coords[i * 3], 2) +
                            pow(x[1] - coords[i * 3 + 1], 2) +
                            pow(x[2] - coords[i * 3 + 2], 2));
                if (dist < min_dist)
                {
                    min_dist = dist;
                    b_value = b_values[i];
                }
            }
            C_UDSI(c, t, 0) = b_value;  // Assign to UDS-0
        }
        end_c_loop(c, t)
    }
    free(coords);
    free(b_values);
}
#include "udf.h"
/* Global arrays to store B-field data */
static real *coords = NULL;
static real *b_values = NULL;
static int n_points = 0;
static int initialized = 0;
DEFINE_ON_DEMAND(read_bfield_data)
{
    FILE *fp = fopen("bfield_data_relative.txt", "r");
    real file_x, file_y_rel, file_z, file_b;
    int i;
    if (fp == NULL)
    {
        Message("Error: Could not open bfield_data_relative.txt\n");
        return;
    }
    /* Count number of points */
    n_points = 0;
    while (fscanf(fp, "%lf %lf %lf %lf", &file_x, &file_y_rel, &file_z, &file_b) == 4)
        n_points++;
    rewind(fp);
    /* Allocate memory */
    coords = (real *)malloc(n_points * 3 * sizeof(real));
    b_values = (real *)malloc(n_points * sizeof(real));
    /* Read data */
    for (i = 0; i < n_points; i++)
    {
        fscanf(fp, "%lf %lf %lf %lf", &file_x, &file_y_rel, &file_z, &file_b);
        coords[i * 3] = file_x;
        coords[i * 3 + 1] = file_y_rel;
        coords[i * 3 + 2] = file_z;
        b_values[i] = file_b;
    }
    fclose(fp);
    initialized = 1;
    Message("B-field data loaded: %d points\n", n_points);
}
DEFINE_ADJUST(update_bfield, domain)
{
    Thread *t;
    cell_t c;
    real x[ND_ND], y_relative, piston_pos, min_dist, dist, b_value;
    real amplitude = 0.01;  // Amplitude in meters (match Step 1)
    real frequency = 1.0;   // Frequency in Hz (match Step 1)
    real omega = 2.0 * M_PI * frequency;
    int i;
    if (!initialized)
    {
        Message("Error: B-field data not loaded. Run read_bfield_data first.\n");
        return;
    }
    /* Calculate current piston position */
    piston_pos = amplitude * sin(omega * CURRENT_TIME);
    /* Update B-field for each cell */
    thread_loop_c(t, domain)
    {
        begin_c_loop(c, t)
        {
            C_CENTROID(x, c, t);  // Get current cell centroid
            y_relative = x[1] - piston_pos;  // Relative y-position
            /* Find nearest neighbor */
            min_dist = 1e10;
            b_value = 0.0;
            for (i = 0; i < n_points; i++)
            {
                dist = sqrt(pow(x[0] - coords[i * 3], 2) +
                            pow(y_relative - coords[i * 3 + 1], 2) +
                            pow(x[2] - coords[i * 3 + 2], 2));
                if (dist < min_dist)
                {
                    min_dist = dist;
                    b_value = b_values[i];
                }
            }
            C_UDSI(c, t, 0) = b_value;  // Assign to UDS-0
        }
        end_c_loop(c, t)
    }
}
