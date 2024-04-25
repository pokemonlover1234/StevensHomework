#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "linked_list.h"

void print_str(void *str) {
    printf("\"%s\"", (char *)str);
}

void print_int(void *integer) {
    printf("%d", *(int *)integer);
}

void insert_string(linked_list *list, char *string, bool at_end) {
    if (at_end) {
        push_back(list, create_node((void *)strdup(string)));
    } else {
        push_front(list, create_node((void *)strdup(string)));
    }
}

void insert_integer(linked_list *list, int integer, bool at_end) {
    int *value = (int *)malloc(sizeof(int));
    *value = integer;
    if (at_end) {
        push_back(list, create_node((void *)value));
    } else {
        push_front(list, create_node((void *)value));
    }
}

int str_cmp(const void *a, const void *b) {
    return strcmp(*(const char **)a, *(const char **)b);
}

int int_cmp(const void *a, const void *b) {
    return *(const int *)a - *(const int *)b;
}

/**
 * Returns a new linked list with all the elements from the original list
 * that are less than the supplied key.
 * Works on strings.
 */
linked_list *find_less_str(linked_list *list, char *key,
                           int (*cmp)(const void *, const void *)) {
    linked_list *results = NULL;
    for (node *cur = list->head; cur != NULL; cur = cur->next) {
        if (cmp(&cur->data, &key) < 0) {
            if (!results) {
                results = create_linked_list();
            }
            push_back(results, create_node((void *)strdup(cur->data)));
        }
    }
    if (results) {
        char **array = (char **)malloc(results->num_nodes * sizeof(char *)),
             **p;
        p = array;
        for (node *cur = results->head; cur != NULL; cur = cur->next) {
            *p++ = (char *)cur->data;
        }
        qsort(array, results->num_nodes, sizeof(char *), cmp);
        p = array;
        for (node *cur = results->head; cur != NULL; cur = cur->next) {
            cur->data = *p++;
        }
        free(array);
    }
    return results;
}

int *intdup(int *value) {
    int *copy = malloc(sizeof(int));
    *copy = *value;
    return copy;
}

/**
 * Returns a new linked list with all the elements from the original list
 * that are less than the supplied key.
 * Works on ints.
 */
linked_list *find_less_int(linked_list *list, int key,
                           int (*cmp)(const void *, const void *)) {
    linked_list *results = NULL;
    for (node *cur = list->head; cur != NULL; cur = cur->next) {
        if (cmp(cur->data, &key) < 0) {
            if (!results) {
                results = create_linked_list();
            }
            push_back(results, create_node((void *)intdup(cur->data)));
        }
    }
    if (results) {
        int *array = (int *)malloc(results->num_nodes * sizeof(int)),
            *p;
        p = array;
        for (node *cur = results->head; cur != NULL; cur = cur->next) {
            *p++ = *(int *)cur->data;
        }
        qsort(array, results->num_nodes, sizeof(int), cmp);
        p = array;
        for (node *cur = results->head; cur != NULL; cur = cur->next) {
            *(int *)cur->data = *p++;
        }
        free(array);
    }
    return results;
}

int main() {
    linked_list *list = create_linked_list();
    insert_string(list, "apples", true);
    insert_string(list, "oranges", true);
    insert_string(list, "zebras", false);
    insert_string(list, "horses", false);
    insert_string(list, "cats", false);
    insert_string(list, "sharks", true);
    puts("Original list:");
    print_list(list, print_str);
    linked_list *less = find_less_str(list, "oranges", str_cmp);
    puts("Search results:");
    if (less) {
        print_list(less, print_str);
    } else {
        puts("No results found.");
    }

    while (list->num_nodes > 0) {
        node *front = pop_front(list);
        printf("Popped value: %s\n", (char *)front->data);
        free_node(front, free);
    }
    free(list);
    if (less) {
        while (less->num_nodes > 0) {
            free_node(pop_front(less), free);
        }
    }
    free(less);

    list = create_linked_list();
    insert_integer(list, 20, true);
    insert_integer(list, 99, true);
    insert_integer(list, 81, false);
    insert_integer(list, 46, false);
    insert_integer(list, 55, false);
    insert_integer(list, 19, true);
    puts("Original list:");
    print_list(list, print_int);
    less = find_less_int(list, 21, int_cmp);
    puts("Search results:");
    if (less) {
        print_list(less, print_int);
    } else {
        puts("No results found.");
    }

    while (list->num_nodes > 0) {
        node *front = pop_front(list);
        printf("Popped value: %d\n", *(int *)front->data);
        free_node(front, free);
    }
    free(list);
    if (less) {
        while (less->num_nodes > 0) {
            free_node(pop_front(less), free);
        }
    }
    free(less);

    return 0;
}
