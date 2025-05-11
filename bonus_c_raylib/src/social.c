
#define RAYGUI_IMPLEMENTATION
#define VEC2_IMPLEMENTATION
#define SOCIAL_IMPLEMENTATION
#include "social.h"

const float rad_wall = 0.15;
const float max_speed = 50.;
const Rectangle populate_rect = (Rectangle){ .x=2., .y=2., .width=4.5, .height=6.};

Vec2 fild_door(Vec2);
Personne pe_template = (Personne){
    .pos = (Vec2){0},
    .speed = (Vec2){0., 0.},
    .wish_dir = (Vec2){1., 0.},
    .wish_speed = 0.,
    .tau = .008,
    .mass = 1.,
    .radius = 0., 
    .wish_dist = .01,
    .color = WHITE,
    .fild = fild_door,
    .back_step = 0
};

void print_rect(Rectangle obj)
{
    printf("x%f y%f w%f h%f", obj.x, obj.y, obj.width, obj.height);
}

// point le plus proche de "pos" sur le mur "w"
Vec2 wall_closest_point(const Vec2 pos, const Wall w)
{
    const Vec2 p_w = v2_diff(pos, w.pos); // vector wall_pos -> pos  ; wall_pos: starting point
    const float lenght_len = v2_lenght(w.len);
    if (lenght_len == 0)
        return (w.pos); // mur taille null
    const Vec2 len_nor = v2_scal_prod(1. / lenght_len, w.len);

    float k = v2_dot_prod(p_w, len_nor);

    if (k <= 0)
        return (w.pos);
    if (k >= v2_lenght(w.len))
        return v2_add(w.pos, w.len);
    return v2_add(
        w.pos,
        v2_scal_prod(k, len_nor)
    );
}


int hash_x_Hash_map(const Vec2 pos, const Hash_map *map, Rectangle vir_canvas)
{
    return 1./map->ratio * (pos.x - vir_canvas.x);
}
int hash_y_Hash_map(const Vec2 pos, const Hash_map *map, Rectangle vir_canvas)
{
    return 1./map->ratio * (pos.y - vir_canvas.y);
}


Vec2 force_personne_personne(const Personne *self, const Personne *other)
{
    const float dist_i_s = v2_dist(self->pos, other->pos);

    const float scale = 10. * exp(
        (other->radius + self->radius - dist_i_s)
            / self->wish_dist
    );
    const Vec2 n_i_self = v2_diff(other->pos, self->pos);

    return v2_scal_prod(-scale, n_i_self);
}
Vec2 force_people(const da_Personne *pers, int self_index)
{
    const Personne *self = &da_get(pers, self_index);
    Vec2 res = (Vec2){0., 0.};
    for (int i = 0; i < pers->size; i++) { if (i != self_index)
    {
        float dist_i_s = v2_dist(self->pos, pers->arr[i].pos);
        if (dist_i_s < 1. * pers->arr[i].radius + self->radius)
            res = v2_add(res, force_personne_personne(self, &pers->arr[i]));
    }}
    return (res);
}


Vec2 force_personne_wall(const Personne *self, const Wall *wall)
{
    const Vec2 closest = wall_closest_point(self->pos, *wall);

    const float scale = 10. * exp(
        (wall->radius + self->radius - v2_dist(closest, self->pos))
            / self->wish_dist
    );
    
    const Vec2 n_i_self = v2_normalize(v2_diff(closest, self->pos));

    return v2_scal_prod(-scale, n_i_self);
}
Vec2 force_map_people(const Simulation_context *context, int self_index)
{
    const Personne *self = &da_get(&context->pers, self_index);

    Vec2 res = (Vec2){0., 0.};
    int x = hash_x_Hash_map(self->pos, &context->map, context->vir_canvas);
    int y = hash_y_Hash_map(self->pos, &context->map, context->vir_canvas);
    
    for (int l = -1; l <= 1; l++) if (0 <= y+l && y+l < context->map.size)
    {
        for (int c = -1; c <= 1; c++) if (0 <= x+c && x+c < context->map.size)
        {
            int index = (y+l)*context->map.size + (x+c);
            const da_ptr_Personne *cell_arr = &context->map.array[index];
            
            foreach_ptr (Personne *, perssone, cell_arr) if (self != *perssone)
            {
                res = v2_add(res, force_personne_personne(self, *perssone));
                
            }
        }
    }
    return (res);
}

