from datetime import datetime

filename="river_stations.txt"

river_stations = {
    'Sungai Klang KL': {'state': 'Selangor', 'wqi': 68.3, 'status': ''},
    'Sungai Muar': {'state': 'Johor', 'wqi': 54.1, 'status': ''},
    'Sungai Pinang': {'state': 'Pulau Pinang', 'wqi': 42.7, 'status': ''},
    'Sungai Kelantan': {'state': 'Kelantan', 'wqi': 95.4, 'status': ''},
    'Sungai Perak': {'state': 'Perak', 'wqi': 80.2, 'status': ''},
}

def classify_wqi(wqi):
    if wqi > 92.7:
        return 'Class I - Clean'
    elif wqi > 76.5:
        return 'Class II - Slightly Polluted'
    elif wqi > 51.9:
        return 'Class III - Moderately Polluted'
    elif wqi > 31.0:
        return 'Class IV - Polluted'
    else:
        return 'Class V - Heavily Polluted'

def classify_all_stations():
    for name in river_stations:
        wqi = river_stations[name]['wqi']
        river_stations[name]['status'] = classify_wqi(wqi)

def print_station_table():
    print(f"\n{'Station':<20}{'State':<15}{'WQI':<10}{'Status':<30}")
    print('-' * 75)
    for name, station in river_stations.items():
        print(f"{name:<20}{station['state']:<15}{station['wqi']:<10.1f}{station['status']:<30}")

def add_update_station():
    name = input("Enter station name: ")
    state = input("Enter state: ")
    while True:
        try:
            wqi = float(input("Enter WQI value: "))
            break
        except ValueError:
            print("Invalid WQI. Please enter a numeric value.")
    
    if name in river_stations:
        river_stations[name]['state'] = state
        river_stations[name]['wqi'] = wqi
        print(f"Station {name} updated with new WQI: {wqi}.")
    else:
        river_stations[name] = {'state': state, 'wqi': wqi, 'status': ''}
        print(f"New station {name} added.")
    classify_all_stations()

def menu():
        print("\n======= Main Menu =======")
        print("1. Classify All Stations")
        print("2. Add / Update Station")
        print("3. Log Monitoring Reading")
        print("4. Trend Analysis")
        print("5. Export Report")
        print("6. Load Data / Refresh")
        print("0. Exit")

reading_log=[]

def log_monitoring():
    classify_all_stations()

    while(True):
        river_name = input("Enter River Name (Enter 'done' to return to main menu): ").strip()
        if river_name.lower()=='done':
            break
        elif river_name not in river_stations:
            print(f"Error: Station {river_name} not found.")
        else:
            wqi=float(input("Enter WQI Reading: "))
            while(True):
                try:
                    if wqi<0 and wqi>100:
                        print("Error. WQI value must be between 0 and 100.")
                        continue
                    else: 
                        river_stations[river_name]['wqi']=wqi
                        classify_all_stations()
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        reading_log.append((timestamp, river_name, wqi))
                        print(f"Logged WQI {wqi} for {river_name} at {timestamp}.")
                        break
                except ValueError:
                    print("Invalid WQI Value, please enter again.")
                    continue

    if all(river['wqi'] >= 51.9 for river in river_stations.values()):
        print("\nAll monitored rivers are within acceptable quality levels.")
    else:
        print( "\n"+ "="*50)
        for river_name, river in river_stations.items():
            if river['wqi'] < 51.9:
                print(f"[!] ALERT: {river_name} in {river['state']} is {river['status']} (WQI: {river['wqi']})\n")

    if not reading_log:
        print("\nNo readings have been logged yet.\n")
    else:
        print("\n========== Monitoring Log: ==========")
        for entry in reading_log:
            print(f"{entry[0]} - {entry[1]}: WQI {entry[2]}")
        print("="*40 + "\n")

class RiverStation:
        def __init__(self, name, state, wqi):
            self.name = name
            self.state = state
            self.wqi = wqi
        
        def get_class_label(self):
            return classify_wqi(self.wqi)
        
        def display_summary(self):
            print(f"{self.name} | {self.state} | WQI: {self.wqi} | {self.get_class_label()}")
        
