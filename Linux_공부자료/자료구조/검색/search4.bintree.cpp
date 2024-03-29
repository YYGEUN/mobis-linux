#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <memory.h>

#define MAX_WORD_LENGTH 20
#define MAX_MEAN_LENGTH 200

typedef struct {   //영어사전 항목의 구조 정의
	char word[MAX_WORD_LENGTH];
	char mean[MAX_MEAN_LENGTH];
}element;

typedef struct treeNode {   //영어사전 이진트리의 노드 구조 정의
	element key;
	struct treeNode *left;
	struct treeNode *right;
}treeNode;

treeNode* insertKey(treeNode *p, element key)  
{  //포인터 p가 가리키는 노드와 비교하여 항목 key를 삽입하는 연산
	treeNode *newNode;
	int compare;
	if (p == NULL) {  //삽입할 자리에 새 노드를 구성하여 연결
		newNode = (treeNode*)malloc(sizeof(treeNode));
		newNode->key = key;
		newNode->left = NULL;
		newNode->right = NULL;
		return newNode;
	}
	else {   //이진트리에서 삽입할 자리 탐색
		compare = strcmp(key.word, p->key.word);
		if (compare < 0)      p->left = insertKey(p->left, key);
		else if (compare > 0)  p->right = insertKey(p->right, key);
		else  printf("\n 이미 같은 단어가 있습니다! \n");

		return p;  //삽입한 자리를 반환
	}
}

void insert(treeNode** root, element key)
{
	*root = insertKey(*root, key);
}

void deleteNode(treeNode *root, element key)
{  //root 노드 부터 탐색하여 key와 같은 노드를 찾아  삭제하는 연산
	treeNode *parent, *p, *succ, *succ_parent;
	treeNode *child;

	parent = NULL;
	p = root;
	while ((p != NULL) && (strcmp(p->key.word, key.word) != 0)) {
		parent = p;
		if (strcmp(key.word, p->key.word)<0)  p = p->left;
		else  p = p->right;
	}
	if (p == NULL) {   //삭제할 노드가 없는 경우
		printf("\n 삭제할 단어가 사전에 없습니다!!");
		return;
	}
	// 삭제할 노드가 단말노드인 경우
	if ((p->left == NULL) && (p->right == NULL)) {
		if (parent != NULL) {
			if (parent->left == p) parent->left = NULL;
			else parent->right = NULL;
		}
		else root = NULL;
	}
	// 삭제할 노드가 한 개의 자식노드를 가진 경우
	else if ((p->left == NULL) || (p->right == NULL)) {
		if (p->left != NULL) child = p->left;
		else  child = p->right;

		if (parent != NULL) {
			if (parent->left == p) parent->left = child;
			else  parent->right = child;
		}
		else root = child;
	}
	// 삭제할 노드가 두 개의 자식노드를 가진 경우
	else {
		succ_parent = p;
		succ = p->right;
		while (succ->left != NULL) {
			succ_parent = succ;
			succ = succ->left;
		}
		if (succ_parent->left == succ)
			succ_parent->left = succ->right;
		else   succ_parent->right = succ->right;

		p->key = succ->key;
		p = succ;
	}
	free(p);
}

treeNode* searchBST(treeNode* root, element key)
{  //이진 탐색 트리에서 키값이 key인 노드의 위치를 탐색하는 연산
	treeNode* p;
	int compare;
	p = root;

	while (p != NULL) {
		compare = strcmp(key.word, p->key.word);
		if (compare < 0)      p = p->left;
		else if (compare > 0)  p = p->right;
		else {
			printf("\n찾은 단어 : %s", p->key.word);
			return p;
		}
	}
	return p;
}

void displayInorder(treeNode* root)
{   //이진 탐색 트리를 중위 순회하면서 출력하는 연산
	if (root) {
		displayInorder(root->left);
		printf("\n%s : %s", root->key.word, root->key.mean);
		displayInorder(root->right);
	}
}

void menu()
{
	printf("\n*---------------------------*");
	printf("\n\t1 : 출력");
	printf("\n\t2 : 입력");
	printf("\n\t3 : 삭제");
	printf("\n\t4 : 검색");
	printf("\n\t5 : 종료");
	printf("\n*---------------------------*\n  ");
}

void main()
{
	char choice;
	element e;
	treeNode *root = NULL, *temp = NULL;

	do {
		menu();
		choice = getchar(); getchar();

		switch (choice - '0') {
		case 1:
			printf("\t[사전 출력]");
			displayInorder(root); printf("\n\t[사전 끝]\n");
			break;
		case 2:
			printf("\n[단어 입력] 단어를 입력하세요 : ");
			gets_s(e.word);
			printf("\n[단어입력] 단어 뜻을 입력하세요 : ");
			gets_s(e.mean);
			insert(&root, e);
			break;
		case 3:
			printf("\n[단어 삭제] 삭제할 단어 : ");
			gets_s(e.word);
			deleteNode(root, e);
			break;
		case 4:
			printf("\n[단어 검색] 검색할 단어 : ");
			gets_s(e.word);
			temp = searchBST(root, e);
			if (temp != NULL)
				printf("\n단어 뜻 : %s", temp->key.mean);
			else printf("\n사전에 없는 단어입니다.");
			break;
		}
	} while ((choice - '0') != 5);

}