class FreqList:
    def __init__(self, csv_list):
        self.csv_list = csv_list

    def save(self, filename, count=None):
        file = open(filename, "+w")

        if count == None:
            count = len(self.csv_list)

        for i in range(count):
            file.write( f"{self.csv_list[i][0]}, {self.csv_list[i][1]}\n" )