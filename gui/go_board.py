import tkinter as tk

class go_board(tk.Canvas):
    grid_size = 25
    stones = dict()
    move_allowed = True

    def __init__(self, master, move_callback_fn=None):
        tk.Canvas.__init__(self, master, relief=tk.RAISED, bd=4, bg="#F7EE8A",
            width=20 * self.grid_size, height=20 * self.grid_size, highlightthickness=0)
        self.bind("<1>", self.put_stone_on_click)
        self.move_callback_fn = move_callback_fn
        self.draw_board()
    
    def set_on_click_callback(self, on_click_fn):
        self.bind("<1>", on_click_fn)  
    
    def set_move_allowed(self, flag):
        self.move_allowed = flag
    
    def draw_board(self):
        en = self.grid_size * 19
        z = self.grid_size * 0.36
        for i in range(19):
            x = (i + 1) * self.grid_size
            self.create_line(x, self.grid_size, x, en)
            self.create_line(self.grid_size, x, en, x)

            self.create_text(z, x, text=str(i), justify=tk.RIGHT, fill="#002010", font=("Helvetica", "6", "normal"))
            self.create_text(x, z, text=str(i), justify=tk.CENTER, fill="#002010", font=("Helvetica", "6", "normal"))
        
        hosi = 2
        for i in range(4, 17, 6):
            for j in range(4, 17, 6):
                x = i * self.grid_size
                y = j * self.grid_size
                self.create_oval(x-hosi, y-hosi, x+hosi, y+hosi, fill="black")

    def clear_board(self):
        self.stones.clear()
        self.delete("stone")
    
    # def load_board(self, fname):
    #     fp = file(fname)
    #     lb, lw = eval(rm_cmt(fp.read()))
    #     fp.close()

    #     for row, col in lb:
    #         self.stones[(row, col)] = self.put_stone(row, col, "black")
        
    #     for row, col in lw:
    #         self.stones[(row, col)] = self.put_stone(row, col, "white")
        
    # def save_board(self, fname):
    #     lb = []
    #     lw = []

    #     for key, val in self.stones.items():
    #         if self.itemcget(val, "fill") == "black":
    #             lb.append(key)
    #         else:
    #             lw.append(key)
        
    #     fp = file(fname, "w")
    #     fp.write("-- ([black stones], [white stones])")
    #     fp.write("(\n    ")
    #     fp.write(str(lb))
    #     fp.write("(\n    ")
    #     fp.write(str(lw))
    #     fp.write("\n)\n")
    #     fp.close()
    
    def get_clicked_col_row(self, event):
        cx = self.canvasx(event.x, self.grid_size)
        cy = self.canvasy(event.y, self.grid_size)
        col = int(cx / self.grid_size) - 1
        row = int(cy / self.grid_size) - 1
        return col, row

    def put_stone_on_click(self, event, callback_fn=lambda col, row: None):
        col, row = self.get_clicked_col_row(event)

        if 0 <= row <= 18 and 0 <= col <= 18:
            if not ((row, col) in self.stones):
                self.stones[(row, col)] = self.put_stone(row, col, "black")
            elif self.itemcget(self.stones[(row, col)], "fill") == "black":
                self.itemconfig(self.stones[(row, col)], fill="white")
            else:
                self.delete(self.stones[(row, col)])
                del self.stones[(row, col)]
        callback_fn(col, row)  

    def put_white_on_click(self, event, callback_fn=lambda col, row: None):
        self.put_color_on_click(event, "white", callback_fn)

    def put_black_on_click(self, event, callback_fn):
        self.put_color_on_click(event, "black", callback_fn)

    def put_color_on_click(self, event, color, callback_fn):
        if self.move_allowed is False:
            return
        col, row = self.get_clicked_col_row(event)
        self.put_stone(row, col, color)
        callback_fn(col, row)  

    def put_stone(self, row, col, color):
        if 0 <= row <= 18 and 0 <= col <= 18 and not ((row, col) in self.stones):
            self.stones[(row, col)] = self.__draw_stone(row, col, color)  

    def __draw_stone(self, row, col, color):
        r = self.grid_size * 0.40
        x_left  = (col + 1) * self.grid_size - r
        x_right = (col + 1) * self.grid_size + r
        y_top   = (row + 1) * self.grid_size - r
        y_down  = (row + 1) * self.grid_size + r
        return self.create_oval(x_left, y_top, x_right, y_down, fill=color, tags="stone")

if __name__ == '__main__':
    g = go_board(None)
    g.pack()
    g.mainloop()