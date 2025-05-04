from mrjob.job import MRJob
import re
import sys

'''
python word_count.py 11-0.txt > output.txt
'''

WORD_RE = re.compile(r"\b\w+\b")

class MRWordCount(MRJob):
    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield word.lower(), 1

    def reducer(self, word, counts):
        total = sum(counts)
        yield word, sum(counts)

if __name__ == '__main__':
    MRWordCount.run()

