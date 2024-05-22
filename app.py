import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk, ImageSequence
from API import scrapper, gemini_api

def getlocation(location_type, query_size):
    Thread(target=scrape_and_display, args=(location_type, query_size)).start()

def scrape_and_display(location_type, query_size):
    show_loading_gif()
    scrapper.scrape(location_type, query_size)
    result = scrapper.clean()
    hide_loading_gif()
    display_results(result)

def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")

def on_focusout(event, entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)

def display_results(results):
    for item in results:
        tree.insert('', 'end', values=(
            item['lead_name'], item['lead_contacts'], item['website'], item['price_range'], item['location']
        ))

def on_select(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        item_values = item['values']
        show_lead_details({
            'lead_name': item_values[0],
            'lead_contacts': item_values[1],
            'website': item_values[2],
            'price_range': item_values[3],
            'location': item_values[4],
        })

def show_lead_details(lead):
    detail_window = tk.Toplevel(root)
    detail_window.title(lead['lead_name'])
    detail_window.geometry("1200x500")

    revs = scrapper.get_reviews(lead['lead_name'])

    max_val, max_rt, min_val, min_rt = revs
    detail_window.grid_rowconfigure(0, weight=1)
    detail_window.grid_columnconfigure(0, weight=1)
    frame = tk.Frame(detail_window, padx=10, pady=10)
    frame.grid(row=0, column=0, sticky="nsew")

    tk.Label(frame, text=f"Name: {lead['lead_name']}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(frame, text=f"Contacts: {lead['lead_contacts']}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(frame, text=f"Website: {lead['website']}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(frame, text=f"Price Range: {lead['price_range']}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(frame, text=f"Reviews:", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(frame, text=f"\tMax Rating: {max_val} : {max_rt}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(frame, text=f"\tMin Rating: {min_val} : {min_rt}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Button(frame, text="Get AI Review", command= lambda: priv_rev(lead['lead_name']+", Location: "+lead['location'])).pack(anchor="w", pady=5)
    tk.Button(frame, text="Get Directions", command= lambda: scrapper.open_link(lead['lead_name'])).pack(anchor="w", pady=5)


    close_button = tk.Button(detail_window, text="Close", command=detail_window.destroy)
    close_button.grid(row=1, column=0, pady=10)

def priv_rev(name):
  Thread(target=get_ai_review, args=(name,)).start()

def get_ai_review(lead_name):
  global root

  ai_window = tk.Toplevel(root)
  ai_window.title(lead_name)
  ai_window.geometry("1200x500")

  frame = tk.Frame(ai_window, padx=10, pady=10)
  frame.grid(row=0, column=0, sticky="nsew")

  resp = gemini_api.get_resp(lead_name)

  tk.Label(frame, text=f"Name: {lead_name}", font=("Arial", 14)).pack(anchor="w", pady=5)
  tk.Label(frame, text=f"AI Review: {resp}", font=("Arial", 14), wraplength=1100).pack(pady=5, side=tk.LEFT)

  close_button = tk.Button(ai_window, text="Close", command=ai_window.destroy)
  close_button.grid(row=1, column=0, pady=10)

def show_loading_gif():
    global loading_label, loading_frames, animation_running
    loading_label = tk.Label(root)
    loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    loading_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(Image.open("loading.gif"))]
    animation_running = True
    animate_gif()

def animate_gif():
    global loading_label, loading_frames, animation_running
    if animation_running:
        frame = loading_frames.pop(0)
        loading_frames.append(frame)
        loading_label.configure(image=frame)
        root.after(100, animate_gif) 

def hide_loading_gif():
    global animation_running
    animation_running = False
    loading_label.place_forget()
    loading_label.destroy()


root = tk.Tk()
root.title("Lead Gen App")
root.geometry("1200x500")

background_label = tk.Label(root, bg="white")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

search_frame = tk.Frame(root, bg="cyan", padx=10, pady=10)
search_frame.pack(fill=tk.X)

location_type_entry = tk.Entry(search_frame, width=50, font=("Arial", 14))
location_type_entry.insert(0, "Location Type")
location_type_entry.bind('<FocusIn>', lambda event: on_entry_click(event, location_type_entry, "Location Type"))
location_type_entry.bind('<FocusOut>', lambda event: on_focusout(event, location_type_entry, "Location Type"))
location_type_entry.pack(side=tk.LEFT, padx=10)

query_size_entry = tk.Entry(search_frame, width=30, font=("Arial", 14))
query_size_entry.insert(0, "Query Size")
query_size_entry.bind('<FocusIn>', lambda event: on_entry_click(event, query_size_entry, "Query Size"))
query_size_entry.bind('<FocusOut>', lambda event: on_focusout(event, query_size_entry, "Query Size"))
query_size_entry.pack(side=tk.LEFT)

button = tk.Button(search_frame, text="Get Leads", command=lambda: getlocation(location_type_entry.get(), query_size_entry.get()))
button.pack(side=tk.LEFT, padx=10)

list_frame = tk.Frame(root)
list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = ('Name', 'Contacts', 'Website', 'Price Range', 'Location')
tree = ttk.Treeview(list_frame, columns=columns, show='headings')
tree.pack(fill=tk.BOTH, expand=True)

for col in columns:
    tree.heading(col, text=col)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.bind('<<TreeviewSelect>>', on_select)

root.mainloop()