def show_river_station_objects():
    print("\n--- RiverStation Object Summaries ---")
    station_names = list(river_stations.keys())[:2]
    for name in station_names:
        info = river_stations[name]
        station_obj = RiverStation(name, info['state'], info['wqi'])
        station_obj.display_summary()

def average_wqi_by_state():
    state_totals = {}
    state_counts = {}
    state_averages = {}

    for station in river_stations.values():
        state = station['state']
        state_totals[state] = state_totals.get(state, 0) + station['wqi']
        state_counts[state] = state_counts.get(state, 0) + 1

    for state in state_totals:
        state_averages[state] = state_totals[state] / state_counts[state]

    print("\n--- Average WQI by State ---")
    for state, avg in sorted(state_averages.items(), key=lambda x: x[1], reverse=True):
        print(f"{state:<20}: {avg:.2f}")

def calculate_historical_trends():
    trends={}

    for _,station,wqi in reading_log:
        trends.setdefault(station,[]).append(wqi)

    for s, r in trends.items():
        if not len(r) >= 2:
            print("\n"+"="*50 +"\n")
            print("Insufficient data for trend analysis. Please log more readings.")
            return
        else:
            improvement = {s:max(r)-min(r)}
            best = max(improvement, key=improvement.get)
            worst = min(improvement, key=improvement.get)

            print("\n"+"="*50 +"\n")
            print(f"Greatest improvement: {best} (+{improvement[best]:.2f})")
            print(f"Least improvement: {worst} ({improvement[worst]:.2f})")

def classification_count():
    classify_all_stations()

    classes_count = {"Class I - Clean": 0, "Class II - Slightly Polluted": 0, "Class III - Moderately Polluted": 0, "Class IV - Polluted": 0, "Class V - Heavily Polluted": 0}

    for river in river_stations.values():
        classes_count[river['status']] += 1
    
    print("\n"+"="*50)
    print("State Counts by Classes")
    print("="*50+"\n")
    print(f"{'Class':<35}{'Count'}")
    for classes, count in classes_count.items():
        print(f"{classes:<35}{count}")

def trendAnalysis():
    print("\n======= Trend Analysis Report =======")
    show_river_station_objects()
    average_wqi_by_state()
    calculate_historical_trends()
    classification_count()
    print("="*50)


def writefile():
    classify_all_stations()
    try:
        with open(filename,"w") as file:
            for river, data in river_stations.items():
                file.write(f"{river}, {data['state']}, {data['wqi']}, {data['status']}\n")
            print(f"\nData written into {filename}\n")
    except PermissionError:
        print("PermissionError: Write failed. Access to the file is restricted.")

def readfile():
    try:
        file = open(filename, "r")
        stations_data = file.readlines()
        for line in stations_data:
            name, state, wqi, status = line.strip().split(", ")
            try:
                river_stations[name] = {'state': state, 'wqi': float(wqi), 'status': status}
            
            except ValueError:
                print(f"ValueError: Invalid WQI value in line: {line.strip()}")
                continue
        classify_all_stations()
        print(f"\nThe file {filename} loaded successfully.\n")

    except FileNotFoundError:
        print(f"FileNotFoundError: The file {filename} could not be found.")

while True:
    menu()
    option = input("Please select an option: ")
    
    match option:
        case '1':
            print("\n"+"="*50 +"\n")
            classify_all_stations()
            print_station_table()
        
        case '2':
            print("\n"+"="*50 +"\n")
            add_update_station()
        
        case '3':
            print("\n"+"="*50 +"\n")
            log_monitoring()
            
        case '4':
            trendAnalysis()

        case '5':
            print("\n"+"="*50 +"\n")
            writefile()

        case '6':
            readfile()
            
        case '0':
            print("\n"+"="*50 +"\n")
            print("Exiting the RQM System. Thanks for using it!")
            print("\n"+"="*50 +"\n")
            break
        
        case _:
            print("\nInvalid input. Please try again.")
            continue