#include <math.h>
#include <stdio.h>
#include <assert.h>
#include <time.h>
#include <stdlib.h>

#define BUFFER_PRINT_SIZE 1024

#ifndef DEBUG_ASSERT
# define DEBUG_ASSERT(expr) assert(expr)
#endif


// to mark extern if not implementation
#ifdef VEC2_IMPLEMENTATION
# define V2_GLOBAL_VARABLE
#else
# define V2_GLOBAL_VARABLE extern
#endif

#ifndef VEC2_H
# define VEC2_H


typedef struct 
{
    float x,y;
} Vec2;

V2_GLOBAL_VARABLE char print_buffer[BUFFER_PRINT_SIZE];
V2_GLOBAL_VARABLE int print_buffer_size;
V2_GLOBAL_VARABLE Vec2 null_vec2;

static inline float v2_dot_prod(const Vec2 a, const Vec2 b)
{
    DEBUG_ASSERT(!isnan(a.x));
    DEBUG_ASSERT(!isnan(a.y));
    DEBUG_ASSERT(!isnan(b.x));
    DEBUG_ASSERT(!isnan(b.y));
    float res = a.x * b.x + a.y * b.y;
    DEBUG_ASSERT(!isnan(res));
    return (res);
}
static inline Vec2 v2_add(const Vec2 a, const Vec2 b)
{
    DEBUG_ASSERT(!isnan(a.x));
    DEBUG_ASSERT(!isnan(a.y));
    DEBUG_ASSERT(!isnan(b.x));
    DEBUG_ASSERT(!isnan(b.y));
    Vec2 res = (Vec2){a.x + b.x, a.y + b.y};
    DEBUG_ASSERT(!isnan(res.x));
    DEBUG_ASSERT(!isnan(res.y));
    return (res);
}
static inline Vec2 v2_diff(const Vec2 a, const Vec2 b)
{ 
    DEBUG_ASSERT(!isnan(a.x));
    DEBUG_ASSERT(!isnan(a.y));
    DEBUG_ASSERT(!isnan(b.x));
    DEBUG_ASSERT(!isnan(b.y));
    Vec2 res = (Vec2){a.x - b.x, a.y - b.y};
    DEBUG_ASSERT(!isnan(res.x));
    DEBUG_ASSERT(!isnan(res.y));
    return (res);
}
static inline float v2_lenght(const Vec2 a)
{
    DEBUG_ASSERT(!isnan(a.x));
    DEBUG_ASSERT(!isnan(a.y));
    DEBUG_ASSERT(a.x * a.x + a.y * a.y >= 0.);
    float res = sqrt(a.x * a.x + a.y * a.y);
    DEBUG_ASSERT(!isnan(res));
    return (res);
}
static inline float v2_dist(const Vec2 a, const Vec2 b)
{
    DEBUG_ASSERT(!isnan(a.x));
    DEBUG_ASSERT(!isnan(a.y));
    DEBUG_ASSERT(!isnan(b.x));
    DEBUG_ASSERT(!isnan(b.y));
    float res = v2_lenght(v2_diff(b, a));
    DEBUG_ASSERT(!isnan(res));
    return (res);
}
static inline Vec2 v2_scal_prod(const float lambda, const Vec2 v)
{
    DEBUG_ASSERT(!isnan(lambda));
    DEBUG_ASSERT(!isnan(v.x));
    DEBUG_ASSERT(!isnan(v.y));
    Vec2 res = (Vec2){lambda * v.x, lambda * v.y};
    DEBUG_ASSERT(!isnan(res.x));
    DEBUG_ASSERT(!isnan(res.y));
    return (res);
}
static inline Vec2 v2_normalize(const Vec2 v)
{
    DEBUG_ASSERT(!isnan(v.x));
    DEBUG_ASSERT(!isnan(v.y));
    // DEBUG_ASSERT(v2_lenght(v) != 0.);
    float lenght = v2_lenght(v);
    if (lenght == 0.)   
        return (Vec2){0., 1.}; 
    Vec2 res = v2_scal_prod(1./lenght, v);
    DEBUG_ASSERT(!isnan(res.x));
    DEBUG_ASSERT(!isnan(res.y));
    return (res);
}


static inline char *v2_sprint(const Vec2 v)
{
    assert(print_buffer_size + 4+2*10 < BUFFER_PRINT_SIZE);

    char *res = &print_buffer[print_buffer_size];
    print_buffer_size += sprintf(res, "(%.2f,%.2f)", v.x, v.y) + 1 /* '\0' */; 
    
    return (res);
}

// rand in [a, b]
static inline Vec2 v2_rand(float a, float b)
{
    DEBUG_ASSERT(!isnan(b-a));
    return (Vec2){
        a + (float)rand()/(float)((float)RAND_MAX/(b-a)),
        a + (float)rand()/(float)((float)RAND_MAX/(b-a))
    };
}

#endif /* VEC2_H */