static inline Vec2 social_acceleration(Simulation_context *context, int self_index, da_Wall *walls)
{
    Personne *self = &(context->pers.arr[self_index]);

    // wish F
    Vec2 socials_F = v2_scal_prod(
        1. / self->tau, 
        v2_diff(
            v2_scal_prod(self->wish_speed, self->wish_dir), 
            self->speed
        )
    );

    // People F
    Vec2 people_F = (Vec2){NAN, NAN};
    if (context->mode_hash_map)
        people_F = force_map_people(context, self_index);
    else people_F = force_people(&context->pers, self_index);
    socials_F = v2_add(socials_F, people_F);

    
    // walls F
    for (int i = 0; i < walls->size; i++)
    {
        socials_F = v2_add(socials_F, force_personne_wall(self, &da_get(walls, i)));
    }
    assert(socials_F.x != NAN);
    assert(socials_F.y != NAN);
    assert(self->mass != 0. || self->mass != -0.);

    return v2_scal_prod(1. / self->mass, socials_F);
}

static inline void kutta2_social(Simulation_context *context, const double step, const int self_index, da_Wall *walls)
{
    da_Personne *pers = &context->pers;
    assert(0 <= self_index && self_index < pers->size);

    const Vec2 acc = social_acceleration(context, self_index, walls);

    const Vec2 k1 = v2_scal_prod(step, acc);
    
    pers->arr[self_index].speed = v2_add(pers->arr[self_index].speed, v2_scal_prod(.5, k1));

    const Vec2 k2 = v2_scal_prod(step, social_acceleration(context, self_index, walls));
    pers->arr[self_index].speed = v2_add(pers->arr[self_index].speed, k2);

    // cap the speed to |v| = max_speed
    if (v2_lenght(pers->arr[self_index].speed) > max_speed)
        pers->arr[self_index].speed = v2_scal_prod(max_speed, v2_normalize(pers->arr[self_index].speed));
    
    // update pos
    pers->arr[self_index].pos = v2_add(
        pers->arr[self_index].pos,
        v2_scal_prod(step, pers->arr[self_index].speed)
    );
}
static inline void euler_social(Simulation_context *context, const double step, const int self_index, da_Wall *walls)
{
    assert(0 <= self_index && self_index < context->pers.size);
    
    Personne *self = &da_get(&context->pers, self_index);

    Vec2 acceleration = social_acceleration(context, self_index, walls);
    


    da_get(&context->pers, self_index).speed = v2_add(
        da_get(&context->pers, self_index).speed,
        v2_scal_prod(
            step,
            acceleration
        )
    );

    da_Personne *pers = &context->pers;

    if (v2_lenght(da_get(pers, self_index).speed) > max_speed)
        da_get(pers, self_index).speed = v2_scal_prod(
            max_speed, v2_normalize(da_get(pers, self_index).speed)
        );

    
    da_get(pers, self_index).pos = v2_add(
        da_get(pers, self_index).pos,
        v2_scal_prod(step, da_get(pers, self_index).speed)
    );
}


#pragma region filds

Vec2 fild_const_down(Vec2 _)
{
    return (Vec2){0., 2.};
}
Vec2 fild_const_right(Vec2 _)
{
    return (Vec2){2., 0.};
}
Vec2 fild_right_mid(Vec2 v)
{
    if (v.y < 5.)
        return (Vec2){2., 1.};
    return (Vec2){2., -1.};
}
Vec2 fild_id(Vec2 v)
{   
    return (v);
}


Vec2 _fild_point(Vec2 v, Vec2 point)
{
    return v2_scal_prod(5., v2_normalize(v2_diff(point, v)));
}
Vec2 fild_door(Vec2 v)
{
    return _fild_point(v, (Vec2){10.5, 5.});
}

Vec2 fild_mouse(Vec2 v)
{
    Vec2 mouse_circle = (Vec2)V2_TO_V2(GetMousePosition());

    mouse_circle.x /= 900. / 10.;
    mouse_circle.y /= 900. / 10.;
    

    return (_fild_point(v, mouse_circle));
}

