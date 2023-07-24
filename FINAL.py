def get_username():
	# Make the popup window
	enter_username_window = Toplevel(main_window)
	enter_username_window.title("Enter your username")
	enter_username_window.configure(width= 500,height= 250, bg="#0E1428", padx=100, pady=100)
	
	# Labels
	username_label = Label(enter_username_window, text="Enter a username: ", font=("Roboto Mono", 15, "bold"), fg="#FF7F11", bg="#0E1428")
	username_label.grid(column=0, row=0, padx=50, pady=10)
	
	# Entry
	username_entry = Entry(enter_username_window, bg="#FFFFFC", borderwidth=0, highlightcolor="#FF7F11")
	username_entry.focus_set()
	username_entry.grid(column=0, row=1, pady= 10)
	
	# Button
	username_button = Button(enter_username_window, bg="#FFFFFC", text="Submit", font=("Roboto Mono", 15, "bold"), fg="#0E1428", command=lambda: add_user(username_entry.get(), enter_username_window))
	username_button.grid(column=0, row=2, pady=10)
	
	
def display_login():
	# Make login window
	login_window = Toplevel(main_window)
	login_window.title("Login")
	login_window.configure(width= 500,height= 250, bg="#0E1428", padx=100, pady=100)
	
	# Labels
	title_label = Label(login_window, text="Login", font=("Roboto Mono", 15, "bold"), fg="#FF7F11", bg="#0E1428")
	title_label.grid(column=0, row=0, columnspan = 2)
	
	username_label = Label(login_window, text="Username: ", font=("Roboto Mono", 15, "bold"), fg="#FF7F11", bg="#0E1428")
	username_label.grid(column=0, row=1, padx=50, pady=10)
	
	password_label = Label(login_window, text="Password: ", font=("Roboto Mono", 15, "bold"), fg="#FF7F11", bg="#0E1428")
	password_label.grid(column=0, row=2, padx=50, pady=10)

	# Entry
	username_entry = Entry(login_window, bg="#FFFFFC", borderwidth=0, highlightcolor="#FF7F11")
	username_entry.focus_set()
	username_entry.grid(column=1, row=1)
	password_entry = Entry(login_window, bg="#FFFFFC", borderwidth=0, highlightcolor="#FF7F11", show="*")
	password_entry.grid(column=1, row=2)
	
	username_button = Button(login_window, bg="#FFFFFC", text="log in", font=("Roboto Mono", 15, "bold"), fg="#0E1428", command=lambda: check_password(username_entry.get(), password_entry.get(), login_window))
	username_button.grid(column=0, row=3, pady=10, columnspan=2)
	
	
def check_password(username, password, login_window):
	if username == "pesu" and password == "pesu123":
		login_window.destroy()
		get_username()
	else:
		alert_message = messagebox.showinfo(message="Wrong Username and Password!")
		
		now = dt.datetime.now()
		date = now.strftime("%d/%m/%Y")
		bot = telebot.TeleBot(bot_token)
		bot.send_message(chat_id, f"There was a failed attempt to login in your system for registering a face on {date}")
		
def add_user(username, window):
	# Check if username is valid
	if username == None or username == "":
		warning = messagebox.showinfo(message="Please enter a valid username!")
		
	# load the pics to check username availability
	folder_path = "/home/pesu/test-files/images/"
	known_face_names = []
	
	for filename in os.listdir(folder_path):
		img = face_recognition.load_image_file(f"/home/pesu/test-files/images/{filename}")
		img_name = filename.replace("_0.jpg", "")
		known_face_names.append(img_name)
		
	if username in known_face_names:
		alert_message = messagebox.showinfo(message="That username is already taken!! Choose another username")
	else:
		window.destroy()
		register_user(username)

def register_user(user: str):
	img_saved = False
	cam = cv.VideoCapture(0)
	image_counter = 0
	info = messagebox.showinfo(message="Press SpaceBar to take the pic and Esc to quit")
	
	# while loop
	while image_counter < 1:
		ret, frame = cam.read()
		
		# Resize frame of video to 1/4 size for faster face detection processing
		small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)

		# converting from BGR to RGB
		rgb_small_frame = small_frame[:, :, ::-1]

		# Find all the faces in the current frame of video
		face_locations = face_recognition.face_locations(rgb_small_frame)

		# Display the results
		for (top, right, bottom, left) in face_locations:
			# Scale back up face locations since the frame we detected in was scaled to 1/4 size
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4

			# Draw a box around the face
			cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
		
		# check health of frames
		if not ret:
			print("Error fetching the frames! exiting....\n\n")
			break
			
		# title of window
		cv.imshow("Register User: Space to save and Esc to close", frame)
		
		k = cv.waitKey(1)
		
		if k%256 == 27:
			print("Esc hit, exiting....\n\n")
			break
			
		elif k%256 == 32:
			if len(face_locations) > 0:
				img_name = f"{user}_{image_counter}.jpg"
				path_name = "/home/pesu/test-files/images"
				cv.imwrite(os.path.join(path_name, img_name), frame)
				print(f"\n\nSaved user: {user} in the name: {img_name}")
				print("Save successful!\n")
				img_saved = True
				image_counter += 1
			else:
				break
			
	cam.release()
	cv.destroyAllWindows()
	if img_saved == True:
		success_message = messagebox.showinfo(message=f"Saved user: {user} in the name: {img_name}")
	else:
		no_face_message = messagebox.showinfo(message="There are no faces detected!")
	
	
