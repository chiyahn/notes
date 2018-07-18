

```julia
using Interpolations
using Base.Test
using Base.Cartesian

# convenient constructors
LinearInterpolation(ranges::NTuple{N,T}, vs) where {N,T <: Range} = extrapolate(scale(interpolate(vs, BSpline(Linear()), OnGrid()), ranges...),  Interpolations.Throw())
LinearInterpolation(ranges::NTuple{N,T}, vs) where {N,T <: AbstractArray} = extrapolate(interpolate(ranges, vs, Gridded(Linear())),  Interpolations.Throw())
CubicSplineInterpolation(ranges::NTuple{N,T}, vs) where {N,T <: Range} = extrapolate(scale(interpolate(vs, BSpline(Cubic(Line())), OnGrid()), ranges...),  Interpolations.Throw())

# unit test setup
XMIN = 2
XMAX = 10
YMIN = 1
YMAX = 8
ΔX = .1
ΔY = .5
XLEN = convert(Integer, floor((XMAX - XMIN)/ΔX) + 1)
YLEN = convert(Integer, floor((YMAX - YMIN)/ΔY) + 1)
```




    15




```julia
@testset "1d-interpolations" begin
    @testset "1d-regular-grids" begin
        xs = XMIN:ΔX:XMAX
        f(x) = log(x)
        A = [f(x) for x in xs]
        interp = LinearInterpolation((xs, ), A)

        @test interp[XMIN] ≈ f(XMIN)
        @test interp[XMAX] ≈ f(XMAX)
        @test interp[XMIN + ΔX] ≈ f(XMIN + ΔX)
        @test interp[XMAX - ΔX] ≈ f(XMAX - ΔX)
        @test interp[XMIN + ΔX / 2] ≈ f(XMIN + ΔX / 2) atol=.1 
        @test_throws BoundsError interp[XMIN - ΔX / 2]
        @test_throws BoundsError interp[XMAX + ΔX / 2]
    end

    @testset "1d-regular-grids-cubic" begin
        xs = XMIN:ΔX:XMAX
        f(x) = log(x)
        A = [f(x) for x in xs]
        interp = CubicSplineInterpolation((xs, ), A)

        @test interp[XMIN] ≈ f(XMIN)
        @test interp[XMAX] ≈ f(XMAX)
        @test interp[XMIN + ΔX] ≈ f(XMIN + ΔX)
        @test interp[XMAX - ΔX] ≈ f(XMAX - ΔX)
        @test interp[XMIN + ΔX / 2] ≈ f(XMIN + ΔX / 2) atol=.1 
        @test_throws BoundsError interp[XMIN - ΔX / 2]
        @test_throws BoundsError interp[XMAX + ΔX / 2]
    end

    @testset "1d-irregular-grids" begin
        xs = [x^2 for x in XMIN:ΔX:XMAX]
        xmin = xs[1]
        xmax = xs[XLEN]
        f(x) = log(x)
        A = [f(x) for x in xs]
        interp = LinearInterpolation((xs, ), A)

        @test interp[xmin] ≈ f(xmin)
        @test interp[xmax] ≈ f(xmax)
        @test interp[xs[2]] ≈ f(xs[2])
        @test interp[xmin + ΔX / 2] ≈ f(xmin + ΔX / 2) atol=.1
        @test_throws BoundsError interp[xmin - ΔX / 2]
        @test_throws BoundsError interp[xmax + ΔX / 2]
    end
end
```

    [1m[37mTest Summary:     | [39m[22m[1m[32mPass  [39m[22m[1m[36mTotal[39m[22m
    1d-interpolations | [32m  20  [39m[36m   20[39m





    Base.Test.DefaultTestSet("1d-interpolations", Any[Base.Test.DefaultTestSet("1d-regular-grids", Any[], 7, false), Base.Test.DefaultTestSet("1d-regular-grids-cubic", Any[], 7, false), Base.Test.DefaultTestSet("1d-irregular-grids", Any[], 6, false)], 0, false)




```julia
@testset "2d-interpolations" begin
    @testset "2d-regular-grids" begin
        xs = XMIN:ΔX:XMAX
        ys = YMIN:ΔY:YMAX
        f(x, y) = log(x+y)
        A = [f(x,y) for x in xs, y in ys]
        interp = LinearInterpolation((xs, ys), A)

        @test interp[XMIN,YMIN] ≈ f(XMIN,YMIN)
        @test interp[XMIN,YMAX] ≈ f(XMIN,YMAX)
        @test interp[XMAX,YMIN] ≈ f(XMAX,YMIN)
        @test interp[XMAX,YMAX] ≈ f(XMAX,YMAX)
        @test interp[XMIN + ΔX,YMIN] ≈ f(XMIN + ΔX,YMIN)
        @test interp[XMIN,YMIN + ΔY] ≈ f(XMIN,YMIN + ΔY)
        @test interp[XMIN + ΔX,YMIN + ΔY] ≈ f(XMIN + ΔX,YMIN + ΔY)
        @test interp[XMIN + ΔX / 2,YMIN + ΔY / 2] ≈ f(XMIN + ΔX / 2,YMIN + ΔY / 2) atol=.1
        @test_throws BoundsError interp[XMIN - ΔX / 2,YMIN - ΔY / 2]
        @test_throws BoundsError interp[XMIN - ΔX / 2,YMIN + ΔY / 2]
        @test_throws BoundsError interp[XMIN + ΔX / 2,YMIN - ΔY / 2]
        @test_throws BoundsError interp[XMAX + ΔX / 2,YMAX + ΔY / 2]
    end

    @testset "2d-regular-grids-cubic" begin
        xs = XMIN:ΔX:XMAX
        ys = YMIN:ΔY:YMAX
        f(x, y) = log(x+y)
        A = [f(x,y) for x in xs, y in ys]
        interp = CubicSplineInterpolation((xs, ys), A)

        @test interp[XMIN,YMIN] ≈ f(XMIN,YMIN)
        @test interp[XMIN,YMAX] ≈ f(XMIN,YMAX)
        @test interp[XMAX,YMIN] ≈ f(XMAX,YMIN)
        @test interp[XMAX,YMAX] ≈ f(XMAX,YMAX)
        @test interp[XMIN + ΔX,YMIN] ≈ f(XMIN + ΔX,YMIN)
        @test interp[XMIN,YMIN + ΔY] ≈ f(XMIN,YMIN + ΔY)
        @test interp[XMIN + ΔX,YMIN + ΔY] ≈ f(XMIN + ΔX,YMIN + ΔY)
        @test interp[XMIN + ΔX / 2,YMIN + ΔY / 2] ≈ f(XMIN + ΔX / 2,YMIN + ΔY / 2) atol=.1
        @test_throws BoundsError interp[XMIN - ΔX / 2,YMIN - ΔY / 2]
        @test_throws BoundsError interp[XMIN - ΔX / 2,YMIN + ΔY / 2]
        @test_throws BoundsError interp[XMIN + ΔX / 2,YMIN - ΔY / 2]
        @test_throws BoundsError interp[XMAX + ΔX / 2,YMAX + ΔY / 2]
    end

    @testset "2d-irregular-grids" begin
        xs = [x^2 for x in XMIN:ΔX:XMAX]
        ys = [y^2 for y in YMIN:ΔY:YMAX]
        xmin = xs[1]
        xmax = xs[XLEN]
        ymin = ys[1]
        ymax = ys[YLEN]
        f(x, y) = log(x+y)
        A = [f(x,y) for x in xs, y in ys]
        interp = LinearInterpolation((xs, ys), A)

        @test interp[xmin,ymin] ≈ f(xmin,ymin)
        @test interp[xmin,ymax] ≈ f(xmin,ymax)
        @test interp[xmax,ymin] ≈ f(xmax,ymin)
        @test interp[xmax,ymax] ≈ f(xmax,ymax)
        @test interp[xs[2],ymin] ≈ f(xs[2],ymin)
        @test interp[xmin,ys[2]] ≈ f(xmin,ys[2])
        @test interp[xs[2],ys[2]] ≈ f(xs[2],ys[2])
        @test interp[xmin + ΔX / 2,ymin + ΔY / 2] ≈ f(xmin + ΔX / 2,ymin + ΔY / 2) atol=.1
        @test_throws BoundsError interp[xmin - ΔX / 2,ymin - ΔY / 2]
        @test_throws BoundsError interp[xmin - ΔX / 2,ymin + ΔY / 2]
        @test_throws BoundsError interp[xmin + ΔX / 2,ymin - ΔY / 2]
        @test_throws BoundsError interp[xmax + ΔX / 2,ymax + ΔY / 2]
    end
end
```

    [1m[37mTest Summary:     | [39m[22m[1m[32mPass  [39m[22m[1m[36mTotal[39m[22m
    2d-interpolations | [32m  36  [39m[36m   36[39m





    Base.Test.DefaultTestSet("2d-interpolations", Any[Base.Test.DefaultTestSet("2d-regular-grids", Any[], 12, false), Base.Test.DefaultTestSet("2d-regular-grids-cubic", Any[], 12, false), Base.Test.DefaultTestSet("2d-irregular-grids", Any[], 12, false)], 0, false)


