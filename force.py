def force(f, potEn):
    f[:] = 0
    potEn = 0
    for i in range(N_part - 1):
        for j in range(i + 1, N_part):
            xr = x[i] - x[j]
            yr = y[i] - y[j]
            zr = z[i] - z[j]
            xr -= box*round(xr/box)
            yr -= box*round(yr/box)
            zr -= box*round(zr/box)
            x2 = xr**2
            y2 = yr**2
            z2 = zr**2
            if x2 < xc && y2 < yc && z2 < zc:
                x2i = 1/x2
                y2i = 1/y2
                z2i = 1/z2
                x6i = x2i**3
                y6i = y2i**3
                z6i = z2i**3
                ff = 48*(x2i + y2i + z2i)*(x6i + y6i + z6i)*(x6i + y6i + z6i - 1.5)
                f(i) += ff*(xr + yr + zr)
                f(j) -= ff*(xr + yr + zr)
                potEnCut = 4*(1/(xc**6 + yc**6 + zc**6) - 1/(xc**3 + yc**3 + zc**3))
                potEn += 4*(x6i + y6i + z6i)*(x6i + y6i + z6i - 3) - potEnCut
    return f, potEn