def recognise_face():
	
	cam = cv.VideoCapture(0)
	
	# We load all the images
	folder_path = "/home/pesu/test-files/images/"
	known_face_encoding = []
	known_face_names = []
	
	for filename in os.listdir(folder_path):
		img = face_recognition.load_image_file(f"/home/pesu/test-files/images/{filename}")
		img_face_encoding = face_recognition.face_encodings(img)[0]
		known_face_encoding.append(img_face_encoding)
		img_name = filename.replace("_0.jpg", "")
		known_face_names.append(img_name)
		
	if len(known_face_names) < 1:
		error_message = messagebox.showinfo(message=f"There are no faces registered!")
		return
		
				
	# Variables for the user
	face_locations = []
	face_encodings = []
	face_names = []
	
	process_this_frame = True
	
	find_face = True
	
	start_time = time.time()
	
	while find_face:
		# Get a single frame from vid
		ret, frame = cam.read()
		
		if process_this_frame:
			# Resize the image to a smaller img to perform face recog
			small_frame = cv.resize(frame, (0,0), fx=0.25, fy=0.25)
			
			# Convert BRG to RGB
			rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])
			
			# Find faces and encodings from video
			face_locations = face_recognition.face_locations(rgb_small_frame)
			
			if len(face_locations) > 0:
				face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
				
				
				match_found = False
				
				face_names = []
				for face_encoding in face_encodings:
					# Check for match
					matches = face_recognition.compare_faces(known_face_encoding, face_encoding, tolerance=0.4)
					name = "Unknown"
					
					face_distances = face_recognition.face_distance(known_face_encoding, face_encoding)
					print(face_distances)
					best_match_index = numpy.argmin(face_distances)
					if matches[best_match_index]:
						name = known_face_names[best_match_index]
					face_names.append(name)
					
					if True in matches:
						print(f"\n\nFace recognized: {name}\n\n")
						open_door()
						match_found = True
						find_face = False
						success = messagebox.showinfo(message=f"Face Recognised. Welcome {name}")
						break
						
					else:
						print("\n\nUnknown User! Alert!!\n\n")
						send_alert_message(frame)
						find_face = False
						break
					  
		process_this_frame = not process_this_frame
		
		# Displaying rectangle and puting the name
		for (top, right, bottom, left), name in zip(face_locations, face_names):
			# Scale the frame back
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4
			
			# Drawing the rectangle
			cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
			
			# Lable
			cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
			font = cv.FONT_HERSHEY_DUPLEX
			cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
		
		cv.imshow("Recognising", frame)
		
		k = cv.waitKey(1)
		
		# Checking for time out 
		elapsed_time = time.time() - start_time
		if elapsed_time > 20:
			error_message = messagebox.showinfo(message=f"Could not detect any faces!")
			print("\n\nCould not detect any faces!\n\n")
			break
		
		
		if k%256 == 27:
			print("Esc hit, exiting....\n\n")
			break
	
	cam.release()
	cv.destroyAllWindows()
	
	
def open_door():
	gpio_pin = 18
	# ~ GPIO.setwarnings(False)
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(gpio_pin, GPIO.OUT)
	
	GPIO.output(gpio_pin, 0)
	time.sleep(3)
	GPIO.output(gpio_pin, 1)
	time.sleep(3)
	

def send_alert_message(frame):
	now = dt.datetime.now()
	date = now.strftime("%d/%m/%Y")
	bot = telebot.TeleBot(bot_token)
	cv.imwrite("/home/pesu/test-files/unknown_faces/Unknown_face.jpg", frame)
	photo = open("/home/pesu/test-files/unknown_faces/Unknown_face.jpg", "rb")
	bot.send_photo(chat_id, photo)
	bot.send_message(chat_id, f"Unknown person detected at the door! - date: {date}")
	time.sleep(3)
	try:
		os.remove("/home/pesu/test-files/unknown_faces/Unknown_face.jpg")
	except:
		pass
	unknown_face_message = messagebox.showinfo(message=f"Unknown face! Security procedure initiated and successful.")



# Main program
from tkinter import *
from tkinter import messagebox
import cv2 as cv 
import os
import face_recognition
import numpy 
import RPi.GPIO as GPIO 
import time
import telebot
import datetime as dt

gpio_pin = 18
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.OUT)

GPIO.output(gpio_pin, 1)

bot_token = BOT_TOKEN
chat_id = CHAT_ID

# Making the main tkinter window
main_window = Tk()
main_window.title("Face Recognising Door")
main_window.config(width=600, height=600, bg="#FFFFFC", padx=20, pady=100)
main_window.resizable(0, 0)
main_window.eval("tk::PlaceWindow . center")


# Making the labels for main window
heading_label = Label(main_window, text="Face Recognising Door", font=("Roboto Mono", 20, "bold"), bg="#FFFFFC", fg="#FF7F11")
heading_label.config(padx=150, pady=10)
heading_label.grid(row=0, column=0)

# Canvas for pesu-log
pesu_logo = PhotoImage(file="PESU-logo.jpg")
pesu_logo_canvas = Canvas(main_window, width=200, height=120, bg="#FFFFFC", highlightthickness=0)
pesu_image = pesu_logo_canvas.create_image(90, 66, image=pesu_logo)
pesu_logo_canvas.grid(column=0, row= 1)

# Making the buttons
register_button = Button(text="Register Face", font=("Roboto Mono", 15, "bold"), bg="#0E1428", fg="#FF7F11", padx=15, pady=10, activebackground="#FF7F11", activeforeground="#0E1428", command=display_login)
register_button.grid(column=0, row=2, pady=10)

recognise_button = Button(text="Recognise Face", font=("Roboto Mono", 15, "bold"), bg="#0E1428", fg="#FF7F11", padx=15, pady=10, activebackground="#FF7F11", activeforeground="#0E1428", command=recognise_face)
recognise_button.grid(column=0, row=3, pady=10)




main_window.mainloop()
