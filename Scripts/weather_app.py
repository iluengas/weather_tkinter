"""The purpose of this application is to show the weather info for city typed in"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from scripts.get_weather import get_weather
import pytz
from datetime import datetime

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Weather app details 
        self.title("Isaacs Weather Application")
        self.geometry("1039x750")
        self.configure(bg="#000000")

        self.style = ttk.Style()
        self.style.theme_use("default")

        self.notebook = ttk.Notebook(self, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.screen1 = tk.Frame(self.notebook, bg="black", padx=0, pady=0)
        self.screen2 = tk.Frame(self.notebook, bg="black")

        self.notebook.add(self.screen1, text="Weather")
        self.notebook.add(self.screen2, text="Weather Patterns")

        self.display_search_bar()
        self.modify_weather_patterns()

        # Load the space background image
        # self.weather_frame_space_image = Image.open("Images/space.png")
        # self.weather_frame_space_photo = ImageTk.PhotoImage(self.weather_frame_space_image)
        # Create frames for weather display
        self.weather_frame = tk.Frame(self.screen1, bg="black")
        self.weather_frame.pack(pady=(10, 0))

        self.col_frame = tk.Frame(self.weather_frame, bg="black")
        self.col_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create labels for city_name, temperature, and image
        self.city_label = tk.Label(self.col_frame, text="", bg="black", font=("Helvetica", 50))
        self.city_label.pack()

        self.temperature_label = tk.Label(self.col_frame, text="", bg="black", font=("Helvetica", 90))
        self.temperature_label.pack()

        # Create a canvas to display the image directly
        self.canvas = tk.Canvas(self.col_frame, bg="black", width=0, height=0, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

        # weather description
        self.weather_description_label = tk.Label(self.col_frame, text="", bg="black", font=("Helvetica", 30))
        self.weather_description_label.pack()

        # Create a row frame for additional weather information
        self.row_frame = tk.Frame(self.weather_frame, bg="black", pady=10)
        self.row_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.humidity_frame = tk.Frame(self.row_frame, bg="black")
        self.humidity_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.humidity_label = tk.Label(self.humidity_frame, text="", bg="black", font=("Helvetica", 25), anchor="n", fg="gray", width=15)
        self.humidity_label.pack(side=tk.TOP, fill=tk.X)
        self.humidity_percent_label = tk.Label(self.humidity_frame, text="", bg="black", font=("Helvetica", 60), anchor="n")
        self.humidity_percent_label.pack(side=tk.TOP, fill=tk.X)
        humidity_empty_frame = tk.Frame(self.humidity_frame, bg="black")# Create an empty frame to push the humidity labels to the top
        humidity_empty_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.wind_frame = tk.Frame(self.row_frame, bg="black")
        self.wind_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.wind_speed_label = tk.Label(self.wind_frame, text="", bg="black", font=("Helvetica", 25), anchor="n", fg="gray", width=15)
        self.wind_speed_label.pack(side=tk.TOP, fill=tk.X)
        self.wind_amount_label = tk.Label(self.wind_frame, text="", bg="black", font=("Helvetica", 60), anchor="n")
        self.wind_amount_label.pack(side=tk.TOP, fill=tk.X)
        wind_empty_frame = tk.Frame(self.wind_frame, bg="black")# Create an empty frame to push the humidity labels to the top
        wind_empty_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.pressure_frame = tk.Frame(self.row_frame, bg="black")
        self.pressure_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pressure_label = tk.Label(self.pressure_frame, text="", bg="black", font=("Helvetica", 25), width=25, anchor="n", fg="gray")
        self.pressure_label.pack(side=tk.TOP, fill=tk.X)
        self.pressure_amount_label = tk.Label(self.pressure_frame, text="", bg="black", font=("Helvetica", 60), anchor="n")
        self.pressure_amount_label.pack(side=tk.TOP, fill=tk.X)
        wind_empty_frame = tk.Frame(self.pressure_frame, bg="black")# Create an empty frame to push the humidity labels to the top
        wind_empty_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def display_search_bar(self):
        search_frame = tk.Frame(self.screen1, bg="black")
        search_frame.pack(side=tk.TOP, anchor='w', pady=(5, 0))

        # Add widgets inside the search_frame here
        label = tk.Label(search_frame, text="Enter your city: ", bg="black")
        label.pack(side=tk.LEFT)

        # where you enter city name
        entry = tk.Entry(search_frame, bg="#3A3B3C", width=40)
        entry.pack(side=tk.LEFT)

        # Create a custom button style with a red background
        style = ttk.Style()
        style.configure("Custom.TButton", background="cyan")

        # Create the search button with the custom style
        search_button = ttk.Button(search_frame, text="Search", style="Custom.TButton", command=lambda: self.search_weather(entry.get()))
        search_button.pack(side=tk.LEFT)


    def search_weather(self, city_name):
        # Remove leading and trailing whitespace from the city_name and lower it
        city_name = city_name.strip().lower()
        result = get_weather(city_name)
        if result:
            print(result)
            self.update_weather_screen(result, city_name)
        else:
            print("No weather found")


    def update_weather_screen(self, result, city_name):
        # Update the labels and image with the new weather data
        self.city_label.config(text=city_name)
        temperature_text = f"{result['temperature']}°"
        self.temperature_label.config(text=temperature_text)
        weather_image = self.choose_weather_image(result["weather"], result["timezone"])
        self.canvas.config(width=weather_image.width(), height=weather_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=weather_image)
        self.weather_description_label.config(text=f"{result['description']}")

        # Apply card-like appearance to additional weather information labels
        self.humidity_frame.config(bd=2, relief=tk.RAISED)
        humidity_text = "Humidity"
        self.humidity_label.config(text=humidity_text)
        self.humidity_percent_label.config(text=f"{result['humidity']}%")

        self.wind_frame.config(bd=2, relief=tk.RAISED)
        wind_speed_text = "Wind Speed"
        self.wind_speed_label.config(text=wind_speed_text)
        self.wind_amount_label.config(text=f"{result['wind_speed']}mph")

        self.pressure_frame.config(bd=2, relief=tk.RAISED)
        pressure_text = "Pressure"
        self.pressure_label.config(text=pressure_text)
        self.pressure_amount_label.config(text=f"{result['pressure']}Pa")


    def choose_weather_image(self, weather, timezone):
        x, y = 360, 300
        # Get the current time for the city
        city_timezone = pytz.FixedOffset(timezone // 60)  # Convert the timezone offset to a FixedOffset
        city_time = datetime.now(city_timezone)

        if "clear" in weather.lower():
            if self.is_daytime(city_timezone):
                x, y = 300, 300
                weather_image = Image.open("images/sun.png").resize((x, y))
            else:
                x, y = 350, 300
                weather_image = Image.open("images/moon.png").resize((x, y))
                
        elif "cloud" in weather.lower():
            weather_image = Image.open("images/cloud.png").resize((x, y))
        elif "rain" in weather.lower():
            weather_image = Image.open("images/rain.png").resize((x, y))
        elif "thunder" in weather.lower() or "lightning" in weather.lower() or "storm" in weather.lower():
            weather_image = Image.open("images/thunder.png").resize((x, y))
        else:
            # Set a default image if the weather is not recognized
            weather_image = Image.open("images/default.png").resize((x, y))

        # Convert the PIL Image to PhotoImage and save it as an instance variable
        self.weather_image = ImageTk.PhotoImage(weather_image)
        return self.weather_image

    def is_daytime(self, city_timezone):
        # Get the current time for the city
        city_time = datetime.now(city_timezone)
        
        # Extract the hour from the city's local time
        city_hour = city_time.hour
        
        # Define the range of hours considered as daytime (e.g., 6 AM to 6 PM)
        daytime_start_hour = 6
        daytime_end_hour = 18
        
        # Check if the city's local time falls within the daytime range
        return daytime_start_hour <= city_hour < daytime_end_hour

    def modify_weather_patterns(self):
        pass
