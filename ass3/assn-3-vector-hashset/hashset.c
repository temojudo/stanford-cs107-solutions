#include "hashset.h"
#include <assert.h>
#include <stdlib.h>
#include <string.h>

void HashSetNew(hashset *h, int elemSize, int numBuckets, HashSetHashFunction hashfn, 
				HashSetCompareFunction comparefn, HashSetFreeFunction freefn) {

	h->numBuckets = numBuckets;
	h->hashSetFun = hashfn;
	h->compareFun = comparefn;
	h->logLen = 0;

	h->buckets = malloc(sizeof(vector *) * numBuckets);
	for (int i = 0; i < numBuckets; i++) {
		h->buckets[i] = malloc(sizeof(vector));
		VectorNew(h->buckets[i], elemSize, freefn, 13);
	}
}

void HashSetDispose(hashset *h) {
	for (int i = 0; i < h->numBuckets; i++) {
		VectorDispose(h->buckets[i]);
		free(h->buckets[i]);
	}
	free(h->buckets);
}

int HashSetCount(const hashset *h) { 
	return h->logLen; 
}

void HashSetMap(hashset *h, HashSetMapFunction mapfn, void *auxData) {
	for (int i = 0; i < h->numBuckets; i++)
		for (int j = 0; j < h->buckets[i]->logLen; j++)
			mapfn(VectorNth(h->buckets[i], j), auxData);
}

void HashSetEnter(hashset *h, const void *elemAddr) {
	int pos = h->hashSetFun(elemAddr, h->numBuckets);
	int k = VectorSearch(h->buckets[pos], elemAddr, h->compareFun, 0, false);
	if (k != -1) {
		VectorReplace(h->buckets[pos], elemAddr, k);
		return;
	}
	VectorAppend(h->buckets[pos], elemAddr);
	h->logLen++;
}

void *HashSetLookup(const hashset *h, const void *elemAddr) {
	int pos = h->hashSetFun(elemAddr, h->numBuckets); 
	int i = VectorSearch(h->buckets[pos], elemAddr, h->compareFun, 0, false); 
	if (i == -1) return NULL;
	return VectorNth(h->buckets[pos], i);
}
