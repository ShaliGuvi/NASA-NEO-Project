import streamlit as st
import pandas as pd 
from datetime import datetime
import pymysql

st.title('🚀NASA Asteroid Tracker🌠')

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "🔍 Filter Criteria"  # default page

# Sidebar with buttons inside a container
with st.sidebar.container(border=True):
    st.header(":moon: **Asteroid Approaches**")
    if st.button("🔍 Filter Criteria"):
        st.session_state.page = "🔍 Filter Criteria"
    if st.button("📊 Queries"):
        st.session_state.page = "📊 Queries"

#database connection

connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "Wonder*555",  #your actual password of your sql profile
    database = "market" #it should match with the database created in mysql
    
)


cursor = connection.cursor()

# Render based on selected page
if st.session_state.page == "🔍 Filter Criteria":
    
    

    # Create 3 columns
    col1,spacer,col2,spacer2,col3 = st.columns([1.5, 0.1, 1.5, 0.1, 1.5])

    with col1:
        Slider2 = st.slider('Min Magnitude', 0.02009, 194.481, (0.02009, 194.481))
        Slider4 = st.slider('Min Estimated_diameter(km)', 0.000799015, 4.59785, (0.000799015, 4.59785))
        Slider5 = st.slider('Max Estimated_diameter(km)', 0.00178665, 10.2811, (0.00178665, 10.2811))

    with col2:
        Slider3 = st.slider('Relative Velocity_kmph Range', 1418.22, 190513.0, (1418.22, 190513.0))
        Slider1 = st.slider('Astronomical Units', 0.0000516453, 0.499952, (0.0000516453, 0.499952))
        Hazardous = st.selectbox("Only Show Potentially Hazardous", [0, 1])

    with col3:
        Start_date = st.date_input("Start Date", datetime(2024, 1, 1))
        End_date = st.date_input("End Date", datetime(2025, 4, 13))
        
        
      
        
        

    Filter_query = """
    SELECT 
        close_approaches.Neo_reference_id, 
        Close_approach_date, 
        Relative_velocity_kmph, 
        Astronomical,  
        Miss_distance_km, 
        Miss_distance_lunar, 
        Orbiting_body, 
        asteroids_data.ID, 
        Name, 
        Absolute_magnitude_h,
        Estimated_diameter_min_km, 
        Estimated_diameter_max_km, 
        Is_potentially_hazardous_asteroid
    FROM market.close_approaches 
    JOIN market.asteroids_data ON asteroids_data.ID = close_approaches.Neo_reference_id
    WHERE Astronomical BETWEEN %s AND %s
    AND Miss_distance_lunar BETWEEN %s AND %s
    AND Relative_velocity_kmph BETWEEN %s AND %s
    AND Estimated_diameter_min_km BETWEEN %s AND %s
    AND Estimated_diameter_max_km BETWEEN %s AND %s
    AND Is_potentially_hazardous_asteroid = %s
    AND Close_approach_date BETWEEN %s AND %s;
    """

    Values = (
        Slider1[0], Slider1[1],
        Slider2[0], Slider2[1],
        Slider3[0], Slider3[1],
        Slider4[0], Slider4[1],
        Slider5[0], Slider5[1],
        Hazardous,
        Start_date, End_date
    )

    if st.button("Filter"):
        cursor.execute(Filter_query, Values)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=[i[0] for i in cursor.description])
        df.drop_duplicates(inplace=True)
        st.dataframe(df)

