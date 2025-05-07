#include "social.h"
#include "gui.h"



void add_Button(Gui_handel *res, Button_switch button)
{
    assert(strlen(button.icons0) < LABEL_MAX_SIZE);
    assert(strlen(button.icons1) < LABEL_MAX_SIZE);
    da_push(&res->buttons, button);
}
void add_Slider(Gui_handel *res, Slider slider)
{
    assert(strlen(slider.label) < LABEL_MAX_SIZE);
    da_push(&res->sliders, slider);
}




static void reset_sliders(Simulation_context *context, Slider *element)
{
    if (!element->reset_value)
        return ;
    element->reset_value = 0;

    element->scale_function(context, element->value);
}
static void reset_buttons(Simulation_context *context, Button_switch *element)
{
    if (!element->reset_value)
        return ;
    
    printf("button pressed (%s)\n", element->icons0);
    element->reset_value = 0;
    element->state = !element->state;
    element->push_function(context, element->state);
    // return (!element->state);
}


// sync gui and context
void reset_gui_context(Simulation_context *context)
{
    Gui_handel *ui = &context->ui;

    foreach_ptr (Slider, slider, &ui->sliders)
        reset_sliders(context, slider);

    foreach_ptr (Button_switch, button, &ui->buttons)
        reset_buttons(context, button);
}


static void sliders_draw(const da_Slider *sliders, bool simu_stoped)
{
    foreach_ptr (Slider , slider, sliders)
    {
        if (!slider->show_only_on_stop || simu_stoped)
        {
            slider->reset_value = GuiSliderBar(
                slider->rect,
                "",
                "",
                &slider->value,
                slider->min_val,
                slider->max_val
            );
            DrawTextF("%s: %.3f", 
                slider->rect.x + slider->rect.width *.03,
                slider->rect.y + slider->rect.height *.1,
                24, RED,
                slider->label,
                slider->value
            );
        }
    }
}
static void buttons_draw(const da_Button_switch *buttons)
{
    foreach_ptr (Button_switch , button, buttons)
    {
        button->reset_value = GuiButton(
            button->rect, 
            button->state ? button->icons1 : button->icons0
        );
    }
}

// inside BeginDrawing() / EndDrawing() pair
void ui_draw(Simulation_context *context)
{
    sliders_draw(&context->ui.sliders, context->stoped);
    buttons_draw(&context->ui.buttons);


    DrawTextF("FPS: %d", 
        10 + context->render_box.x, 
        context->render_box.height + context->render_box.y - 75,
        24, LIGHTGRAY, GetFPS()
    );
    DrawTextF("Time simu: %lf\tTime reset ui: %lf",
        10 + context->render_box.y,
        context->render_box.height + context->render_box.y - 45,
        24, LIGHTGRAY, 
        TIME_CLOCK_TO_MILISEC(context->simulate_time),
        TIME_CLOCK_TO_MILISEC(context->gui_reset_time)
    );
}


