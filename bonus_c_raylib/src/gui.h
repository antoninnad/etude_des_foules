#include "da.h"
#include "vec2.h"
#include "raylib.h"


#ifndef GUI_H
# define GUI_H

typedef struct Simulation_context Simulation_context;
#define LABEL_MAX_SIZE 64
typedef struct Slider
{
    Rectangle rect;

    bool show_only_on_stop;
    void (*scale_function)(Simulation_context*, float);
    float value;
    float min_val;
    float max_val;
    char label[LABEL_MAX_SIZE];
    bool reset_value;
} Slider;
DA_TYPEDEF_ARRAY(Slider);

typedef struct Button_switch
{
    Rectangle rect;
    
    bool state;
    void (*push_function)(Simulation_context*, bool);
    char icons0[LABEL_MAX_SIZE];
    char icons1[LABEL_MAX_SIZE];
    bool reset_value;
} Button_switch;
DA_TYPEDEF_ARRAY(Button_switch);


typedef struct Gui_handel
{
    da_Slider sliders;
    da_Button_switch buttons;
} Gui_handel;




Gui_handel init_gui();
void add_Slider(Gui_handel *res, Slider slider);
void add_Button(Gui_handel *res, Button_switch button);
void reset_gui_context(Simulation_context *context);
void ui_draw(Simulation_context *context);
void free_gui(Gui_handel *gui);

#endif /* GUI_H */