elif st.session_state.page == "📊 Queries":
    
    Query = st.selectbox("Select your Query", ["1.Count how many times each asteroid has approached Earth",
                                        "2.Average velocity of each asteroid over multiple approaches",
                                        "3.List top 10 fastest asteroids",
                                        "4.Find potentially hazardous asteroids that have approached Earth more than 3 times",
                                        "5.Find the month with the most asteroid approaches",
                                        "6.Get the asteroid with the fastest ever approach speed",
                                        "7.Sort asteroids by maximum estimated diameter (descending)",
                                        "8.Asteroids whose closest approach is getting nearer over time",
                                        "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
                                        "10.List names of asteroids that approached Earth with velocity > 50,000 km/h",
                                        "11.Count how many approaches happened per month",
                                        "12.Find asteroid with the highest brightness (lowest magnitude value)",
                                        "13.Get number of hazardous vs non-hazardous asteroids",
                                        "14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
                                        "15.Find asteroids that came within 0.05 AU(astronomical distance)",
                                        "16.Find the Hazardous Asteroids approached earth in the monthh of Feb 2025",
                                        "17.Find the Hazardous Asteroid approached earth in the month of Feb 2025 with high speed",
                                        "18.Find the Non-Hazardous Asteroid approached earth with low speed along with Relative velocity",
                                        "19.Find the Hazardous Asteroid approached earth with lowest brightness",
                                        "20.Find the average distance between Asteroids and earth"])

    if Query == "3.List top 10 fastest asteroids":

        cursor.execute("""SELECT distinct Neo_reference_id, Relative_velocity_kmph
                            FROM market.close_approaches
                                order by Relative_velocity_kmph DESC
                                Limit 10;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "1.Count how many times each asteroid has approached Earth":
        
        cursor.execute("""SELECT Name, Count(*) AS count
                            FROM market.asteroids_data
                                group by Name;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "2.Average velocity of each asteroid over multiple approaches":
        
        cursor.execute("""SELECT Neo_reference_id, AVG(Relative_velocity_kmph)"Average velocity"
                            FROM market.close_approaches
                                group by Neo_reference_id, Relative_velocity_kmph;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "4.Find potentially hazardous asteroids that have approached Earth more than 3 times":
        
        cursor.execute("""SELECT Name, Count(*) AS count, Is_potentially_hazardous_asteroid
                            FROM market.asteroids_data
                                group by Name, Is_potentially_hazardous_asteroid
                                HAVING count>3 and Is_potentially_hazardous_asteroid=1;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "5.Find the month with the most asteroid approaches":
        
        cursor.execute("""SELECT 
                            month(Close_approach_date) AS Month,
                                COUNT(*) AS Approach_count
                                    FROM 
                                    close_approaches
                                    GROUP BY 
                                    Month
                                    ORDER BY 
                                    Approach_count DESC
                                    LIMIT 1;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "6.Get the asteroid with the fastest ever approach speed":
        
        cursor.execute("""SELECT Neo_reference_id, Relative_velocity_kmph 
                            FROM market.close_approaches
                                Group by Neo_reference_id, Relative_velocity_kmph
                                    Order by Relative_velocity_kmph DESC
                                        Limit 1;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "7.Sort asteroids by maximum estimated diameter (descending)":
        
        cursor.execute("""SELECT Name, Estimated_diameter_max_km
                            FROM market.asteroids_data
                                group by Name, Estimated_diameter_max_km
                                    Order by Estimated_diameter_max_km DESC;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "8.Asteroids whose closest approach is getting nearer over time":     
        
        cursor.execute("""SELECT DISTINCT Neo_reference_id, Close_approach_date, Miss_distance_km       			/*clarify*/
                            FROM market.close_approaches
                                order by Close_approach_date;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df) 

    elif Query == "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth": 
        
        cursor.execute("""SELECT DISTINCT a.Name, ap.Close_approach_date, ap.Miss_distance_km
                                FROM market.asteroids_data a
                                    JOIN market.close_approaches ap
                                    ON a.ID = ap.Neo_reference_id;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df) 

    elif Query == "10.List names of asteroids that approached Earth with velocity > 50,000 km/h": 
        
        cursor.execute("""SELECT DISTINCT a.Name
                            FROM market.asteroids_data a
                                JOIN market.close_approaches ap ON a.ID = ap.Neo_reference_id
                                    Where ap.Relative_velocity_kmph > 50000;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df) 

    elif Query == "11.Count how many approaches happened per month": 
        
        cursor.execute("""SELECT DATE_FORMAT(Close_approach_date, '%Y-%M') AS Month,
                            count(*) AS total_approaches
                                FROM market.close_approaches
                                    group by DATE_FORMAT(Close_approach_date, '%Y-%M')
                                        order by Month;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "12.Find asteroid with the highest brightness (lowest magnitude value)": 
        
        cursor.execute("""SELECT Name, Absolute_magnitude_h
                            FROM market.asteroids_data
                                order by Absolute_magnitude_h ASC
                                    Limit 1;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "13.Get number of hazardous vs non-hazardous asteroids": 
        
        cursor.execute("""SELECT IF (Is_potentially_hazardous_asteroid = 1, 'Hazardous','Non-Hazardous'), COUNT(*) AS total
                            FROM market.asteroids_data
                                GROUP BY Is_potentially_hazardous_asteroid;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance": 
        
        cursor.execute("""SELECT distinct a.Name, ap.Close_approach_date, ap.Miss_distance_lunar
                            FROM market.asteroids_data a
                                JOIN market.close_approaches ap
                                ON a.ID = ap.Neo_reference_id
                                WHERE ap.Miss_distance_lunar < 1;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "15.Find asteroids that came within 0.05 AU(astronomical distance)": 
        
        cursor.execute("""SELECT distinct a.Name
                            FROM market.asteroids_data a
                                JOIN market.close_approaches ap
                                ON a.ID = ap.Neo_reference_id
                                WHERE ap.Astronomical < 0.05;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)
    
    elif Query == "16.Find the Hazardous Asteroids approached earth in the monthh of Feb 2025": 
        
        cursor.execute("""SELECT a.Name, a.Is_potentially_hazardous_asteroid, ap.Close_approach_date
                            FROM market.asteroids_data a
                                JOIN market.close_approaches ap ON a.ID = ap.Neo_reference_id
                                Where a.Is_potentially_hazardous_asteroid = 1 
	                            AND ap.Close_approach_date >= '2025-02-01'
	                            AND ap.Close_approach_date < '2025-03-01'
                                ORDER BY 
                                ap.Close_approach_date;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "17.Find the Hazardous Asteroid approached earth in the month of Feb 2025 with high speed": 
        
        cursor.execute("""SELECT a.Name
                            FROM market.asteroids_data a
                                JOIN market.close_approaches ap ON a.ID = ap.Neo_reference_id
                                Where a.Is_potentially_hazardous_asteroid = 1 
	                            AND ap.Close_approach_date >= '2025-02-01'
	                            AND ap.Close_approach_date < '2025-03-01'
                                ORDER BY 
                                ap.Relative_velocity_kmph DESC
                                LIMIT 1;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "18.Find the Non-Hazardous Asteroid approached earth with low speed along with Relative velocity": 
        
        cursor.execute("""SELECT a.Name, ap.Relative_velocity_kmph
                            FROM market.asteroids_data a
                                JOIN market.close_approaches ap ON a.ID = ap.Neo_reference_id
                                Where a.Is_potentially_hazardous_asteroid = 0 
	                            ORDER BY 
                                ap.Relative_velocity_kmph ASC
                                LIMIT 1; """)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "19.Find the Hazardous Asteroid approached earth with lowest brightness": 
        
        cursor.execute("""SELECT a.Name, a.Absolute_magnitude_h
                            FROM market.asteroids_data a
                                Where a.Is_potentially_hazardous_asteroid = 1
                                ORDER BY 
                                a.Absolute_magnitude_h ASC
                                LIMIT 1;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)

    elif Query == "20.Find the average distance between Asteroids and earth": 
        
        cursor.execute("""SELECT Avg(Miss_distance_km) AS Average_Distance_Km
                            FROM market.close_approaches;""")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0]for i in cursor.description])
        st.dataframe(df)
