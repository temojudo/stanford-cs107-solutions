#include "vector.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

void VectorNew(vector *v, int elemSize, VectorFreeFunction freeFn, int initialAllocation) {
    v->allocLen = initialAllocation;
    v->elemSize = elemSize;
    v->logLen = 0;
    v->data = malloc(elemSize * initialAllocation);
    v->vecFreeFun = freeFn;
}

void VectorDispose(vector *v) {
    if (v->vecFreeFun == NULL) return;
    for (int i = 0; i < v->logLen; i++)
        v->vecFreeFun(VectorNth(v, i));
}

int VectorLength(const vector *v) {
    return v->logLen;
}

void *VectorNth(const vector *v, int position) {
    return (char *)v->data + position * v->elemSize;
}

void VectorReplace(vector *v, const void *elemAddr, int position) {
    void * currElem = VectorNth(v, position);
    if (v->vecFreeFun != NULL) v->vecFreeFun(currElem);
    memmove(currElem, elemAddr, v->elemSize);
}

void VectorInsert(vector *v, const void *elemAddr, int position) {
    if (v->logLen == v->allocLen) {
        v->data = realloc(v->data, 2 * v->allocLen * v->elemSize + 1);
        v->allocLen = 2 * v->allocLen + 1;
    }

    memmove(VectorNth(v, position + 1), VectorNth(v, position), (v->logLen - position) * v->elemSize);
    memmove(VectorNth(v, position), elemAddr, v->elemSize);
    v->logLen++;
}

void VectorAppend(vector *v, const void *elemAddr) {
    VectorInsert(v, elemAddr, v->logLen);
}

void VectorDelete(vector *v, int position) {
    memmove(VectorNth(v, position), VectorNth(v, position + 1), (v->logLen - position - 1) * v->elemSize);
    v->logLen--;
} 

void VectorSort(vector *v, VectorCompareFunction compare) {
    qsort(v->data, v->logLen, v->elemSize, compare);
}

void VectorMap(vector *v, VectorMapFunction mapFn, void *auxData) {
    for (int i = 0; i < v->logLen; i++)
        mapFn(VectorNth(v, i), auxData);
}

static const int kNotFound = -1;
int getBinarySearch(const vector *v, int start, const void *key, VectorCompareFunction searchFn) {
    int end = v->logLen - 1;
    while (start <= end) {
        int mid = (start + end) / 2;
        if (searchFn(key, VectorNth(v, mid)) == 0) return mid;
        if (searchFn(key, VectorNth(v, mid)) > 0) start = mid + 1;
                                             else end = mid - 1;
    }
    return kNotFound;
}

int getLinearSearch(const vector *v, int start, const void *key, VectorCompareFunction searchFn) {
    for (int i = start; i < v->logLen; i++)
        if (searchFn(VectorNth(v, i), key) == 0) return i;
    return kNotFound;
}

int VectorSearch(const vector *v, const void *key, VectorCompareFunction searchFn, int startIndex, bool isSorted) {
    if (isSorted) return getBinarySearch(v, startIndex, key, searchFn);
    return getLinearSearch(v, startIndex, key, searchFn); 
} 