Vec2 _fild_rotate(Vec2 v, Vec2 point)
{
    return (Vec2){
        point.x - v.y,
        -point.y + v.x
    };
}
Vec2 fild_rotate(Vec2 v)
{
    return _fild_rotate(v, (Vec2){5., 5.});
}
Vec2 _fild_pogo(Vec2 v, Vec2 point)
{
    v = v2_diff(v, point);
    return (Vec2){
        - v.x - v.y,
        - v.y + v.x
    };
}

Vec2 fild_pogo(Vec2 v)
{
    return _fild_pogo(v, (Vec2){5., 5.});
}

Vec2 fild_obstacle(Vec2 v)
{
    Vec2 res = (Vec2){1., 0.};
    if (v.x > 7.)
    {
        if (v.y < 4.3 || v.y > 5.7)
            return (_fild_point(v, (Vec2){8.5, 5.}));
        return (_fild_point(v, (Vec2){11., 5.}));
    }
    return (res);
}

#pragma endregion filds

int is_inside_rect(Vec2 pos, Rectangle rect)
{
    return (rect.x <= pos.x && pos.x <= rect.x + rect.width
         && rect.y <= pos.y && pos.y <= rect.y + rect.height);
}

void wish_update(da_Personne *obj, Vec2 (*fild)(Vec2), const Rectangle green_rect, const float fild_strength)
{
    for (int i = 0; i < obj->size; i++)
    {
        if (!is_inside_rect(obj->arr[i].pos, green_rect))
        {
            da_erase_index(obj, i);
            i--;
        }
        else
        {
            Vec2 fild_wish = obj->arr[i].fild(obj->arr[i].pos);
            obj->arr[i].wish_dir = v2_normalize(fild_wish);
            obj->arr[i].wish_speed = fild_strength;
        }
    }
}

void populate_Personne(da_Personne *pers, int nb_parti)
{
    int axe_count = sqrt((double)nb_parti);
    if (axe_count <= 1)
        axe_count = 2;

   for (int i = 0; i < axe_count; i++)
    {
        const float yratio = (float)i / (float)(axe_count-1);

        for (int j = 0; j < axe_count; j++)
        {
            const float xratio = (float)j / (float)(axe_count-1);
            da_push(pers, pe_template);

            da_top(pers).pos = v2_add(
                (Vec2){
                    2. + xratio * 4.4,
                    2. + yratio * 6.
                },
                v2_rand(-.02,.02)
            );
            da_top(pers).radius = v2_rand(0.2, 0.3).x;
            da_top(pers).color = (Color){
                (unsigned char)v2_rand(10, 236).x,
                (unsigned char)v2_rand(10, 236).x,
                (unsigned char)v2_rand(10, 236).x,
                (unsigned char)255
            };
        }
    }
}

void wall_add_triangle(da_Wall *walls, Vec2 a, Vec2 b, Vec2 c, float radius)
{
    da_push(walls, ((Wall){
        .pos = a,
        .len = v2_diff(b, a),
        .radius = radius
    }));
    da_push(walls, ((Wall){
        .pos = b,
        .len = v2_diff(c, b),
        .radius = radius
    }));
    da_push(walls, ((Wall){
        .pos = c,
        .len = v2_diff(a, c),
        .radius = radius
    }));
}



void add_obstacle(Simulation_context *context, float v)
{
    if (context->obstacle == circle)
    {
        const float s = 2.*rad_wall;
        // push a new one
        da_push(&context->walls, ((Wall){
            .pos = (Vec2){v, 5.},
            .len = (Vec2){0., 0.},
            .7
        }));
    }
    else if (context->obstacle == triangle)
    {
        const float s = 2.*rad_wall;
        // push a new one
        da_push(&context->walls, ((Wall){
            .pos = (Vec2){v + s + 1., 4.},
            .len = (Vec2){0.,         2.},
            rad_wall
        }));
        da_push(&context->walls, ((Wall){
            .pos = (Vec2){v + 1., 4.},
            .len = (Vec2){s, 0.},
            rad_wall
        }));
        da_push(&context->walls, ((Wall){
            .pos = (Vec2){v + 1., 6.},
            .len = (Vec2){s, 0.},
            rad_wall
        }));
        wall_add_triangle(
            &context->walls,
            (Vec2){v + 1.,4.},
            (Vec2){v + 1.,6.},
            (Vec2){v + .3,5.},
            rad_wall
        );
    }
}
void rm_obstacle(Simulation_context *context)
{
    if (context->obstacle == circle)
        da_pop(&context->walls);
    else if (context->obstacle == triangle)
    {
        da_pop(&context->walls);
        da_pop(&context->walls);
        da_pop(&context->walls);
        da_pop(&context->walls);
        da_pop(&context->walls);
        da_pop(&context->walls);
    }
    else assert(false);
}



