#include<stdio.h>
#include<string.h>
#include<errno.h>
#include<stdlib.h>
#include<ctype.h>

#define BUFLEN 256
#define ARRAYLEN 32
#define FAKE_SPACE "|"

#define FILE_CONTENTS "a 1 b 2\n\na 1 c 4\n\nb 2 c 4\n\nb 2 d 0\n\nb 3 b 2\n\nb 3 e 2\n\nc 4 d 0\n\nc 4 e 1\n\n"

//#define DEBUG_OUTPUT 

typedef struct node {
    struct node* children[ARRAYLEN];
    struct node* parents[ARRAYLEN];
    char value[BUFLEN];
} node;

node* nodes_list[ARRAYLEN] = { NULL };
int node_count = 0;


/* 
 * my_split()
 * 
 * Take in a line from file contents, and split it based on spaces 
 * populate the two 'out' strings for the package and dependency name.
 * 
 * Note each out string contains the package name and version, with a 
 * space in between.
 * 
 * Returns: 4 when successful, 0 otherwise.
 */
int my_split(char* line, char** package, char** depend)
{
    int count = 0;
    char* space = strtok(line, " ");
    while (space != NULL)
    {
        count++;
        switch (count)
        {
        case 1:
            *package = malloc(BUFLEN*sizeof(char));
            sprintf(*package, "%s ", space);
            break;
        case 2:
            strcat(*package, space);
            break;
        case 3:
            *depend = malloc(BUFLEN*sizeof(char));
            sprintf(*depend, "%s ", space);
            break;
        case 4:
            strcat(*depend, space);
            break;
        }
        space = strtok(0, " ");
    }

    if (count < 4)
    {
        // If we didnt get all the parts constructed,
        // clean up any memory, and return 0.
        if (*depend != NULL)
        {
            free(*depend);
            *depend = NULL;
        }
        
        if (*package != NULL)
        {
            free(*package);
            *package = NULL;
        }
        return 0;
    }
    return 4;
}


/*
 * find_node()
 * 
 * In a depth first search manner, search the tree for a node that
 * has the same value as the one passed in.
 *
 * Returns: null if no node exists.
 */
node* find_node(node* current, char* value)
{
    if (strcmp(value, current->value) == 0)
        return current;

    for (int ii = 0; ii < ARRAYLEN; ii++)
    {
        if (current->children[ii] == NULL)
            return NULL;

        node* found = find_node(current->children[ii], value);
        if (found != NULL)
            return found;
    }
    return NULL;
}


node* print_tree(node* current, int tab_count)
{
    char buffer[BUFLEN];
    memset(buffer, ' ', BUFLEN);
    buffer[tab_count] = 0;
    strcat(buffer, " -> ");
    strcat(buffer, current->value);
    if (current->parents[0] != NULL)
    {
        strcat(buffer, "(");
        strcat(buffer, current->parents[0]->value);
        for (int ii = 1; ii < ARRAYLEN; ii++)
        {
            if (current->parents[ii] == NULL)
                break;

            strcat(buffer, ",");
            strcat(buffer, current->parents[ii]->value);
        }
        strcat(buffer, ")");
    }
    strcat(buffer, "\n");
    printf("%s", buffer);
    for (int ii = 0; current->children[ii] != NULL; ii++)
        print_tree(current->children[ii], tab_count + 2);
}


/*
 * init_node()
 * 
 * Create a new node, on success, the value copied into a new variable, 
 * and if a parent value is passed it it will be used to initialise the first 
 * element of the parents array.  
 * 
 * Returns: pointer to the initliased node.
 */
node* init_node(char* value, node* parent)
{
    node *w = malloc(sizeof(node));
    if (w == NULL)
        return NULL;

    strcpy(w->value, value);

    for (int ii = 0; ii < ARRAYLEN; ii++)
        w->children[ii] = NULL;

    for (int ii = 0; ii < ARRAYLEN; ii++)
        w->parents[ii] = NULL;

    w->parents[0] = parent;
    
    nodes_list[node_count++] = w;
    return w;
}


/*
 * add_parent()
 * 
 * Add the passed into parent value to this nodes (current's)
 * list of parents. Note, this makes it a graph, not a tree as 
 * each node can have mulitple parents.
 */
void add_parent(node* current, node* parent)
{
    for (int ii = 0; ii < ARRAYLEN; ii++)
    {
        if (current->parents[ii] == NULL)
        {
            current->parents[ii] = parent;
            return;
        }
    }
}


/* 
 * add_child
 * 
 * This adds either a new node onto the listo of children for the current 
 * node, or adds a pointer to the existing node that represents this child 
 * (dependency) node.
 * 
 * Return: on success, this returns the pointer to the child node, 
 * NULL otherwise.
 */
