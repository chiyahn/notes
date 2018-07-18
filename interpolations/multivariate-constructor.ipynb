

```julia
using Interpolations
using Base.Test
using Base.Cartesian

# convenient constructors
LinearInterp(ranges::NTuple{N,T}, vs) where {N,T <: Range} = scale(interpolate(vs, BSpline(Linear()), OnGrid()), ranges...)
LinearInterp(ranges::NTuple{N,T}, vs) where {N,T <: AbstractArray} = interpolate(ranges, vs, Gridded(Linear()))

# unit test setup
XMIN = 1
XMAX = 5
YMIN = 1
YMAX = 8
ΔX = .1
ΔY = .5
XLEN = convert(Integer, floor((XMAX - XMIN)/ΔX) + 1)
YLEN = convert(Integer, floor((YMAX - YMIN)/ΔY) + 1)
```




    15




```julia
## 1D cases
# regular grids
xs = XMIN:ΔX:XMAX
ys = YMIN:ΔY:YMAX
f(x) = log(x)
A = [f(x) for x in xs]
interp = LinearInterp((xs, ), A)

@test interp[XMIN] ≈ f(XMIN)
@test interp[XMAX] ≈ f(XMAX)
@test interp[XMIN + ΔX] ≈ f(XMIN + ΔX)
@test interp[XMAX - ΔX] ≈ f(XMAX - ΔX)
@test interp[XMIN + ΔX / 2] ≈ f(XMIN + ΔX / 2) atol=.1

# irregular grids
xs = [x^2 for x in XMIN:ΔX:XMAX]
xmin = xs[1]
xmax = xs[XLEN]
f(x) = log(x)
A = [f(x) for x in xs]
interp = LinearInterp((xs, ), A)

@test interp[xmin] ≈ f(xmin)
@test interp[xmax] ≈ f(xmax)
@test interp[xs[2]] ≈ f(xs[2])
@test interp[xmin + ΔX / 2] ≈ f(xmin + ΔX / 2) atol=.1
```




    [1m[32mTest Passed[39m[22m




```julia
## 2D cases
# regular grids
xs = XMIN:ΔX:XMAX
ys = YMIN:ΔY:YMAX
f(x, y) = log(x+y)
A = [f(x,y) for x in xs, y in ys]
interp = LinearInterp((xs, ys), A)

@test interp[XMIN,YMIN] ≈ f(XMIN,YMIN)
@test interp[XMIN,YMAX] ≈ f(XMIN,YMAX)
@test interp[XMAX,YMIN] ≈ f(XMAX,YMIN)
@test interp[XMAX,YMAX] ≈ f(XMAX,YMAX)
@test interp[XMIN + ΔX,YMIN] ≈ f(XMIN + ΔX,YMIN)
@test interp[XMIN,YMIN + ΔY] ≈ f(XMIN,YMIN + ΔY)
@test interp[XMIN + ΔX,YMIN + ΔY] ≈ f(XMIN + ΔX,YMIN + ΔY)
@test interp[XMIN + ΔX / 2,YMIN + ΔY / 2] ≈ f(XMIN + ΔX / 2,YMIN + ΔY / 2) atol=.1

# irregular grids
xs = [x^2 for x in XMIN:ΔX:XMAX]
ys = [y^2 for y in YMIN:ΔY:YMAX]
xmin = xs[1]
xmax = xs[XLEN]
ymin = ys[1]
ymax = ys[YLEN]
f(x, y) = log(x+y)
A = [f(x,y) for x in xs, y in ys]
interp = LinearInterp((xs, ys), A)

@test interp[xmin,ymin] ≈ f(xmin,ymin)
@test interp[xmin,ymax] ≈ f(xmin,ymax)
@test interp[xmax,ymin] ≈ f(xmax,ymin)
@test interp[xmax,ymax] ≈ f(xmax,ymax)
@test interp[xs[2],ymin] ≈ f(xs[2],ymin)
@test interp[xmin,ys[2]] ≈ f(xmin,ys[2])
@test interp[xs[2],ys[2]] ≈ f(xs[2],ys[2])
@test interp[xmin + ΔX / 2,ymin + ΔY / 2] ≈ f(xmin + ΔX / 2,ymin + ΔY / 2) atol=.1
```




    [1m[32mTest Passed[39m[22m