void populate_Wall(da_Wall *walls, Rectangle vir_canvas)
{
    // door :
    const float Yopen = 1.6;
    const float door_alin = 0.0;
    da_push(walls, ((Wall){
        .pos = (Vec2){vir_canvas.width-1., vir_canvas.height-1.},
        .len = (Vec2){0., door_alin+Yopen-vir_canvas.width*.5},
        .radius = rad_wall
    }));
    da_push(walls, ((Wall){
        .pos = (Vec2){vir_canvas.width-1., 1.},
        .len = (Vec2){0., door_alin+vir_canvas.width*.5-Yopen},
        .radius = rad_wall
    }));


    da_push(walls, ((Wall){
        .pos = (Vec2){1., 1.},
        .len = (Vec2){vir_canvas.width-2., 0.},
        .radius = rad_wall
    }));
    da_push(walls, ((Wall){
        .pos = (Vec2){1., 1.},
        .len = (Vec2){0., vir_canvas.height-2.},
        .radius = rad_wall
    }));
    da_push(walls, ((Wall){
        .pos = (Vec2){vir_canvas.width-1., vir_canvas.height-1.},
        .len = (Vec2){2.-vir_canvas.width, 0.},
        .radius = rad_wall
    }));
}


Hash_map init_Hash_map(float ratio, Rectangle rect)
{
    Hash_map res = {0};

    res.ratio = ratio;

    assert(rect.width == rect.height);

    // check if interger
    DEBUG_ASSERT((int)(rect.width / ratio) != (int)(rect.width / ratio - 10.*__FLT_EPSILON__));
    res.size = rect.width / ratio;

    res.array = (da_ptr_Personne*)calloc(res.size*res.size, sizeof(da_ptr_Personne));
    return (res);
}
void free_Hash_map(Hash_map *map)
{
    for (int i = 0; i < map->size*map->size; i++)
        da_free(&map->array[i]);
    free(map->array);
}

void build_Hash_map(Hash_map *map, const da_Personne *personnes, const Rectangle vir_canvas)
{
    for (int i = 0; i < map->size*map->size; i++)
        map->array[i].size = 0;

    foreach_ptr (Personne, personne, personnes)
    {
        // floor index x implicit ceil
        int fix = hash_x_Hash_map(personne->pos, map, vir_canvas);
        // floor index y implicit ceil
        int fiy = hash_y_Hash_map(personne->pos, map, vir_canvas);

        DEBUG_ASSERT(0 <= fix);       DEBUG_ASSERT(fix < 1./map->ratio * vir_canvas.width);
        DEBUG_ASSERT(0 <= fiy);       DEBUG_ASSERT(fiy < 1./map->ratio * vir_canvas.height);
        DEBUG_ASSERT(fix < map->size);DEBUG_ASSERT(fiy < map->size);
        

        if (0 <= fiy && fiy < map->size && 0 <= fix && fix < map->size)
            da_push(&map->array[fiy*map->size+fix], personne)
    }
}


void draw_Hash_map(const Simulation_context *context)
{
    const Hash_map *map = &context->map;
    for (int l = 0; l < map->size; l++)
    {
        for (int c = 0; c < map->size; c++)
        {
            Vec2 pos_d = (Vec2){
                map->ratio * (float)c / context->vir_canvas.width,
                map->ratio * (float)l / context->vir_canvas.height,
            };
            pos_d.x *= context->render_box.width;
            pos_d.y *= context->render_box.height;
            pos_d.x += context->render_box.x;
            pos_d.y += context->render_box.y;

            float size = map->ratio / context->vir_canvas.width  * context->render_box.width;

            DrawRectangleLinesEx(
                (Rectangle){pos_d.x, pos_d.y, size, size},
                1., DARKPURPLE
            );
            DrawTextF("%d", pos_d.x+3., pos_d.y+3., 20, DARKPURPLE, map->array[l*map->size + c].size);
        }
    }
}