node* add_child(node *current, char *child_value, node *head)
{
    for (int jj = 0; jj < ARRAYLEN; jj++)
    {
        if (current->children[jj] == NULL)
        {
            node* child = find_node(head, child_value);
            if (child)
            {
                current->children[jj] = child;
                add_parent(child, current);
            }
            else
            {
                current->children[jj] = init_node(child_value, current);
            }
            return current->children[jj];
        }
    }
    return NULL;
}


/*
 * count_parents()
 * 
 * Recursive function to process, in a depth first manner, all 
 * the parents of the passed in node.
 * 
 * On completion, the uniques string will contain a list of packages 
 * that were found, separated by FAKE_SPACE for processing later.
 * 
 */
int count_parents(node* current, char* uniques)
{
    // dont include the head node.
    if (strcmp(current->value, "head") == 0)
        return 0;

    // dont include the leaf node.
    if (current->children[0] != NULL)
        if (strstr(uniques, current->value) == NULL)
        {
            strcat(uniques, current->value);
            strcat(uniques, FAKE_SPACE);
        }

    // then for each parent...
    int ii = 0;
    for (; ii < ARRAYLEN; ii++)
    {
        if (current->parents[ii] != NULL)
            count_parents(current->parents[ii], uniques);
        else
            break;
    }
    return ii;
}


int main(int argc, char **argv)
{
    char buffer[BUFLEN * 4] = { 0 };
    char* lines[BUFLEN] = { NULL };
    int nlines = 0;

    // the instructions say data will be provided in a cmdline (as a file).
    if (argc > 1)
    {
        printf("Reading in data from '%s'\n", argv[1]);

        FILE* fp = fopen(argv[1], "r");
        if (fp == NULL)
        {
            printf("Unable to read from '%s'\n", argv[1]);
            exit(1);
        }

        fread(buffer, sizeof(buffer), 1, fp);
        fclose(fp);
    }
    else 
    {
        // if no file found on cmdline, use copy of example data
        printf("Using default example data.\n");
        strcpy(buffer, FILE_CONTENTS);
    }

    char* line = strtok(buffer, "\n");
    while (line != NULL)
    {
        lines[nlines] = line;
        nlines++;
        line = strtok(NULL, "\n");
    }

    char* packages[ARRAYLEN] = { NULL };
    char* depends[ARRAYLEN] = { NULL };
    int pcount = 0;

    for (int ii=0; ii<nlines; ii++)
    {    
        char *line = lines[ii];
        
        char* package = NULL, *depend = NULL;
        if (my_split(line, &package, &depend) != 4)
        {
            //printf("Warning - malformed input line, skipping... \n");
            continue;
        }
#ifdef DEBUG_OUTPUT
        printf("Pair: %s, %s\n", package, depend);
#endif
        
        if (pcount == ARRAYLEN)
        {
            printf("Error - unable to handle more than %d pairings.\n", ARRAYLEN);
            exit(2);
        }

        packages[pcount] = package;
        depends[pcount] = depend;
        pcount++;
    }

    node* head = init_node("head", NULL);
    node* w = head;
    for (int ii = 0; ii < pcount; ii++)
    {
#ifdef DEBUG_OUTPUT
        printf("Adding pair into tree (%s, %s)\n", packages[ii], depends[ii]);
#endif
        node* f = find_node(w, packages[ii]);
        if (f)
        {
            add_child(f, depends[ii], head);
        }
        else
        {
            node *c = add_child(head, packages[ii], head);
            add_child(c, depends[ii], head);
        }
    }
#ifdef DEBUG_OUTPUT
    print_tree(head, 4);
#endif

    float max = 0;
    char* answer = NULL;

    for (int ii = 0; ii < pcount; ii++)
    {
        node* n = find_node(head, depends[ii]);
        if (n->children[0] == NULL)
        {
            // start with the leave nodes...
            char unique_parents[BUFLEN*4] = { 0 };
            int direct = count_parents(n, &unique_parents[0]);

            int transitive = 0;
            char* space = strtok(unique_parents, FAKE_SPACE);
            while (space != NULL)
            {
                transitive++;
                space = strtok(0, FAKE_SPACE);
            }

#ifdef DEBUG_OUTPUT
            printf("Ratio for '%s' = %d/%d = %f.\n", n->value, transitive, direct, (float)transitive/direct);
#endif
            if ((float)transitive / direct > max)
            {
                max = (float)transitive / direct;
                answer = n->value;
            }
        }

    }

    printf("The answer is package '%s'.\n", answer);

    for (int ii = 0; ii < node_count; ii++)
    {
        free(nodes_list[ii]);
        nodes_list[ii] = NULL;
    }
    head = NULL;

    if (packages != NULL)
    {
        for (int ii=0; ii<pcount; ii++)
            free(packages[ii]);
    }

    if (depends != NULL)
    {
        for (int ii=0; ii<pcount; ii++)
            free(depends[ii]);
    }

}

