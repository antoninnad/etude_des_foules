.PHONY : so_debug so_re so_exe so_release so_release_re so_release_exe clean

# For user input
FLAGS= 

CC = clang
LD = clang
GENERAL_CFLAGS = -I~/C/my_lib -I./include_h -Wall $(FLAGS) -Wno-error=sign-compare -Wno-sign-compare -Wno-unused-function -Wno-unused-variable
GENERAL_LDFLAGS = -I~/C/my_lib -I./include_h  -lpthread -lm -l:libraylib.a  -L./lib




# SOCIAL :

SO_HDR = $(wildcard src/*.h)
SO_SRC = $(wildcard src/*.c)
SO_ARGS =


# SO_DEBUG TARGET
SO_CFLAGS_DEBUG = -g3 -O0 -DDEBUG -Werror -fsanitize=address -fsanitize=undefined $(GENERAL_CFLAGS)
SO_LDFLAGS_DEBUG = -fsanitize=address -fsanitize=undefined $(GENERAL_LDFLAGS)

SO_OBJ_DEBUG = $(SO_SRC:.c=_debug.o)
SO_BIN_DEBUG = ./so_debug.out

so_debug : $(SO_BIN_DEBUG)
default : so_debug
so_re : clean $(SO_BIN_DEBUG)
so_exe : 
	$(SO_BIN_DEBUG) $(SO_ARGS)

$(SO_BIN_DEBUG) : $(SO_OBJ_DEBUG)
	$(LD) $^ $(LIB) $(SO_LDFLAGS_DEBUG) -o $@

%_debug.o : %.c
	$(CC) -c $(SO_CFLAGS_DEBUG) $< -o $@

# END SO_DEBUG TARGET


# SO_RELEASE TARGET
SO_CFLAGS_RELEASE = -O3 $(GENERAL_CFLAGS)
SO_LDFLAGS_RELEASE = $(GENERAL_LDFLAGS)

SO_OBJ_RELEASE = $(SO_SRC:.c=_release.o)
SO_BIN_RELEASE = ./so_release.out

so_release : $(SO_BIN_RELEASE)
so_release_re : clean $(SO_BIN_RELEASE)
so_release_exe : 
	$(SO_BIN_RELEASE) $(SO_ARGS)


$(SO_BIN_RELEASE) : $(SO_OBJ_RELEASE)
	$(LD) $^ $(LIB) $(SO_LDFLAGS_RELEASE) -o $@

%_release.o : %.c
	$(CC) -c $(SO_CFLAGS_RELEASE) $< -o $@

# END SO_RELEASE TARGET


clean :
	rm -f $(SO_OBJ_DEBUG) $(SO_OBJ_RELEASE) 
	rm -f $(SO_BIN_DEBUG) $(SO_BIN_RELEASE)
	