Window_handel init_window()
{
    srand(time(NULL));

    Window_handel res = {0};
    
    res.target_FPS = 60;
    res.render_time = 0;
    res.contexts = (da_ptr_Simulation_context){0};


    SetTraceLogLevel(LOG_NONE);
    InitWindow(900, 900, WINDOWNAME);

    SetTargetFPS(res.target_FPS);

    return (res);
}
void destroy_window(Window_handel *win)
{
    da_free(&win->contexts);
}



#pragma region ui_fonction_pointers
void restart_context(Simulation_context *context);

// sliders
void f_frame_scale(Simulation_context *context, float v)
{
    context->step_by_frame = pow(10., v);
    printf("new step_by_frame: %d\n", context->step_by_frame);
}
void f_fild_scale(Simulation_context *context, float v)
{
    context->fild_strength = v;
    printf("new fild_strength: %f\n", context->fild_strength);
}
void f_particule_count(Simulation_context *context, float v)
{
    context->inital_particule_count = (int)v;
    printf("new inital_particule_count: %d\n", context->inital_particule_count);
    restart_context(context);
}
void f_radius_scale(Simulation_context *context, float v)
{
    pe_template.radius = v;
    foreach_ptr (Personne, personne, &context->pers)
        personne->radius = v + v * (v2_rand(0., .1).x - 0.05);
    printf("new radius: %f +-0.05%%\n", v);
}
void f_tau_scale(Simulation_context *context, float v)
{
    float val = pow(10., v);
    pe_template.tau = val;
    foreach_ptr (Personne, personne, &context->pers)
        personne->tau = val;
    printf("new tau: 10^%f = %f\n", v, val);
}
void f_wish_distance(Simulation_context *context, float v)
{
    float val = pow(10., v);
    pe_template.wish_dist = val;
    foreach_ptr (Personne, personne, &context->pers)
        personne->wish_dist = val;
    printf("new wish distance: 10^%f = %f\n", v, val);
}



void f_move_obstacle(Simulation_context *context, float v)
{
    rm_obstacle(context);
    add_obstacle(context, v);
}
void f_wall_door(Simulation_context *context, float v)
{
    
    const float Yopen = 5. - v;
    printf("size door: %f\n", 2.*Yopen);
    const float door_alin = 0.0;

    
    da_get(&context->walls, 0) = (Wall){
        .pos = (Vec2){context->vir_canvas.width-1., context->vir_canvas.height-1.},
        .len = (Vec2){0., door_alin+Yopen-context->vir_canvas.width*.5},
        .radius = rad_wall
    };

    da_get(&context->walls, 1) = (Wall){
        .pos = (Vec2){context->vir_canvas.width-1., 1.},
        .len = (Vec2){0., door_alin+context->vir_canvas.width*.5-Yopen},
        .radius = rad_wall
    };
}

// buttons
void f_change_to_fild_rotate(Simulation_context *context, bool state)
{
    pe_template.fild = fild_rotate;
    foreach_ptr (Personne, personne, &context->pers)
        personne->fild = fild_rotate;
    printf("fild rotate\n");
}
void f_change_to_fild_pogo(Simulation_context *context, bool state)
{
    pe_template.fild = fild_pogo;
    foreach_ptr (Personne, personne, &context->pers)
        personne->fild = fild_pogo;
    printf("fild pogo\n");
}
void f_change_to_fild_mouse(Simulation_context *context, bool state)
{
    pe_template.fild = fild_mouse;
    foreach_ptr (Personne, personne, &context->pers)
        personne->fild = fild_mouse;
    printf("fild mouse\n");
}
void f_change_to_fild_door(Simulation_context *context, bool state)
{
    pe_template.fild = fild_door;
    foreach_ptr (Personne, personne, &context->pers)
        personne->fild = fild_door;
    printf("fild door\n");
}

