import csv

stations = dict()

with open('Hubway_Stations_as_of_July_2017.csv', 'r') as csvfile:

	spamreader = csv.reader(csvfile)

	next(spamreader)

	for row in csvfile:

		row = list(map(str.strip, row.split(',')))

		stations[row[1].strip()] = row

with open('201807-bluebikes-tripdata.csv', 'r') as csvfile:

	spamreader = csv.reader(csvfile)

	next(spamreader)

	for row in csvfile:

		row = row.split(',')

		name = row[4].replace('/', 'at')
		lat = row[5]
		lng = row[6]

		try:
			if len(stations[name]) < 8:
				print("banana")
				stations[name].append(int(row[3]))
		except KeyError as e:
			pass
		else:
			pass

print(stations)

with open('Hubway_Stations_Parsed.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow('Number,Name,Latitude,Longitude,District,Public,Total docks,Id'.split(','))
    for s in stations.values():
    	spamwriter.writerow(s)
