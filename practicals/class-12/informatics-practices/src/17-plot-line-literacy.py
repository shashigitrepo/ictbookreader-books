#: id: ip12-17
#: group: plots
#: title: Take data from an open source (India's literacy rate in the Census of India, 1951–2011), and draw a line plot with title, axis labels and markers; save the plot as an image.
#: title_hi: खुले स्रोत से डेटा (भारत की जनगणना 1951–2011 में साक्षरता दर) लेकर शीर्षक, अक्ष लेबल और मार्कर के साथ लाइन प्लॉट बनाइए; प्लॉट को चित्र के रूप में सहेजिए।
#: syllabus: yes
#: note: Data: literacy rate (%) of India, Census of India 1951–2011.
# Program 17: Line plot of India's literacy rate (Census of India)
import matplotlib.pyplot as plt

years = [1951, 1961, 1971, 1981, 1991, 2001, 2011]
literacy = [18.33, 28.30, 34.45, 43.57, 52.21, 64.84, 74.04]

plt.plot(years, literacy, marker="o", color="green", linestyle="-")
plt.title("Literacy Rate of India (Census 1951-2011)")
plt.xlabel("Census year")
plt.ylabel("Literacy rate (%)")
plt.grid(True)
plt.savefig("literacy.png")
print("Plot saved as literacy.png")
plt.show()