void f_stop_simulation(Simulation_context *context, bool state)
{
    context->stoped = true;

    printf("particule restante : %d\n", context->pers.size);
    printf("temp total : %lf\n", context->time);

    da_get(&context->ui.buttons, 0).state = 0; // pause
    restart_context(context);
    foreach_ptr (Button_switch, button, &context->ui.buttons)
        button->reset_value = true;
    foreach_ptr (Slider, slider, &context->ui.sliders)
        slider->reset_value = true;
    printf("[stop]\n");
}
void f_draw_fild_dir(Simulation_context *context, bool state)
{
    context->draw_fild_dir = !state;
}
void f_pause_play(Simulation_context *context, bool state)
{
    printf("state[%d]\n", state);
    context->stoped = false;
}
void f_hash_map_mode(Simulation_context *context, bool state)
{
    context->mode_hash_map = state;
}
void f_obstacle(Simulation_context *context, bool state)
{
    rm_obstacle(context);
    context->obstacle = state ? triangle : circle;
    add_obstacle(context, 0.);
}

#pragma endregion


void init_ui_component(Gui_handel *ui)
{
    // init sliders
    float paddx = 0.;
    float paddy = 4.;
    float width = 200;
    float height = 32;
    add_Slider(ui, (Slider){
        .value=2.,
        .min_val=1.,
        .max_val=3.,
        .label = "time",
        .reset_value = 0,
        .show_only_on_stop = false,
        .scale_function = f_frame_scale,
        .rect = (Rectangle){.x = paddx, .y = paddy, .width = width, .height = height}
    });
    add_Slider(ui, (Slider){
        .value=1.,
        .min_val=__FLT_EPSILON__,
        .max_val=20.,
        .label = "fild",
        .show_only_on_stop = false,
        .reset_value = 0,
        .scale_function = f_fild_scale,
        .rect = (Rectangle){ .x = paddx, .y = height + 2.* paddy, .width = width, .height = height}
    });
    paddx += width + 10;
    add_Slider(ui, (Slider){
        .value=100.,
        .min_val=1.,
        .max_val=800.,
        .show_only_on_stop = true,
        .label = "particule",
        .rect = (Rectangle){ .x = paddx, .y = paddy, .width = width, .height = height},
        .scale_function = f_particule_count,
    });
    add_Slider(ui, (Slider){
        .value=.3,
        .min_val=.08,
        .max_val=2.,
        .show_only_on_stop = true,
        .label = "radius",
        .rect = (Rectangle){ .x = paddx, .y = height + 2.* paddy, .width = width, .height = height},
        .scale_function = f_radius_scale,
    });
    paddx += width + 10.;
    add_Slider(ui, (Slider){
        .value=1.,
        .min_val=0.,
        .max_val=4.,
        .show_only_on_stop = false,
        .label = "door",
        .rect = (Rectangle){ .x = paddx, .y = paddy, .width = width, .height = height},
        .scale_function = f_wall_door,
    });
    add_Slider(ui, (Slider){
        .value=.3,
        .min_val=0.,
        .max_val=8.,
        .show_only_on_stop = false,
        .label = "obstacle",
        .rect = (Rectangle){ .x = paddx, .y = height + 2.* paddy, .width = width, .height = height},
        .scale_function = f_move_obstacle,
    });
    paddx += width + 10.;
    add_Slider(ui, (Slider){
        .value=-2,
        .min_val=-6.,
        .max_val=0.,
        .show_only_on_stop = false,
        .label = "tau",
        .rect = (Rectangle){ .x = paddx, .y = paddy, .width = width, .height = height},
        .scale_function = f_tau_scale,
    });
    add_Slider(ui, (Slider){
        .value=-2.5,
        .min_val=-3.,
        .max_val=-1.,
        .show_only_on_stop = false,
        .label = "wish",
        .rect = (Rectangle){ .x = paddx, .y = height + 2.* paddy, .width = width, .height = height},
        .scale_function = f_wish_distance,
    });
    
    // init buttons
    paddx = 4.;
    paddy = 4.;
    width = 32;
    height = 32;
    
    float s_x = paddx;
    float s_y = 90.;
    float x = s_x;
    float y = s_y;

    add_Button(ui, (Button_switch){
        .state = 0,
        .reset_value = 0,
        .icons0 = "#131#",
        .icons1 = "#132#",
        .push_function = f_pause_play,
        .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
    });
    x += paddx + width;
    add_Button(ui, (Button_switch){
        .state = 0,
        .reset_value = 0,
        .icons0 = "#133#",
        .icons1 = "#133#",
        .push_function = f_stop_simulation,
        .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
    });
    x = s_x;
    y += paddy + height;
    add_Button(ui, (Button_switch){
        .state = 0,
        .reset_value = 0,
        .icons0 = "#64#",
        .icons1 = "#64#",
        .push_function = f_change_to_fild_door,
        .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
    });
    x += paddx + width;
    add_Button(ui, (Button_switch){
        .state = 0,
        .reset_value = 0,
        .icons0 = "#211#",//"#64#"
        .icons1 = "#211#",
        .push_function = f_change_to_fild_rotate,
        .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
    });
    x = s_x;
    y += paddy + height;
    add_Button(ui, (Button_switch){
        .state = 0,
        .reset_value = 0,
        .icons0 = "#21#",
        .icons1 = "#21#",
        .push_function = f_change_to_fild_mouse,
        .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
    });
    x += paddx + width;
    add_Button(ui, (Button_switch){
        .state = 0,
        .reset_value = 0,
        .icons0 = "#152#",//"#192#",//"#64#"
        .icons1 = "#152#",//"#192#",
        .push_function = f_draw_fild_dir,
        .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
    });
    x = s_x;
    y += paddy + height;
    add_Button(ui, (Button_switch){
        .state = 0,
        .reset_value = 0,
        .icons0 = "#76#",
        .icons1 = "#76#",
        .push_function = f_change_to_fild_pogo,
        .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
    });
    x += paddx + width;
    add_Button(ui, (Button_switch){
        .state = 0,
        .reset_value = 0,
        .icons0 = "#95#",
        .icons1 = "#96#",
        .push_function = f_hash_map_mode,
        .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
    });
    x = s_x;
    y += paddy + height;
    add_Button(ui, (Button_switch){
        .state = 0,
        .reset_value = 0,
        .icons0 = "#121#",
        .icons1 = "#212#",
        .push_function = f_obstacle,
        .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
    });
}

