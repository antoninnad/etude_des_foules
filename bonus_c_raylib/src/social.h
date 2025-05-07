// std
#include <math.h>
#include <stdlib.h>
#include <inttypes.h>
#include <stdio.h>
#include <time.h>
#include <pthread.h>
#include <signal.h>


// raylib
#include "raylib.h"
#include "raygui.h"
#include "rlgl.h"




// perso
#ifdef DEBUG
# define RUN_TIME_ASSERT
# define DEBUG_ASSERT(expr) ((expr) ? (void)0 : (void)raise(SIGABRT))
// # define DEBUG_ASSERT(expr) assert(expr)
#else
# define DEBUG_ASSERT(expr)
#endif

#ifdef RUN_TIME_ASSERT
# define DA_ASSERT DEBUG_ASSERT
#endif /* RUN_TIME_ASSERT */

#include "da.h"
#include "vec2.h"
#include "gui.h"

// to mark extern if not implementation
#ifdef SOCIAL_IMPLEMENTATION
# define SO_GLOBAL_VARABLE
#else
# define SO_GLOBAL_VARABLE extern
#endif

SO_GLOBAL_VARABLE char print_buffer[BUFFER_PRINT_SIZE];
SO_GLOBAL_VARABLE int print_buffer_size;



// conpilation config :
#ifdef KUTTA2
# define WINDOWNAME "KUTTA2 physique simulation"
#else
# define WINDOWNAME "EULER physique simulation"
#endif




// Macros:

// any vec type .x .y -> .x .y
// use :  (NEW_V2)V2_TO_V2(v)
#define V2_TO_V2(v) {v.x, v.y}


#define min(a, b) ((a) < (b) ? (a) : (b))
#define max(a, b) ((a) > (b) ? (a) : (b))

#define Sprintf(...) (printf(__VA_ARGS__), print_buffer_size = 0)

#define DrawTextF(format, x, y, font_size, color, ...)\
(\
    print_buffer_size += sprintf(print_buffer, format, __VA_ARGS__),\
    DrawText(print_buffer, x, y, font_size, color),\
    print_buffer_size = 0\
)

typedef struct _TIME {
    clock_t s;
    int i;
} _TIME;

#define TIME(res) \
for (struct _TIME obj = { .i = 0, .s = clock()};\
    obj.i < 1;\
    (++obj.i, (res) = (clock() - obj.s))\
)
#define TIME_CLOCK_TO_MILISEC(t) ( (double)((double)(t) * 1000. / (double)CLOCKS_PER_SEC) )

// from CLAY render raylib
#define CLAY_RECTANGLE_TO_RAYLIB_RECTANGLE(rectangle) (Rectangle) { .x = rectangle.x, .y = rectangle.y, .width = rectangle.width, .height = rectangle.height }



// structs:

typedef struct Personne
{
    int back_step;   // tick to go backward
    Vec2 pos;        // x
    Vec2 speed;      // v
    Vec2 wish_dir;   // e^0
    float wish_speed;// v^0
    float tau;       // \tau
    float mass;      // m
    float radius;    // r
    float wish_dist; // B
    Vec2 (*fild)(Vec2);
    Color color;
} Personne;
DA_TYPEDEF_ARRAY(Personne);
DA_TYPEDEF_ARRAY_PTR(Personne); // for Hash_map

typedef struct Wall
{
    Vec2 pos;
    Vec2 len;
    float radius;
} Wall;
DA_TYPEDEF_ARRAY(Wall);



DA_TYPEDEF_ARRAY(da_ptr_Personne);
typedef struct Hash_map
{
    float ratio; // cell in map by dist in vir_canvas
    int size;    // 2D but a square
    
    da_ptr_Personne *array; // 1D but virualy 2D (l*w+c) 
    // hash is simply floor func
} Hash_map;


typedef struct Simulation_context
{
    Rectangle render_box;

    int inital_particule_count;

    Rectangle vir_canvas;
    float step;
    int64_t tick;
    double time;
    int step_by_frame;
    float fild_strength;

    bool stoped;
    bool draw_fild_dir;
    bool mode_hash_map;
    enum obstacle_type {
        none = 0,
        circle,
        triangle
    } obstacle;
    
    clock_t simulate_time;
    clock_t gui_reset_time;

    Gui_handel ui;

    // storage
    da_Personne pers;

    // used ref rebuild each tick
    Hash_map map;

    da_Wall walls;

    Vec2 (*fild)(Vec2);
} Simulation_context;
DA_TYPEDEF_ARRAY_PTR(Simulation_context);


typedef struct Window_handel
{
    int target_FPS;    

    clock_t render_time;

    da_ptr_Simulation_context contexts;
} Window_handel;
