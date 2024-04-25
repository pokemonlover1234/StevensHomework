/**
 * Name: Aidan Fischer
 * No Partner
 * 2/26/2021 
 * I pledge my honor that I have abided by the Stevens Honor System.
 */

#ifndef LINKEDLIST_H_
#define LINKEDLIST_H_

#include <stdio.h>
#include <string.h>
#include "node.h"

typedef struct linked_list {
    node *head;
    node *tail;
    size_t num_nodes;
} linked_list;

linked_list* create_linked_list() {
    return (linked_list *)calloc(1, sizeof(linked_list));
}

/**
 * Inserts a non-NULL node into a non-NULL linked list.
 * The node is inserted so that the data in the linked list is in
 * non-decreasing order.
 * A node with a value already in the list is inserted AFTER the node(s)
 * already in the list.
 */
void insert_in_order(linked_list *list, node *n,
                     int (*cmp)(const void*, const void*)) {
    node *prev = NULL;
    node *cur = list->head;
    //Place new node at start of list if list is empty or it is before head.
    if(cur == NULL){
        list->head = n;
        list->tail = n;
        list->num_nodes++;
    } else if(cmp(n->data,cur->data) < 0) { 
        list->head = n;
        cur->prev = n;
        n->next = cur;
        list->num_nodes++;
    }else if(cmp(n->data,cur->data) >= 0){
        //Traverse linked list until we get to where cur is directly AFTER where we need to put the new node.
        //And prev is directly prior to where it needs to go.
        do{
            prev = cur;
            cur = cur->next;
        } while (cur != NULL && cmp(n->data,cur->data) >= 0);
        //Update proper pointers
        //If cur is null that means the new node needs to be the new tail.
        if (cur == NULL){
            prev->next = n;
            n->prev = prev;
            list->tail = n;
            list->num_nodes++;
        } else {
            prev->next = n;
            n->prev = prev;
            cur->prev = n;
            n->next = cur;
            list->num_nodes++;
        }
    }
}

void print_list(linked_list *list, void (*print_function)(void*)) {
    putchar('[');
    node *cur = list->head;
    if (cur != NULL) {
        print_function(cur->data);
        cur = cur->next;
    }
    for ( ; cur != NULL; cur = cur->next) {
        printf(", ");
        print_function(cur->data);
    }
    printf("]\n{length: %lu, head->data: ", list->num_nodes);
    list->head != NULL ? print_function(list->head->data) :
                         (void)printf("NULL");
    printf(", tail->data: ");
    list->tail != NULL ? print_function(list->tail->data) :
                         (void)printf("NULL");
    printf("}\n\n");
}

/**
 * Frees a list starting from the tail.
 * This will check if your previous pointers have been set up correctly.
 */
void free_list(linked_list *list, void (*free_data)(void *)) {
    while (list->tail != NULL) {
        node *prev = list->tail->prev;
        free_node(list->tail, free_data);
        list->tail = prev;
    }
}

#endif