Simulation_context init_context(int nb_particule, float step)
{
    Simulation_context res = {0};
    
    // init data struct
    res.pers = *da_make(&res.pers);
    res.walls = *da_make(&res.walls);


    // not restart by restart_context
    res.inital_particule_count = nb_particule;
    res.vir_canvas = (Rectangle){0., 0., 10., 10.};

    Vec2 pos = (Vec2){0., 0.};
    res.render_box = (Rectangle){pos.x, pos.y, GetScreenWidth() - fmax(pos.x, pos.y), GetScreenHeight() - fmax(pos.x, pos.y)};
    assert(res.render_box.width == res.render_box.height);
    
    res.fild_strength = 1.;
    res.step = step;
    res.step_by_frame = (int)(1. / res.step) / 1000;
    
    res.fild = fild_mouse;

    res.ui = init_gui();
    init_ui_component(&res.ui);


    foreach_ptr (Button_switch, button, &res.ui.buttons)
    {
        button->rect.x += res.render_box.x;
        button->rect.y += res.render_box.y;
    }
    foreach_ptr (Slider, slider, &res.ui.sliders)
    {
        slider->rect.x += res.render_box.x;
        slider->rect.y += res.render_box.y;
    }

    res.draw_fild_dir = true;
    
    // 
    populate_Personne(&res.pers, nb_particule);    
    populate_Wall(&res.walls, res.vir_canvas);
    
    res.obstacle = circle;
    add_obstacle(&res, 7.);

    assert(res.vir_canvas.width == res.vir_canvas.height);
    res.map = init_Hash_map(.5, res.vir_canvas);
    

    // restart_context equivalent 
    res.stoped = true;
    res.time = 0.;
    res.tick = 0;

    return (res);
}

void simulate_context(Simulation_context *obj)
{
    for (int _ = 0; _ < obj->step_by_frame; _++)
    {
        if (obj->mode_hash_map)
            build_Hash_map(&obj->map, &obj->pers, obj->vir_canvas);


        #ifdef KUTTA2
        for (int i = 0; i < obj->pers.size; i++)
            kutta2_social(&obj->pers, obj->step, i, &obj->walls);
        #else
        for (int i = 0; i < obj->pers.size; i++)
            euler_social(obj, obj->step, i, &obj->walls);
        #endif

        
        
        wish_update(&obj->pers, obj->fild, obj->vir_canvas, obj->fild_strength);

        obj->tick++;
        obj->time += obj->step;
        
        if (obj->pers.size == 0)
            break;
    }

}

