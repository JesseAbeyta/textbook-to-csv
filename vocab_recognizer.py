# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 14:00:20 2019

@author: Warlock
"""

from PIL import Image, ImageTk
import tkinter as tk
import csv
import pytesseract

def ocr_core(filename=None, image=None, echo=True):
    if image is None:
        image = Image.open(filename)
    if echo:
        print("Beginning Optical Character Recognition...")
    text = pytesseract.image_to_string(image, lang="eng+isl", config="--psm 4")
    if echo:
        print("Done")
    return text

def text_to_csv(text, echo=True):
    if echo:
        print("Writing to file...")
    lines = ocr_output_to_list(text)
    seps = ['n.', 'n', 'v.', 'v', 'v1', 'v2', 'v3',
            'v4', 'v5', 'adj.', 'adj', 'interj.', 
            'interj', 'adv.', 'adv', 'pron.', 'pron',
            'ad', 'm', 'm.', 'f', 'f.', 'conj.'
            ]
    n_lines = []
    for line in lines:
        words = line.split()
        for i, word in enumerate(words):
            if word in seps:
                n_line = []
                n_line.append(" ".join(words[:i]))
                n_line.append(" ".join(words[i:]))
                n_lines.append(n_line)
                break
        else:
            n_lines.append([line])

    with open("phrases" + ".csv", mode="w+", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for row in n_lines:
            writer.writerow(row)
            
    if echo:
        print("Done")
    return n_lines

def ocr_output_to_list(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != '']
    return lines

def combine_columns(image1, image2, output=None, echo=True):
    if output is None:
        output = "vocaby.csv"
    t1 = ocr_output_to_list(ocr_core(image=image1))
    t2 = ocr_output_to_list(ocr_core(image=image2))
    
    if echo:
        print("Writing to file...")
        
    with open(output + ".csv", mode="w+", newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for row in zip(t1, t2):
            writer.writerow(row)
    if echo:
        print("Done")
    
    
class GUI:
    def __init__(self, filename, output):
        self.filename = filename
        self.output_filename = output
        
        self.root = tk.Tk()
        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<B1-Motion>", self.on_motion)
        self.root.bind("<space>", self.on_space)
        self.root.bind("<Key>", self.on_key)
        self.canvas_height = 900
        self.canvas_width = 900
        self.canvas = tk.Canvas(self.root, bg="white", height=self.canvas_height, 
                                width=self.canvas_width)
        self.canvas.pack()
        
        self.image_original = Image.open(filename)
        self.image_scale_factor = 1
        self.scaled_image = self.scale_image(self.image_original)        
        self.photo = ImageTk.PhotoImage(self.scaled_image)
        self.img = self.canvas.create_image(0,0, image=self.photo, anchor=tk.NW)
        
        self.start_point = [0,0]
        self.crop_coords = [None, None]
        
        self.current_rect = 0
        self.rect1_onscreen = False
        self.rect2_onscreen = False
        
        self.cropped_image1 = None
        self.cropped_image2 = None
        
    def start(self):
        self.root.mainloop()

    # Scales the image and returns an unscaled copy of the original
    def scale_image(self, image_original):
        image_copy = image_original.copy()
        self.image_scale_factor = 800 / max(image_original.size)
        #print("Image Scaled by:\t" + str(image_scale_factor))
        max_size = (800,800)
        image_copy.thumbnail(max_size, Image.ANTIALIAS)
        
        return image_copy

    def columns_by_image(self):
        self.crop_selection(0)
        self.crop_selection(1)
        combine_columns(self.cropped_image1, self.cropped_image2, output=self.output_filename)

    def on_click(self, event):
        self.start_point[0] = event.x
        self.start_point[1] = event.y
    
    def on_motion(self, event):
        self.draw_rect(self.start_point[0], self.start_point[1], event.x, event.y)
        self.set_crop_coords(self.start_point[0], self.start_point[1], event.x, event.y)
    
    def set_crop_coords(self, x1,y1,x2,y2):
        self.crop_coords[self.current_rect] = (x1/self.image_scale_factor,y1/self.image_scale_factor,
                       x2/self.image_scale_factor,y2/self.image_scale_factor)
    
    def on_space(self, event):
        if self.rect1_onscreen and self.rect2_onscreen:
            self.columns_by_image()
        elif self.rect1_onscreen:
            self.crop_selection(0)
            text_to_csv(ocr_core(image= self.cropped_image1))
        elif self.rect2_onscreen:
            self.crop_selection(1)
            text_to_csv(ocr_core(image= self.cropped_image2))
    
    def crop_selection(self, rect_num):
        if rect_num == 0:
            self.cropped_image1 = self.image_original.crop(self.crop_coords[0])
        else:
            self.cropped_image2 = self.image_original.crop(self.crop_coords[1])
    
    def on_key(self, event):
        if event.char == '1':
            self.current_rect = 0
        if event.char == '2':
            self.current_rect = 1
        if event.char == 'c':
            self.clear_rect(0)
            self.clear_rect(1)
            
    def draw_rect(self, x1, y1, x2, y2):
        if self.current_rect == 0:
            self.clear_rect(0)
            self.rect1_onscreen = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")
        
        if self.current_rect == 1:
            self.clear_rect(1)
            self.rect2_onscreen = self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue")
            
    def clear_rect(self, rect_num):
        if rect_num == 0:
            if self.rect1_onscreen:
                self.canvas.delete(self.rect1_onscreen)
                self.rect1_onscreen = False
        elif rect_num == 1:
            if self.rect2_onscreen:
                self.canvas.delete(self.rect2_onscreen)
                self.rect2_onscreen = False
        

g = GUI("pictures/p3.png", "phrases.csv")
g.start()

