import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from datetime import datetime

class OCRAnnotationEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Annotation Editor")
        self.root.state('zoomed')  # Start maximized on Windows
        
        # State variables
        self.current_image_path = None
        self.current_json_path = None
        self.annotations = []
        self.modified = False
        self.selected_box = None
        self.resizing = False
        self.moving = False
        self.last_x = 0
        self.last_y = 0
        self.resize_handle = None
        self.current_image_index = 0
        self.image_list = []
        self.drawing_new_box = False
        self.start_x = 0
        self.start_y = 0
        
        # Create main frames
        self.left_frame = tk.Frame(root, width=200, bg="#f0f0f0")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Image canvas
        self.canvas_frame = tk.Frame(self.right_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        # Status bar
        self.status_bar = tk.Label(self.right_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Controls in left frame
        tk.Label(self.left_frame, text="OCR Annotation Editor", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Buttons
        tk.Button(self.left_frame, text="Open Project", command=self.open_project, width=20).pack(pady=5)
        tk.Button(self.left_frame, text="Open JSON", command=self.open_json, width=20).pack(pady=5)
        tk.Button(self.left_frame, text="Open Image", command=self.open_image, width=20).pack(pady=5)
        tk.Button(self.left_frame, text="Save", command=self.save_annotations, width=20).pack(pady=5)
        tk.Button(self.left_frame, text="Save As...", command=self.save_annotations_as, width=20).pack(pady=5)
        
        # Navigation
        nav_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        nav_frame.pack(pady=10)
        tk.Button(nav_frame, text="◀ Prev", command=self.prev_image).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Next ▶", command=self.next_image).pack(side=tk.LEFT, padx=5)
        
        # File info
        self.file_info_frame = tk.LabelFrame(self.left_frame, text="File Info", bg="#f0f0f0", padx=5, pady=5)
        self.file_info_frame.pack(fill=tk.X, pady=10, padx=5)
        
        self.image_name_label = tk.Label(self.file_info_frame, text="Image: None", bg="#f0f0f0", anchor="w", justify=tk.LEFT)
        self.image_name_label.pack(fill=tk.X)
        
        self.json_name_label = tk.Label(self.file_info_frame, text="JSON: None", bg="#f0f0f0", anchor="w", justify=tk.LEFT)
        self.json_name_label.pack(fill=tk.X)
        
        self.count_label = tk.Label(self.file_info_frame, text="Annotations: 0", bg="#f0f0f0", anchor="w")
        self.count_label.pack(fill=tk.X)
        
        # Annotation list frame
        self.ann_list_frame = tk.LabelFrame(self.left_frame, text="Annotations", bg="#f0f0f0")
        self.ann_list_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)
        
        self.ann_listbox = tk.Listbox(self.ann_list_frame, height=15, selectmode=tk.SINGLE)
        self.ann_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.ann_listbox.bind('<<ListboxSelect>>', self.on_annotation_select)
        
        # Help text
        help_frame = tk.LabelFrame(self.left_frame, text="Controls", bg="#f0f0f0")
        help_frame.pack(fill=tk.X, pady=10, padx=5)
        
        help_text = "Click: Select box\nDel: Delete box\nDrag: Move box\nShift+Drag: Resize box\nCtrl+Drag: Create new box"
        tk.Label(help_frame, text=help_text, justify=tk.LEFT, bg="#f0f0f0").pack(padx=5, pady=5)
        
        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<Delete>", self.delete_selected)
        self.root.bind("<Control-s>", lambda e: self.save_annotations())
        
        # Modified indicator
        self.modified_indicator = self.canvas.create_text(20, 20, text="", fill="red", font=("Arial", 16, "bold"), anchor="nw")
        
        # Welcome message
        self.show_welcome()
    
    def show_welcome(self):
        welcome_text = """
        Welcome to OCR Annotation Editor
        
        This tool allows you to edit OCR annotations with ease.
        
        To get started:
        1. Open a JSON file with OCR annotations
        2. Edit bounding boxes and text
        3. Save your changes
        
        Use the controls listed on the left panel.
        """
        self.canvas.create_text(400, 300, text=welcome_text, fill="white", font=("Arial", 14))
    
    def open_project(self):
        folder_path = filedialog.askdirectory(title="Select Project Directory")
        if not folder_path:
            return
            
        # Look for image files and json files
        self.image_list = []
        json_files = []
        
        for file in os.listdir(folder_path):
            lower_file = file.lower()
            if lower_file.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                self.image_list.append(os.path.join(folder_path, file))
            elif lower_file.endswith('.json'):
                json_files.append(os.path.join(folder_path, file))
        
        if not self.image_list:
            messagebox.showwarning("Warning", "No image files found in the selected directory")
            return
            
        # Try to match json files with images
        self.current_image_index = 0
        self.load_image(self.image_list[0])
        
        # Try to find matching JSON
        base_name = os.path.splitext(os.path.basename(self.image_list[0]))[0]
        matching_json = None
        
        for json_file in json_files:
            json_base = os.path.splitext(os.path.basename(json_file))[0]
            if json_base == base_name or json_base.startswith(base_name):
                matching_json = json_file
                break
                
        if matching_json:
            self.load_json(matching_json)
            
        self.status_bar.config(text=f"Loaded project with {len(self.image_list)} images and {len(json_files)} JSON files")
    
    def next_image(self):
        if not self.image_list or len(self.image_list) <= 1:
            return
            
        # Check if current has unsaved changes
        if self.modified:
            if messagebox.askyesno("Unsaved Changes", "Save changes before moving to next image?"):
                self.save_annotations()
        
        self.current_image_index = (self.current_image_index + 1) % len(self.image_list)
        self.load_image(self.image_list[self.current_image_index])
        
        # Try to find matching JSON
        base_name = os.path.splitext(os.path.basename(self.image_list[self.current_image_index]))[0]
        json_path = os.path.join(os.path.dirname(self.image_list[self.current_image_index]), f"{base_name}.json")
        
        if os.path.exists(json_path):
            self.load_json(json_path)
        else:
            # Clear annotations if no JSON found
            self.annotations = []
            self.update_annotation_list()
            self.redraw_annotations()
            
        self.status_bar.config(text=f"Image {self.current_image_index + 1} of {len(self.image_list)}")
    
    def prev_image(self):
        if not self.image_list or len(self.image_list) <= 1:
            return
            
        # Check if current has unsaved changes
        if self.modified:
            if messagebox.askyesno("Unsaved Changes", "Save changes before moving to previous image?"):
                self.save_annotations()
        
        self.current_image_index = (self.current_image_index - 1) % len(self.image_list)
        self.load_image(self.image_list[self.current_image_index])
        
        # Try to find matching JSON
        base_name = os.path.splitext(os.path.basename(self.image_list[self.current_image_index]))[0]
        json_path = os.path.join(os.path.dirname(self.image_list[self.current_image_index]), f"{base_name}.json")
        
        if os.path.exists(json_path):
            self.load_json(json_path)
        else:
            # Clear annotations if no JSON found
            self.annotations = []
            self.update_annotation_list()
            self.redraw_annotations()
            
        self.status_bar.config(text=f"Image {self.current_image_index + 1} of {len(self.image_list)}")
    
    def open_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            self.load_json(file_path)
    
    def load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Try to extract annotations - adapt this to your JSON structure
            self.annotations = []
            
            # Attempt to detect the format and extract annotations
            if isinstance(data, list):
                # Assume it's a list of annotations
                for item in data:
                    if 'bbox' in item and 'text' in item:
                        self.annotations.append(item)
            elif isinstance(data, dict):
                # Look for common patterns in JSON structures
                if 'annotations' in data:
                    for item in data['annotations']:
                        if 'bbox' in item and 'text' in item:
                            self.annotations.append(item)
                elif 'results' in data:
                    for item in data['results']:
                        if 'bbox' in item and 'text' in item:
                            self.annotations.append(item)
                elif 'words' in data:
                    for item in data['words']:
                        if 'bbox' in item and 'text' in item:
                            self.annotations.append(item)
                            
            if not self.annotations:
                # If we couldn't find annotations, ask user to specify the path
                path_query = simpledialog.askstring(
                    "JSON Path",
                    "Couldn't automatically find annotations.\nPlease enter the JSON path to annotations (e.g., 'results.annotations'):"
                )
                
                if path_query:
                    parts = path_query.split('.')
                    current = data
                    for part in parts:
                        if part in current:
                            current = current[part]
                        else:
                            messagebox.showerror("Error", f"Path '{part}' not found in JSON")
                            return
                    
                    # Now current should point to the annotations
                    if isinstance(current, list):
                        for item in current:
                            if 'bbox' in item and 'text' in item:
                                self.annotations.append(item)
            
            self.current_json_path = file_path
            self.json_name_label.config(text=f"JSON: {os.path.basename(file_path)}")
            self.count_label.config(text=f"Annotations: {len(self.annotations)}")
            self.modified = False
            self.update_annotation_list()
            self.redraw_annotations()
            self.update_modified_indicator()
            
            # Try to find and load corresponding image if not already loaded
            if not self.current_image_path:
                json_dir = os.path.dirname(file_path)
                json_basename = os.path.splitext(os.path.basename(file_path))[0]
                
                # Look for common image extensions
                for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                    img_path = os.path.join(json_dir, f"{json_basename}{ext}")
                    if os.path.exists(img_path):
                        self.load_image(img_path)
                        break
            
            self.status_bar.config(text=f"Loaded {len(self.annotations)} annotations from {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON: {str(e)}")
    
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp"), 
            ("All files", "*.*")
        ])
        if file_path:
            self.load_image(file_path)
            
            # Check for a matching JSON file
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            json_path = os.path.join(os.path.dirname(file_path), f"{base_name}.json")
            
            if os.path.exists(json_path):
                self.load_json(json_path)
    
    def load_image(self, file_path):
        try:
            # Open and resize image for display
            self.cv_image = cv2.imread(file_path)
            self.cv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
            
            # Create PIL Image
            self.pil_image = Image.fromarray(self.cv_image)
            self.tk_image = ImageTk.PhotoImage(self.pil_image)
            
            # Update canvas
            self.canvas.delete("all")
            self.canvas.config(scrollregion=(0, 0, self.pil_image.width, self.pil_image.height))
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW, tags="image")
            
            # Update UI
            self.current_image_path = file_path
            self.image_name_label.config(text=f"Image: {os.path.basename(file_path)}")
            
            # Redraw annotations if any
            self.redraw_annotations()
            
            # Show modified indicator
            self.modified_indicator = self.canvas.create_text(20, 20, text="", fill="red", font=("Arial", 16, "bold"), anchor="nw")
            
            self.status_bar.config(text=f"Loaded image: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def update_annotation_list(self):
        self.ann_listbox.delete(0, tk.END)
        for i, ann in enumerate(self.annotations):
            text = ann.get('text', 'No text')
            truncated = text[:20] + "..." if len(text) > 20 else text
            self.ann_listbox.insert(tk.END, f"{i+1}: {truncated}")
    
    def on_annotation_select(self, event):
        if not self.ann_listbox.curselection():
            return
            
        idx = self.ann_listbox.curselection()[0]
        if 0 <= idx < len(self.annotations):
            self.selected_box = idx
            self.redraw_annotations()
            
            # Ensure selected box is visible
            bbox = self.annotations[idx].get('bbox', [0, 0, 100, 100])
            x1, y1, x2, y2 = bbox if len(bbox) == 4 else [bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3]]
            
            # Calculate center of the box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            # Scroll to center the box
            self.canvas.xview_moveto((center_x - self.canvas.winfo_width()/2) / self.pil_image.width)
            self.canvas.yview_moveto((center_y - self.canvas.winfo_height()/2) / self.pil_image.height)
    
    def redraw_annotations(self):
        if not hasattr(self, 'pil_image'):
            return
            
        # Clear existing annotations on canvas
        self.canvas.delete("box")
        self.canvas.delete("text")
        self.canvas.delete("handle")
        
        # Redraw all annotations
        for i, ann in enumerate(self.annotations):
            bbox = ann.get('bbox', [0, 0, 100, 100])
            text = ann.get('text', '')
            
            # Handle different bbox formats
            if len(bbox) == 4:
                x1, y1, x2, y2 = bbox
            else:
                # Assume format is x, y, width, height
                x1, y1, w, h = bbox
                x2, y2 = x1 + w, y1 + h
            
            # Draw the box
            color = "green" if i == self.selected_box else "blue"
            width = 2 if i == self.selected_box else 1
            
            self.canvas.create_rectangle(
                x1, y1, x2, y2, 
                outline=color, 
                width=width,
                tags=("box", f"box{i}")
            )
            
            # Draw the text inside or above the box
            text_y = y1 - 5 if y1 > 20 else y2 + 5
            self.canvas.create_text(
                x1, text_y,
                text=text[:20] + "..." if len(text) > 20 else text,
                fill="black",
                tags=("text", f"text{i}"),
                anchor="nw"
            )
            
            # Draw resize handle if selected
            if i == self.selected_box:
                self.canvas.create_rectangle(
                    x2-5, y2-5, x2+5, y2+5,
                    fill="red",
                    tags=("handle", f"handle{i}")
                )
    
    def on_press(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.last_x, self.last_y = x, y
        
        # Check if we're clicking on a resize handle
        handle_item = self.canvas.find_withtag("handle")
        items = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        
        # Check for resize handle first
        if handle_item and any(item in handle_item for item in items):
            self.resizing = True
            return
            
        # Check if we're clicking on a box
        box_items = self.canvas.find_withtag("box")
        for item in items:
            if item in box_items:
                # Find which box we clicked on
                for i in range(len(self.annotations)):
                    if item in self.canvas.find_withtag(f"box{i}"):
                        self.selected_box = i
                        self.moving = True
                        self.ann_listbox.selection_clear(0, tk.END)
                        self.ann_listbox.selection_set(i)
                        self.ann_listbox.see(i)
                        self.redraw_annotations()
                        return
        
        # If Ctrl is pressed, start drawing a new box
        if event.state & 0x4:  # Ctrl key
            self.drawing_new_box = True
            self.start_x, self.start_y = x, y
            return
            
        # If we didn't click on anything, deselect
        self.selected_box = None
        self.ann_listbox.selection_clear(0, tk.END)
        self.redraw_annotations()
    
    def on_drag(self, event):
        if not hasattr(self, 'pil_image'):
            return
            
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        dx, dy = x - self.last_x, y - self.last_y
        self.last_x, self.last_y = x, y
        
        if self.resizing and self.selected_box is not None:
            # Resize the selected box
            bbox = self.annotations[self.selected_box].get('bbox', [0, 0, 100, 100])
            
            if len(bbox) == 4:
                x1, y1, x2, y2 = bbox
                
                # Update the bottom-right corner
                x2 += dx
                y2 += dy
                
                # Ensure minimum size
                if x2 - x1 < 10:
                    x2 = x1 + 10
                if y2 - y1 < 10:
                    y2 = y1 + 10
                    
                self.annotations[self.selected_box]['bbox'] = [x1, y1, x2, y2]
            else:
                # Assume format is x, y, width, height
                x, y, w, h = bbox
                
                # Update width and height
                w += dx
                h += dy
                
                # Ensure minimum size
                if w < 10:
                    w = 10
                if h < 10:
                    h = 10
                    
                self.annotations[self.selected_box]['bbox'] = [x, y, w, h]
                
            self.modified = True
            self.update_modified_indicator()
            self.redraw_annotations()
            
        elif self.moving and self.selected_box is not None:
            # Move the selected box
            bbox = self.annotations[self.selected_box].get('bbox', [0, 0, 100, 100])
            
            if len(bbox) == 4:
                x1, y1, x2, y2 = bbox
                
                # Update all corners
                x1 += dx
                y1 += dy
                x2 += dx
                y2 += dy
                    
                self.annotations[self.selected_box]['bbox'] = [x1, y1, x2, y2]
            else:
                # Assume format is x, y, width, height
                x, y, w, h = bbox
                
                # Update position
                x += dx
                y += dy
                    
                self.annotations[self.selected_box]['bbox'] = [x, y, w, h]
                
            self.modified = True
            self.update_modified_indicator()
            self.redraw_annotations()
            
        elif self.drawing_new_box:
            # Clear previous temporary rectangle
            self.canvas.delete("temp_box")
            
            # Draw temporary rectangle
            self.canvas.create_rectangle(
                self.start_x, self.start_y, x, y,
                outline="red",
                dash=(4, 4),
                tags="temp_box"
            )
    
    def on_release(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        if self.drawing_new_box:
            # Clear temporary rectangle
            self.canvas.delete("temp_box")
            
            # Calculate box coordinates
            x1, y1 = min(self.start_x, x), min(self.start_y, y)
            x2, y2 = max(self.start_x, x), max(self.start_y, y)
            
            # Minimum size check
            if x2 - x1 > 10 and y2 - y1 > 10:
                # Ask for text
                text = simpledialog.askstring("Annotation Text", "Enter text for this annotation:")
                
                if text:
                    # Create new annotation
                    new_ann = {
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'text': text
                    }
                    
                    self.annotations.append(new_ann)
                    self.selected_box = len(self.annotations) - 1
                    self.modified = True
                    self.update_modified_indicator()
                    self.update_annotation_list()
                    self.ann_listbox.selection_clear(0, tk.END)
                    self.ann_listbox.selection_set(self.selected_box)
                    self.ann_listbox.see(self.selected_box)
                    self.redraw_annotations()
        
        self.resizing = False
        self.moving = False
        self.drawing_new_box = False
    
    def delete_selected(self, event=None):
        if self.selected_box is not None:
            if messagebox.askyesno("Confirm Delete", "Delete selected annotation?"):
                del self.annotations[self.selected_box]
                self.selected_box = None
                self.modified = True
                self.update_modified_indicator()
                self.update_annotation_list()
                self.redraw_annotations()
                self.count_label.config(text=f"Annotations: {len(self.annotations)}")
    
    def update_modified_indicator(self):
        if self.modified:
            self.canvas.itemconfig(self.modified_indicator, text="Modified")
        else:
            self.canvas.itemconfig(self.modified_indicator, text="")
    
    def save_annotations(self):
        if not self.current_json_path:
            return self.save_annotations_as()
            
        try:
            # First read the original JSON to preserve structure
            with open(self.current_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Update the annotations in the original structure
            # This depends on the structure of your JSON
            if isinstance(data, list):
                # If the JSON is just a list of annotations
                data = self.annotations
            elif isinstance(data, dict):
                # Find where to put the annotations
                if 'annotations' in data:
                    data['annotations'] = self.annotations
                elif 'results' in data:
                    data['results'] = self.annotations
                elif 'words' in data:
                    data['words'] = self.annotations
                    
            # Save back to file
            with open(self.current_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            self.modified = False
            self.update_modified_indicator()
            self.status_bar.config(text=f"Saved annotations to {os.path.basename(self.current_json_path)}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
            return False
    
    def save_annotations_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=os.path.dirname(self.current_json_path) if self.current_json_path else None
        )
        
        if not file_path:
            return False
            
        self.current_json_path = file_path
        return self.save_annotations()

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRAnnotationEditor(root)
    root.mainloop()