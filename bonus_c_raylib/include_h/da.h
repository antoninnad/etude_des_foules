#ifndef DA_H 
# define DA_H

#ifndef DA_BASE_SIZE
# define DA_BASE_SIZE 8
#endif

#ifndef DA_SIZE_FACTOR
# define DA_SIZE_FACTOR 2
#endif


#include <string.h>

#ifndef DA_ASSERT
# include <assert.h>
# define DA_ASSERT assert
#endif


#if !defined(DA_ALLOCATOR) || !defined(DA_REALLOCATOR) || !defined(DA_FREE)
# include <stdlib.h>
# define DA_ALLOCATOR malloc
# define DA_REALLOCATOR realloc
# define DA_FREE free
#endif



#define DA_TYPEDEF_ARRAY(T)\
typedef struct da_##T\
{\
    int size;\
    int capacity;\
    T *arr;\
} da_##T


// if ptr to type only the TYPEDEF_ARRAY_PTR differ otherwise da_T <=> da_ptr_T
#define DA_TYPEDEF_ARRAY_PTR(T)\
typedef struct da_ptr_##T\
{\
    int size;\
    int capacity;\
    T **arr;\
} da_ptr_##T




// da_T *da_make_size(da_T *obj, size_t size)
// usage :
// da_T obj = *da_make_size(T, &obj, 16);
// da_T *obj1 = malloc(sizeof(ad_T)); da_make_size(T, obj1, 16); //!\  .
// da_T obj = {0}; // work too 
#define da_make_size(obj, base_size)\
(\
    (obj)->size = 0,\
    (obj)->capacity = base_size,\
    (obj)->arr = DA_ALLOCATOR(sizeof((obj)->arr[0]) * base_size),\
    (obj)\
)

// (da_T)da_make_size(da_T *obj, size_t size)
// same as da_make_size() but with base_size = DA_BASE_SIZE (can be user defined)
#define da_make(obj) da_make_size(obj, DA_BASE_SIZE)

// mem is allocated before hand
#define da_cpy(dest, src)\
(\
    \
    DA_ASSERT((dest)->size == 0),\
    ((dest)->arr == NULL) ?\
    (\
        (dest)->capacity = (src)->size,\
        (dest)->arr = DA_ALLOCATOR(sizeof((src)->arr[0]) * (src)->size)\
    )\
    :\
    (\
        ((dest)->capacity < (src)->size) ?\
        (\
            (dest)->capacity = (src)->size,\
            (dest)->arr = DA_REALLOCATOR(sizeof((src)->arr[0]) * (src)->size)\
        )\
    )\
    memcpy((dest)->arr, (src)->arr, sizeof((src)->arr[0]) * (src)->size)\
)\

// to use compond literal add parentheses : da_push(obj, ((T){...}));
// void da_push(da_T *obj, T element);
#define da_push(obj, element)\
{\
    if ((obj)->arr == NULL)\
    {\
        DA_ASSERT((obj)->size == 0 && (obj)->capacity == 0); /* init with {0} */\
        (obj)->capacity = DA_BASE_SIZE;\
        (obj)->arr = DA_ALLOCATOR(sizeof((obj)->arr[0]) * (obj)->capacity);\
    }\
    if ((obj)->size+1 >= (obj)->capacity)\
    {\
        (obj)->capacity *= 2;\
        (obj)->arr = DA_REALLOCATOR((obj)->arr, sizeof((obj)->arr[0]) * (obj)->capacity);\
        DA_ASSERT((obj)->arr != NULL);\
    }\
    (obj)->arr[(obj)->size++] = (element);\
}

// T da_get(da_T *obj, int index);
#define da_get(obj, index) ((obj)->arr[(DA_ASSERT(0 <= index && index < (obj)->size), index)])

// T da_pop(da_T *obj);
#define da_pop(obj) ((obj)->arr[(DA_ASSERT((obj)->size > 0), --(obj)->size)])
// #define da_pop(obj) ((obj)->size > 0 ? (obj)->arr[(obj)->size--] : {0})


// no free and reorganize ordre
// void da_erase_index(da_T *obj, int index)
#define da_erase_index(obj, index)\
(\
    DA_ASSERT((obj)->size > 0 && 0 <= index && index < (obj)->size),\
    (obj)->arr[index] = da_top(obj),\
    (obj)->size--\
)

// void da_erase_index_ordered(da_T *obj, int index)
#define da_erase_index_ordered(obj, index)\
{\
    DA_ASSERT((obj)->size > 0 && 0 <= index && index < (obj)->size);\
    for (int da_i = (index); da_i < (obj)->size-1; da_i++)\
        (obj)->arr[da_i] = (obj)->arr[da_i+1];\
    (obj)->size--;\
}



// T da_top(da_T *obj);
#define da_top(obj) ((obj)->arr[(DA_ASSERT((obj)->size > 0), (obj)->size-1)])
// #define da_top(obj) ((obj)->size > 0 ? (obj)->arr[(obj)->size-1] : {0})

// void da_free(da_T *obj);
#define da_free(obj)\
{\
    if ((obj)->arr)\
        DA_FREE((obj)->arr);\
}

// void da_free(da_T *obj, void (*free_fun)(T *obj));
#define da_free_func(obj, free_fun)\
{\
    if ((obj)->arr)\
    {\
        for (int i = 0; i < (obj)->size; i++)\
            free_fun((obj)->arr[i]);\
        DA_FREE((obj)->arr);\
    }\
}
// foreach (item* in obj) {...}
// without copy
#ifndef foreach_ptr
# define foreach_ptr(T, item, obj) for (T *item = &(obj)->arr[0]; item < &(obj)->arr[(obj)->size]; item++)
#endif

#endif /* DA_H */
