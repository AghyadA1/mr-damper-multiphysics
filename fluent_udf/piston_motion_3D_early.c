#include "udf.h"

#define AMP 0.01       // Amplitude (meters)
#define FREQ 2.0       // Frequency (Hz)

DEFINE_CG_MOTION(piston_motion, dt, vel, omega, time, dtime)
{
    real omega_rad = 2.0 * M_PI * FREQ;

    vel[0] = 0.0;
    vel[1] = AMP * omega_rad * cos(omega_rad * time);  // Y-direction motion
    vel[2] = 0.0;

    omega[0] = 0.0;
    omega[1] = 0.0;
    omega[2] = 0.0;
}
