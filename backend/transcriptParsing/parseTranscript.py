import pdfplumber
import re
from collections import defaultdict
import sys

def groupCourseToIndexes(termIndexes, levelIndexes, courseIndexes):
    
    terms = defaultdict(set)

    if not termIndexes or not levelIndexes or not courseIndexes:
        return terms

    courseIndex = 0
    termIndex = 0

    while (termIndex + 1 < len(termIndexes)):
        
        current_term_index = termIndexes[termIndex + 1].start(0)

        while (courseIndex < len(courseIndexes) and courseIndexes[courseIndex].start(0) < current_term_index):
            terms[termIndexes[termIndex].group(0)].add(courseIndexes[courseIndex].group(0))
            courseIndex += 1

        termIndex += 1

    terms[termIndexes[-1].group(0)] = set([x.group(0) for x in courseIndexes[courseIndex:]])

    for term, courses in terms.items():
        print(term, courses)

    return terms

def getCoursesPerTerm(filename):

    pdf_text = ""

    with pdfplumber.open(filename) as pdf:   
        for page in pdf.pages:
            pdf_text += page.extract_text()

    termRegex = '(Fall|Winter|Spring)\s+(\d{4})'
    levelRegex = 'Level:\s+(\d\w)'
    courseRegex = '([A-Z]{2,})\s+(\d{1,3}\w?)\s'

    termIterator = re.finditer(termRegex, pdf_text)
    termIndexes = []
    for term in termIterator:
        termIndexes.append(term)

    levelIterator = re.finditer(levelRegex, pdf_text)
    levelIndexes = []
    for level in levelIterator:
        levelIndexes.append(level)

    courseIterator = re.finditer(courseRegex, pdf_text)
    courseIndexes = []
    for course in courseIterator:
        courseIndexes.append(course)

    return groupCourseToIndexes(termIndexes, levelIndexes, courseIndexes)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid Command Arguments")
        print("Usage: ", sys.argv[0], " <pdf transcript name>")
        exit(1)

    getCoursesPerTerm(sys.argv[1])