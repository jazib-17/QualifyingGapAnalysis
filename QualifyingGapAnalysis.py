'''
Driver Qualifying Teammate Gap Analysis

Compare the fastest qualifyinh laptimes of 2 drivers and their teammates on a single
track for a specified range of years

Author: Jazib Ahmed
'''

from fastf1.plotting import get_team_name_by_driver, get_driver_names_by_team, get_driver_abbreviation
import fastf1
import matplotlib.pyplot as plt
from datetime import timedelta
import inflect

fastf1.Cache.enable_cache('fastf1_cache')

p = inflect.engine()

#-----------------------------------
# Change the variables here for different races/different drivers
startyear = 2022 # Which lap to start getting laptimes from
endyear = 2024 # Which lap to end getting laptimes from
race = "Monaco" # Set race here
driver1 = "Leclerc"
driver2 = "Hamilton"

# What color the columns should be set for each driver
driver_color = {
# Two colors:  [Text color, background color]
'Driver1': ['white','red'],
'Driver2': ['yellow','red'],
}

# Set the title and chart/font size for the analysis
chart_title = "Qualifying Difference for " + driver1 + "/" + driver2 + "\n against teammates (" + race + ")"
chartsize = (9,7)
fontsize = 12

#-----------------------------------


differences,differences2 = [],[]
positions1,positions2 = [],[]

def format_lap(laptime):
    # Format the average difference with a '+' or '-' sign at the front
    if laptime < timedelta(0):
        # If negative, format it with a '-' sign
        formatted_diff = "-" + f"{abs(laptime)}"[14:19]
    else:
        # If positive or zero, format it with a '+' sign
        formatted_diff = "+" + f"{laptime}"[14:19]
    return formatted_diff

for year in range(startyear,endyear+1):

    # Load data for each year
    session = fastf1.get_session(year, race, 'Qualifying')
    session.load(telemetry=False,weather=False,messages=False)

    # Get driver and teammate's abbreviations
    driver1abrev = get_driver_abbreviation(driver1, session)
    driver2abrev = get_driver_abbreviation(driver2, session)
    teammates = []
    for driver in [driver1,driver2]:
        target_team = get_team_name_by_driver(driver,session)

        drivers = get_driver_names_by_team(target_team,session)
        # Find teammate by checking who else is in the same team
        teammate = None
        for drv in drivers:
            if driver.lower() not in drv.lower():
                teammates.append(get_driver_abbreviation(drv, session))
                break

    # Getting fastest lap data for drivers and teammates
    driver1lap = session.laps.pick_drivers(driver1abrev).pick_fastest()
    teammate1lap = session.laps.pick_drivers(teammates[0]).pick_fastest()
    driver2lap = session.laps.pick_drivers(driver2abrev).pick_fastest()
    teammate2lap = session.laps.pick_drivers(teammates[1]).pick_fastest()

    # Calculating gap to teammate and qualifying position
    differences.append(format_lap(driver1lap['LapTime']-teammate1lap['LapTime']))
    differences2.append(format_lap(driver2lap['LapTime']-teammate2lap['LapTime']))
    positions1.append(p.ordinal(int(session.results[session.results['Abbreviation'] == driver1abrev]["Position"])))
    positions2.append(p.ordinal(int(session.results[session.results['Abbreviation'] == driver2abrev]["Position"])))

# Label for each driver's year on that track
row =  [driver1 + " (" + race + " " + str(year) + ")" for year in range(startyear,endyear+1)]
row += [driver2 + " (" + race + " " + str(year) + ")" for year in range(startyear,endyear+1)]

# Column names
column = ["Driver","Qualifying Position", "Gap to Teammate (Fastest Lap)"]

lap_data = list(zip(row, positions1+positions2,differences+differences2))  # Zipped driver names, position, gap
# Create a figure and axis
fig, ax = plt.subplots(figsize=chartsize)

# Separating each driver
lap_data.insert(len(differences), column)

# Extra settings for the chart
ax.axis("off")
fig.patch.set_facecolor('#2e2e2e')
fig.suptitle(chart_title,color="white",fontsize = 20)
# Create the table
table = ax.table(cellText=lap_data, colLabels=column, colWidths= [0.75]*3, loc='center', cellLoc='center')
table.scale(xscale=0.5, yscale=3)
table.auto_set_font_size(False)
table.set_fontsize(fontsize)

# Set colors for specific columns
for (i, j), cell in table.get_celld().items():
    cell.set_facecolor('black')
    cell.set_text_props(color='white')
    # Cells with driver 1's name
    if cell.get_text().get_text().startswith(driver1):
        cell.set_facecolor(driver_color['Driver1'][1])  # Background color
        cell.set_text_props( color=driver_color['Driver1'][0])  # Text properties
    # Cells with driver 2's name
    if cell.get_text().get_text().startswith(driver2):
        cell.set_facecolor(driver_color['Driver2'][1])  # Background color
        cell.set_text_props( color=driver_color['Driver2'][0])  # Text properties
    # Adjust color if qualifying gap was positive or negative
    if cell.get_text().get_text().startswith("+"):
        cell.set_facecolor('red')  # Background color
        cell.set_text_props( color='white')  # Text properties
    if cell.get_text().get_text().startswith("-"):
        cell.set_facecolor('green')  # Background color
        cell.set_text_props( color='white')  # Text properties


plt.tight_layout()
# Show the plot
plt.show()