void restart_context(Simulation_context *context)
{
    context->pers.size = 0;
    populate_Personne(&context->pers, context->inital_particule_count);
    da_get(&context->ui.sliders, 3).scale_function(context, da_get(&context->ui.sliders, 3).value);
    


    context->time = 0.;
    context->tick =  0; 
    context->stoped = true;
}



void free_context(Simulation_context *obj)
{
    da_free(&obj->walls);
    da_free(&obj->pers);
    free_gui(&obj->ui);
    free_Hash_map(&obj->map);
}


// inside BeginDrawing() / EndDrawing() pair
void context_draw(Simulation_context *context)
{
    DrawRectangleRec(context->render_box, BLACK);

    const Color particule_color = WHITE;
    rlColor4ub(particule_color.r, particule_color.g, particule_color.b, particule_color.a);

    
    
    // draw personnes
    for (int j = 0; j < context->pers.size; j++)
    {
        float x = context->pers.arr[j].pos.x;
        x /= context->vir_canvas.width;
        x *= context->render_box.width;
        x += context->render_box.x;

        float y = context->pers.arr[j].pos.y;
        y /= context->vir_canvas.height;
        y *= context->render_box.height;
        y += context->render_box.y;
        
        float size = context->pers.arr[j].radius / context->vir_canvas.width  * context->render_box.width;

        if (context->pers.arr[j].back_step)
            DrawCircle(x, y, 0.9 * size, RED);
        else DrawCircle(x, y, 0.9 * size, context->pers.arr[j].color);
        
        if (context->draw_fild_dir)
        {
            Vec2 fild_dir = context->pers.arr[j].wish_dir;

            DrawLineEx(
                (Vector2){x, y},
                (Vector2){x+fild_dir.x*10., y+fild_dir.y*10.},
                3., WHITE
            );
            
            fild_dir = v2_scal_prod(
                v2_lenght(context->pers.arr[j].speed)/ max_speed, 
                fild_dir
            );
            DrawLineEx(
                (Vector2){x, y}, 
                (Vector2){x+fild_dir.x*10., y+fild_dir.y*10.},
                2., RED
            );

        }
    }
    // draw walls
    foreach_ptr (Wall, wall, &context->walls)
    {
        float x = (wall->pos.x) / context->vir_canvas.width * context->render_box.width;
        x += context->render_box.x;
        float y = (wall->pos.y) / context->vir_canvas.height * context->render_box.height;
        y += context->render_box.y;
        float w = (wall->len.x) / context->vir_canvas.width * context->render_box.width;
        float h = (wall->len.y) / context->vir_canvas.height * context->render_box.height;
        
        float r = wall->radius / context->vir_canvas.width * context->render_box.width;
        
        // r *= .9;
        DrawLineEx((Vector2){x, y}, (Vector2){x+w, y+h}, 2.*r, RED);
        DrawCircle(x, y, r, RED);
        DrawCircle(x+w, y+h, r, RED);
        
    }
    
    if (context->draw_fild_dir && context->mode_hash_map)
        draw_Hash_map(context);
    
    ui_draw(context);
}

void window_draw(Window_handel *win)
{
    BeginDrawing();

    ClearBackground(GetColor(GuiGetStyle(DEFAULT, BACKGROUND_COLOR)));
    foreach_ptr (Simulation_context *, context, &win->contexts)
        context_draw(*context);


    EndDrawing();
}

int main()
{

    Window_handel win = init_window();
    
    
    Simulation_context context = init_context(100, 0.0001);
    da_push(&win.contexts, &context);
    
    


    while (!WindowShouldClose())
    {
        foreach_ptr (Simulation_context *, context, &win.contexts)
        {
            if ((*context)->ui.buttons.arr[0].state)
            {
                TIME((*context)->simulate_time) 
                    simulate_context(*context);  
                if ((*context)->pers.size == 0)
                    f_stop_simulation(*context, true);
            }
        }
        
        TIME(win.render_time)
            window_draw(&win);
        
        foreach_ptr (Simulation_context *, context, &win.contexts)
        {
            TIME((*context)->gui_reset_time) {
                int nb_particule = (*context)->pers.size;
                reset_gui_context(*context);
            }
        }
    }
    
    free_context(&context);
    destroy_window(&win);
}

