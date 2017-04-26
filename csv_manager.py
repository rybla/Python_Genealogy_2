import csv

def create_csv(labels,data_array):
    


with open('names.csv', 'w+') as csvfile:
    fieldnames = ['Id','Label', 'Source', 'Target']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'Id': '1', 'Label': 'Node 1', 'Source': '1', 'Target': '2, 3'})
    writer.writerow({'Id': '2', 'Label': 'Node 2', 'Source': '2', 'Target': '1'})
    writer.writerow({'Id': '3', 'Label': 'Node 3', 'Source': '3', 'Target': '2'})