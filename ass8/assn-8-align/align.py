#!/usr/bin/env python

import random # for seed, random
import sys    # for stdout

################################### TEST PART ##################################

# Tests align strands and scores
# Parameters types:
#    score          =  int   example: -6
#    plusScores     = string example: "  1   1  1"
#    minusScores    = string example: "22 111 11 "
#    strandAligned1 = string example: "  CAAGTCGC"
#    strandAligned2 = string example: "ATCCCATTAC"
#
#   Note: all strings must have same length
def test(score, plusScores, minusScores, strandAligned1, strandAligned2):
    print("\n>>>>>>START TEST<<<<<<")

    if testStrands(score, plusScores, minusScores, strandAligned1, strandAligned2):
        sys.stdout.write(">>>>>>>Test SUCCESS:")
        sys.stdout.write("\n\t\t" + "Score: "+str(score))
        sys.stdout.write("\n\t\t+ " + plusScores)
        sys.stdout.write("\n\t\t  " + strandAligned1)
        sys.stdout.write("\n\t\t  " + strandAligned2)
        sys.stdout.write("\n\t\t- " + minusScores)
        sys.stdout.write("\n\n")
    else:
        sys.stdout.write("\t>>>>!!!Test FAILED\n\n")

# converts character score to int
def testScoreToInt(score):
    if score == ' ':
        return 0
    return int(score)

# computes sum of scores
def testSumScore(scores):
    result = 0
    for ch in scores:
        result += testScoreToInt(ch)
    return result

# test each characters and scores
def testValidateEach(ch1, ch2, plusScore, minusScore):
    if ch1 == ' ' or ch2 == ' ':
        return plusScore == 0 and minusScore == 2
    if ch1 == ch2:
        return plusScore == 1 and minusScore == 0
    return plusScore == 0 and minusScore == 1

# test and validates strands
def testStrands(score, plusScores, minusScores, strandAligned1, strandAligned2):
    if len(plusScores) != len(minusScores) or len(minusScores) != len(strandAligned1) or len(strandAligned1) != len(
            strandAligned2):
        sys.stdout.write("Length mismatch! \n")
        return False

    if len(plusScores) == 0:
        sys.stdout.write("Length is Zero! \n")
        return False

    if testSumScore(plusScores) - testSumScore(minusScores) != score:
        sys.stdout.write("Score mismatch to score strings! TEST FAILED!\n")
        return False
    for i in range(len(plusScores)):
        if not testValidateEach(strandAligned1[i], strandAligned2[i], testScoreToInt(plusScores[i]),
                                testScoreToInt(minusScores[i])):
            sys.stdout.write("Invalid scores for position " + str(i) + ":\n")
            sys.stdout.write("\t char1: " + strandAligned1[i] + " char2: " +
                             strandAligned2[i] + " +" + str(testScoreToInt(plusScores[i])) + " -" +
                             str(testScoreToInt(minusScores[i])) + "\n")
            return False

    return True

######################## END OF TEST PART ######################################
def findOptimalAlignment(strand1, strand2):
	helper = {}
	return findOptimalAlignmentHelper(strand1, strand2, helper)

def findOptimalAlignmentHelper(strand1, strand2, helper):
	if len(strand1) == 0:
		return [len(strand2) * -2, len(strand2) * ' ', strand2]
	
	if len(strand2) == 0:
		return [len(strand1) * -2, strand1, len(strand1) * ' ']

	if helper.has_key(strand1 + '-' + strand2):
		return helper[strand1 + '-' + strand2]

	withBoth = findOptimalAlignmentHelper(strand1[1:], strand2[1:], helper)
	if strand1[0] == strand2[0]:
		helper[strand1 + '-' + strand2] = withBoth[0] + 1, strand1[0] + withBoth[1], strand2[0] + withBoth[2]
		return [withBoth[0] + 1, strand1[0] + withBoth[1], strand2[0] + withBoth[2]]
	
	ans = [withBoth[0] - 1, strand1[0] + withBoth[1], strand2[0] + withBoth[2]]
	withoutFirst = findOptimalAlignmentHelper(strand1, strand2[1:], helper)
	if withoutFirst[0] - 2 > ans[0]:
		ans = [withoutFirst[0] - 2, ' ' + withoutFirst[1], strand2[0] + withoutFirst[2]]

	withoutSecond = findOptimalAlignmentHelper(strand1[1:], strand2, helper)
	if withoutSecond[0] - 2 > ans[0]:
		ans = [withoutSecond[0] - 2, strand1[0] + withoutSecond[1], ' ' + withoutSecond[2]]

	helper[strand1 + '-' + strand2] = ans
	return ans


# Utility function that generates a random DNA string of
# a random length drawn from the range [minlength, maxlength]
def generateRandomDNAStrand(minlength, maxlength):
	assert minlength > 0, \
	       "Minimum length passed to generateRandomDNAStrand" \
	       "must be a positive number" # these \'s allow mult-line statements
	assert maxlength >= minlength, \
	       "Maximum length passed to generateRandomDNAStrand must be at " \
	       "as large as the specified minimum length"
	strand = ""
	length = random.choice(xrange(minlength, maxlength + 1))
	bases = ['A', 'T', 'G', 'C']
	for i in xrange(0, length):
		strand += random.choice(bases)
	return strand

def calcScores(strand1, strand2):
	plusAndMinus = ['', '']
	for x in xrange(len(strand1)):
		if strand1[x] == ' ' or strand2[x] == ' ':
			plusAndMinus[0] += ' '
			plusAndMinus[1] += '2'
		elif strand1[x] == strand2[x]:
			plusAndMinus[0] += '1'
			plusAndMinus[1] += ' '
		else:
			plusAndMinus[0] += ' '
			plusAndMinus[1] += '1'
	
	return plusAndMinus


# Method that just prints out the supplied alignment score.
# This is more of a placeholder for what will ultimately
# print out not only the score but the alignment as well

def printAlignment(score, out = sys.stdout):
	out.write("Optimal alignment score is " + str(score) + "\n")


# Unit test main in place to do little more than
# exercise the above algorithm.  As written, it
# generates two fairly short DNA strands and
# determines the optimal alignment score.
#
# As you change the implementation of findOptimalAlignment
# to use memoization, you should change the 8s to 40s and
# the 10s to 60s and still see everything execute very
# quickly.

def main():
	while (True):
		sys.stdout.write("Generate random DNA strands? ")
		if  sys.stdin.readline() == "no\n": break
		strand1 = generateRandomDNAStrand(40, 60)
		strand2 = generateRandomDNAStrand(40, 60)
		sys.stdout.write("Aligning these two strands: " + strand1 + "\n")
		sys.stdout.write("                            " + strand2 + "\n")

		alignment = findOptimalAlignment(strand1, strand2)
		printAlignment(alignment[0])
		plusAndMinus = calcScores(alignment[1], alignment[2])
		test(alignment[0], plusAndMinus[0], plusAndMinus[1], alignment[1], alignment[2])

if __name__ == "__main__":
  main()