#: id: cs12-12
#: group: text-files
#: title: Write a function that counts the lines starting with 'T' and the number of times the word "the" (any case) occurs in a text file.
#: title_hi: एक फ़ंक्शन लिखिए जो टेक्स्ट फ़ाइल में 'T' से शुरू होने वाली पंक्तियाँ और "the" शब्द (किसी भी केस में) कितनी बार आया, गिने।
#: files: story.txt
# Program 12: Lines starting with 'T' and count of the word "the"

def count_in_file(filename):
    t_lines = 0
    the_count = 0
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("T"):
                t_lines += 1
            for word in line.split():
                if word.strip(".,").lower() == "the":
                    the_count += 1
    return t_lines, the_count


lines, words = count_in_file("story.txt")
print("Lines starting with 'T':", lines)
print('The word "the" occurs', words, "times")
