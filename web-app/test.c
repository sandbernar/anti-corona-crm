#include <stdio.h>

//[][][][] [][][][]
typedef struct s_string_array {
	int size;
	char** array;
} string_array;

// a = [1, 2, 3]
// a = [1][2][3][4]

typedef struct s_list {
	char *name;
	int age;
	struct s_list *next;
} list;

//[i, *p] -> [i, *p] -> NULL
//a = [*p, *p]
//b = [][][]
//b = [a1, a2, b3]
// b[2] 
int main() {
	string_array w;

	w.size = 2;


	string_array *s;

	s = (string_array*)malloc(sizeof(string_array));
	s->size = 3;
	//[p1, p2, p3]
	//p1[][][]
	//p2[][][]
	//p3[][][]
	s->array = (char**)malloc(sizeof(char*) * 3);
	s->array[0] = strdup("hello");
	s->array[1] = strdup("hello");
	s->array[2] = strdup("hello");
	free(s);
	s = NULL;
}