Gui_handel init_gui()
{
    Gui_handel res = {0};
    res.sliders = (da_Slider){0};
    res.buttons = (da_Button_switch){0};

    /* {
        float paddx = 0.;
        float paddy = 4.;
        // float liney = 34 + 2.* paddy;
        float width = 200;
        float height = 32;
        add_Slider(&res, (Slider){
            .value=2.,
            .min_val=1.,
            .max_val=3.5,
            .label = "time",
            .reset_value = 0,
            .show_only_on_stop = false,
            .scale_function = f_frame_scale,
            .rect = (Rectangle){ .x = paddx, .y = paddy, .width = width, .height = height}
        });
        add_Slider(&res, (Slider){
            .value=1.,
            .min_val=__FLT_EPSILON__,
            .max_val=50.,
            .label = "fild strength",
            .show_only_on_stop = false,
            .reset_value = 0,
            .scale_function = f_fild_scale,
            .rect = (Rectangle){ .x = paddx, .y = height + 2.* paddy, .width = width, .height = height}
        });
        paddx += width + 10;
        add_Slider(&res, (Slider){
            .value=100.,
            .min_val=1.,
            .max_val=500.,
            .show_only_on_stop = true,
            .label = "init particule",
            .rect = (Rectangle){ .x = paddx, .y = paddy, .width = width, .height = height},
            .scale_function = f_particule_count,
        });
        add_Slider(&res, (Slider){
            .value=.3,
            .min_val=.04,
            .max_val=2.,
            .show_only_on_stop = true,
            .label = "radius particules",
            .rect = (Rectangle){ .x = paddx, .y = height + 2.* paddy, .width = width, .height = height},
            .scale_function = f_radius_scale,
        });
        paddx += width + 10.;
        add_Slider(&res, (Slider){
            .value=1.,
            .min_val=0.,
            .max_val=4.,
            .show_only_on_stop = false,
            .label = "door size",
            .rect = (Rectangle){ .x = paddx, .y = paddy, .width = width, .height = height},
            .scale_function = f_wall_door,
        });
        add_Slider(&res, (Slider){
            .value=.3,
            .min_val=0.,
            .max_val=4.,
            .show_only_on_stop = false,
            .label = "obstacle pos",
            .rect = (Rectangle){ .x = paddx, .y = height + 2.* paddy, .width = width, .height = height},
            .scale_function = f_move_obstacle,
        });
        paddx += width + 10.;
        add_Slider(&res, (Slider){
            .value=-2,
            .min_val=-6.,
            .max_val=0.,
            .show_only_on_stop = false,
            .label = "tau",
            .rect = (Rectangle){ .x = paddx, .y = paddy, .width = width, .height = height},
            .scale_function = f_tau_scale,
        });
        add_Slider(&res, (Slider){
            .value=-2.,
            .min_val=-3.,
            .max_val=-1.,
            .show_only_on_stop = false,
            .label = "wish distance",
            .rect = (Rectangle){ .x = paddx, .y = height + 2.* paddy, .width = width, .height = height},
            .scale_function = f_wish_distance,
        });
    }
    {
        float paddx = 4.;
        float paddy = 4.;
        float width = 32;
        float height = 32;
        
        float s_x = paddx;
        float s_y = 90.;
        float x = s_x;
        float y = s_y;

        add_Button(&res, (Button_switch){
            .state = 0,
            .reset_value = 0,
            .icons0 = "#131#",
            .icons1 = "#132#",
            .push_function = f_pause_play,
            .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
        });
        x += paddx + width;
        add_Button(&res, (Button_switch){
            .state = 0,
            .reset_value = 0,
            .icons0 = "#133#",
            .icons1 = "#133#",
            .push_function = f_stop_simulation,
            .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
        });
        x = s_x;
        y += paddy + height;
        add_Button(&res, (Button_switch){
            .state = 0,
            .reset_value = 0,
            .icons0 = "#64#",
            .icons1 = "#64#",
            .push_function = f_change_to_fild_door,
            .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
        });
        x += paddx + width;
        add_Button(&res, (Button_switch){
            .state = 0,
            .reset_value = 0,
            .icons0 = "#211#",//"#64#"
            .icons1 = "#211#",
            .push_function = f_change_to_fild_rotate,
            .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
        });
        x = s_x;
        y += paddy + height;
        add_Button(&res, (Button_switch){
            .state = 0,
            .reset_value = 0,
            .icons0 = "#21#",
            .icons1 = "#21#",
            .push_function = f_change_to_fild_mouse,
            .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
        });
        x += paddx + width;
        add_Button(&res, (Button_switch){
            .state = 0,
            .reset_value = 0,
            .icons0 = "#152#",//"#192#",//"#64#"
            .icons1 = "#152#",//"#192#",
            .push_function = f_draw_fild_dir,
            .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
        });
        x = s_x;
        y += paddy + height;
        add_Button(&res, (Button_switch){
            .state = 0,
            .reset_value = 0,
            .icons0 = "#76#",
            .icons1 = "#76#",
            .push_function = f_change_to_fild_pogo,
            .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
        });
        x += paddx + width;
        add_Button(&res, (Button_switch){
            .state = 0,
            .reset_value = 0,
            .icons0 = "#96#",
            .icons1 = "#96#",
            .push_function = f_hash_map_mode,
            .rect = (Rectangle){ .x = x, .y = y, .width = width, .height = height}
        });
    }
 */
    return (res);
}

void free_gui(Gui_handel *gui)
{
    da_free(&gui->buttons);
    da_free(&gui->sliders);
}
