import math
import time

theta_spacing = 0.07
phi_spacing = 0.02

screen_width = 32
screen_height = 32

R1 = 1
R2 = 2
K2 = 5
# Calculate K1 based on screen size: the maximum x-distance occurs
# roughly at the edge of the torus, which is at x=R1+R2, z=0.  which
# would be displaced 3/8ths of the width of the screen, which
# is 3/4th of the way from the center to the side of the screen.
# screen_width*3/8 = K1*(R1+R2)/(K2+0)
# screen_width*K2*3/(8*(R1+R2)) = K1
K1 = screen_width*K2*3/(8*(R1+R2))

def render_frame(A, B):
    # precompute sines and cosines of A and B
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    output = [[ ' ' for i in range(screen_height)] for j in range(screen_width)]
    zbuffer = [[ 0 for i in range(screen_height)] for j in range(screen_width)]

    # theta goes around the cross-sectional circle of a torus
    theta = 0
    while (theta < 2 * math.pi):
        theta += theta_spacing
        # precompute sines and cosines of theta
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        # phi goes around the center of revolution of a torus
        phi = 0
        while (phi < 2 * math.pi):
            phi += phi_spacing
            # precompute sines and cosines of phi
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            # the x,y coordinate of the circle, before revolving (factored
            # out of the above equations)
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # final 3D (x,y,z) coordinate after rotations, directly from
            # our math above
            x = circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB
            y = circlex*(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB
            z = K2 + cosA*circlex*sinphi + circley*sinA
            ooz = 1/z  # "one over z"

            # x and y projection.  note that y is negated here, because y
            # goes up in 3D space but down on 2D displays.
            xp = int(screen_width/2 + K1*ooz*x)
            yp = int(screen_height/2 - K1*ooz*y)

            # calculate luminance.  ugly, but correct.
            L = (cosphi*costheta*sinB - cosA*costheta*sinphi - sinA*sintheta
                + cosB*(cosA*sintheta - costheta*sinA*sinphi))

            # L ranges from -sqrt(2) to +sqrt(2).  If it's < 0, the surface
            # is pointing away from us, so we won't bother trying to plot it.
            # and if L = 0, it has no luminance hence it is not plotted.
            if L > 0:
                # test against the z-buffer.  larger 1/z means the pixel is
                # closer to the viewer than what's already plotted.
                if ooz > zbuffer[xp][yp]:
                    zbuffer[xp][yp] = ooz
                    luminance_index = int(L*8)
                    # luminance_index is now in the range 0..11 (8*sqrt(2) = 11.3)
                    # now we lookup the character corresponding to the
                    # luminance and plot it in our output:
                    output[xp][yp] = ".,-~:;=!*#$@"[luminance_index]


    # now, dump output[] to the screen.
    # bring cursor to "home" location, in just about any currently-used
    # terminal emulation mode
    print()
    for j in range(screen_height):
        print(" " * 14, end="")
        for i in range(screen_width):
            print(output[i][j], end="")
        print("\n", end="")
    print()


A = 1.0
B = 1.0
for _ in range(1000):
    render_frame(A, B)
    time.sleep(0.05)
    A += 0.07
    B += 0.02
