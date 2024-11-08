# Target for targeting
# Derek Fujimoto
# Sep 2020 

import matplotlib.patches as patches
from functools import partial
import numpy as np
import tkinter as tk
from tkinter import ttk

class Target(object):
    
    """
        Drawing shapes on lots of figures
        
        Data fields:
            ax_list: list of axis
            bccd: bccd object
            color: string, maplotlib color name for coloring everything
            figures: list of figures to update
            result_frame: ttk Frame object to update text on properties
            popup_target: popup_target object
            points: list of all DraggablePoints
    """

    # ======================================================================= #
    def __init__(self, popup_target, color, result_frame):
        
        self.bccd = popup_target.bccd 
        self.popup_target = popup_target 
        self.ax_list = []
        self.color = color
        self.result_frame = result_frame
        self.points = []
        self.result_entry = []
        self.pt_center = None
        
    # ======================================================================= #
    def disable_drag_points(self):
        """
            Prevent interaction with the draggable points
        """
        # reduce interaction region to zero
        for dragpt in self.points:
            for pt in dragpt.points: 
                try:
                    pt.set_pickradius(0)
                    pt.set_markersize(0)
                except Exception:
                    pass
        
    # ======================================================================= #
    def draw(self, ax):
        """
            Axis operations for drawing
        """
        
        # check if already drawin in these axes
        if ax in self.ax_list:
            raise RuntimeError("Axis already contains this target") 
                
        # connect with window close
        ax.figure.canvas.mpl_connect('close_event', partial(self.remove, ax=ax))
                
        # add axes to list
        self.ax_list.append(ax)
        
    # ======================================================================= #
    def enable_drag_points(self):
        """
            Enable interaction with the draggable points
        """
        # reset interaction region
        for dragpt in self.points:
            for pt in dragpt.points: 
                pt.set_pickradius(DraggablePoint.size)
                pt.set_markersize(DraggablePoint.size)
        
    # ======================================================================= #
    def remove(self, *args, ax=None):
        """
            Remove the DraggablePoints and patch from the axis
        """
        if ax not in self.ax_list:
            return
                
        # remove points 
        for pt in self.points:     
            pt.remove(ax)
            
        # remove patches
        for patch in ax.patches:
            if patch in self.patches:
                ax.patches.remove(patch)
                self.patches.remove(patch)
        
        # remove axis from list
        self.ax_list.remove(ax)
        
    # ======================================================================= #
    def remove_all(self):
        """
            Remove the DraggablePoints and patch from all axes
        """
        for ax in self.ax_list.copy():
            self.remove(ax=ax)
     
    # ======================================================================= #
    def update_center(self, x, y, do_set=True):
        pass
        
    # ======================================================================= #
    def update_center_x(self, _):
        """
            Update circle and draggable point based on typed input
        """
        
        try:
            x = float(self.x.get())
            y = float(self.y.get())
        except ValueError:
            return
        
        # update position
        self.pt_center.set_xdata(x)
        self.update_center(x, y, False)
   
    # ======================================================================= #
    def update_center_y(self, _):
        """
            Update circle and draggable point based on typed input
        """
        try:
            x = float(self.x.get())
            y = float(self.y.get())
        except ValueError:
            return
            
        # update position
        self.pt_center.set_ydata(y)
        self.update_center(x, y, False)
    
class Circle(Target):
    """
        Drawing circle target shapes on lots of figures
        
        Data fields:
            pt_center, pt_radius: DraggablePoints
            patches: mpl.patches for patches
            x, y: center coordinates
            r: radius
    """

    # ======================================================================= #
    def __init__(self, popup_target, color, result_frame, x, y, r):
        
        super().__init__(popup_target, color, result_frame)
        
        # save circle position
        self.x = tk.StringVar()
        self.y = tk.StringVar()
        self.r = tk.StringVar()
        
        self.x.set(x)
        self.y.set(y)
        self.r.set(r)
        
        fields = [self.x, self.y, self.r]
        labels = ['x0', 'y0', 'r']
        update_fns = [self.update_center_x, self.update_center_y, self.update_radius_pt]
        
        # make result lines
        for i in range(len(labels)):
            
            # make fields
            lab = ttk.Label(self.result_frame, text=f'{labels[i]} = ')
            entry = ttk.Entry(self.result_frame, 
                            textvariable=fields[i], 
                            width=10, 
                            justify='right')
            
            entry.bind('<KeyRelease>', update_fns[i])
                            
            # grid
            lab.grid(column=0, row=i, padx=5, pady=5)
            entry.grid(column=1, row=i, padx=5, pady=5)
            
            self.result_entry.append(entry)
        
        # place circle at the center of the window
        self.patches = []
        
        # center
        self.pt_center = DraggablePoint(self, self.update_center, 
                            setx=True, sety=True, color=self.color, marker='x')
        
        # radius
        self.pt_radius = DraggablePoint(self, self.update_radius, 
                            setx=True, sety=False, color=self.color, marker='o')
        
        self.points = [self.pt_center, self.pt_radius]
        
    # ======================================================================= #
    def draw(self, ax):
        """Add the target to the current axes"""
        
        super().draw(ax)

        x = float(self.x.get())
        y = float(self.y.get())
        r = float(self.r.get())
        
        # draw things
        self.patches.append(patches.Circle((x, y), r, 
                                     fill=False, 
                                     facecolor='none', 
                                     lw=1, 
                                     ls='-', 
                                     edgecolor=self.color))
        ax.add_patch(self.patches[-1])
        self.pt_center.add_ax(ax, x, y)
        self.pt_radius.add_ax(ax, x+r, y, )

    # ======================================================================= #
    def update_center(self, x, y, do_set=True):
        """
            Update circle position based on DraggablePoint
        """
        
        try:
            r = float(self.r.get())
        except ValueError:
            return
        
        self.pt_radius.set_xdata(x+r)
        self.pt_radius.set_ydata(y)
        
        for c in self.patches:
            c.set_center((x, y))
        
        if do_set:
            self.x.set(f'{x:.2f}')
            self.y.set(f'{y:.2f}')
            
    # ======================================================================= #
    def update_radius(self, x, y, do_set=True):
        """
            Update circle radius based on DraggablePoint
        """

        try:
            r = abs(float(self.x.get())-x)
        except ValueError:
            return
        
        if do_set:
            self.r.set(f'{r:.2f}')
        
        for c in self.patches:
            c.set_radius(r)
    
    # ======================================================================= #
    def update_radius_pt(self, _):
        """
            Update circle and draggable point based on typed input
        """
        try:
            r = float(self.r.get())
            x = float(self.x.get())
            y = float(self.y.get())
        except ValueError:
            return
            
        # update position
        self.pt_radius.set_xdata(x+r)
        self.update_radius(x+r, y, False)
    
class Square(Target):
    """
        Drawing square target shapes on lots of figures
        
        Data fields:
            pt_center, pt_side: DraggablePoints
            square: mpl.patches for patches
            x, y: center coordinates
            side: side length
    """

    # ======================================================================= #
    def __init__(self, popup_target, color, result_frame, x, y, side):
        
        super().__init__(popup_target, color, result_frame)
        
        # save square position
                # save circle position
        self.x = tk.StringVar()
        self.y = tk.StringVar()
        self.side = tk.StringVar()
        
        self.x.set(x)
        self.y.set(y)
        self.side.set(side)
        
        fields = [self.x, self.y, self.side]
        labels = ['x0', 'y0', 'side']
        update_fns = [self.update_center_x, self.update_center_y, self.update_side_pt]
        
        # make result lines
        for i in range(len(labels)):
            
            # make fields
            lab = ttk.Label(self.result_frame, text=f'{labels[i]} = ')
            entry = ttk.Entry(self.result_frame, 
                            textvariable=fields[i], 
                            width=10, 
                            justify='right')
            
            entry.bind('<KeyRelease>', update_fns[i])
                            
            # grid
            lab.grid(column=0, row=i, padx=5, pady=5)
            entry.grid(column=1, row=i, padx=5, pady=5)
            
            self.result_entry.append(entry)
        
        # place circle at the center of the window
        self.patches = []
        
        # center
        self.pt_center = DraggablePoint(self, self.update_center, 
                            setx=True, sety=True, color=self.color, marker='x')
        
        # radius
        self.pt_side = DraggablePoint(self, self.update_side, 
                            setx=True, sety=False, color=self.color, marker='s')
        
        self.points = [self.pt_center, self.pt_side]
        
    # ======================================================================= #
    def draw(self, ax):
        """Add the target to the current axes"""
        
        super().draw(ax)
        
        try:
            x = float(self.x.get())
            y = float(self.y.get())
            side = float(self.side.get())
        except ValueError:
            return
            
        # draw things
        self.patches.append(patches.Rectangle((x-side/2, y-side/2), 
                                            width=side, 
                                            height=side, 
                                            fill=False, 
                                            facecolor='none', 
                                            lw=1, 
                                            ls='-', 
                                            edgecolor=self.color))
        ax.add_patch(self.patches[-1])
        self.pt_center.add_ax(ax, x, y)
        self.pt_side.add_ax(ax, x+side/2, y)
       
    # ======================================================================= #
    def update_center(self, x, y, do_set=True):
        """
            Update circle position based on DraggablePoint
        """
        
        try:
            side = float(self.side.get())
        except ValueError:
            return
        
        self.pt_side.set_xdata(x+side/2)
        self.pt_side.set_ydata(y)
        
        for c in self.patches:
            c.set_xy((x-side/2, y-side/2))
        
        if do_set:
            self.x.set(f'{x:.2f}')
            self.y.set(f'{y:.2f}')
            
    # ======================================================================= #
    def update_side(self, x, y, do_set=True):
        """
            Update circle radius based on DraggablePoint
        """

        try:
            dx = abs(float(self.x.get())-x)*2
            x = float(self.x.get())
            y = float(self.y.get())
        except ValueError:
            return
            
        for c in self.patches:
            c.set_xy((x-dx/2, y-dx/2))
            c.set_height(dx)
            c.set_width(dx)
        
        if do_set:
            self.side.set(f'{dx:.2f}')
        
    # ======================================================================= #
    def update_side_pt(self, _):
        """
            Update circle and draggable point based on typed input
        """
        try:
            side = float(self.side.get())
            x = float(self.x.get())
            y = float(self.y.get())
        except ValueError:
            return
            
        # update position
        self.pt_side.set_xdata(x+side/2)
        self.update_side(x+side/2, y, False)
        
class Rectangle(Target):
    """
        Drawing Rectangle target shapes on lots of figures
        
        Data fields:
            pt_tr, pt_tl, pt_br, pt_bl: DraggablePoints
            patches:    mpl.patches for patches
            x, y:    center coordinates
            dx, dy:  side length
    """

    # ======================================================================= #
    def __init__(self, popup_target, color, result_frame, x, y, side):
        
        super().__init__(popup_target, color, result_frame)
        
        # save rectangle position
        self.x = tk.StringVar()
        self.y = tk.StringVar()
        self.dx = tk.StringVar()
        self.dy = tk.StringVar()
        
        self.x.set(x)
        self.y.set(y)
        self.dx.set(side*2)
        self.dy.set(side*2)
        
        fields = [self.x, self.y, self.dx, self.dy]
        labels = ['x0', 'y0', 'side x', 'side y']
        
        # make result lines
        for i in range(len(labels)):
            
            # make fields
            lab = ttk.Label(self.result_frame, text=f'{labels[i]} = ')
            entry = ttk.Entry(self.result_frame, 
                            textvariable=fields[i], 
                            width=10, 
                            justify='right')
            
            entry.bind('<KeyRelease>', self.update_typed)
                            
            # grid
            lab.grid(column=0, row=i, padx=5, pady=5)
            entry.grid(column=1, row=i, padx=5, pady=5)
            
            self.result_entry.append(entry)
        
        # place circle at the center of the window
        self.patches = []
        
        # corner points (tr = top right)
        self.pt_tl = DraggablePoint(self, self.update_tl, 
                            setx=True, sety=True, color=self.color, marker='s')
        
        self.pt_tr = DraggablePoint(self, self.update_tr, 
                            setx=True, sety=True, color=self.color, marker='s')

        self.pt_br = DraggablePoint(self, self.update_br, 
                            setx=True, sety=True, color=self.color, marker='s')

        self.pt_bl = DraggablePoint(self, self.update_bl, 
                            setx=True, sety=True, color=self.color, marker='s')
        
        self.points = [self.pt_tl, self.pt_tr, self.pt_br, self.pt_bl]
        
    # ======================================================================= #
    def draw(self, ax):
        """Add the target to the current axes"""
        
        super().draw(ax)
        
        try:
            x = float(self.x.get())
            y = float(self.y.get())
            dx = float(self.dx.get())/2
            dy = float(self.dy.get())/2
        except KeyError:
            return
        
        # draw things
        self.patches.append(patches.Rectangle((x-dx, y-dy), 
                                            width=dx*2, 
                                            height=dy*2, 
                                            fill=False, 
                                            facecolor='none', 
                                            lw=1, 
                                            ls='-', 
                                            edgecolor=self.color))
        ax.add_patch(self.patches[-1])
        self.pt_tr.add_ax(ax, x+dx, y+dy)
        self.pt_tl.add_ax(ax, x-dx, y+dy)
        self.pt_br.add_ax(ax, x+dx, y-dy)
        self.pt_bl.add_ax(ax, x-dx, y-dy)
        
    # ======================================================================= #
    def update_typed(self, _):
        """
            Update shape and draggable point based on typed input
        """
        
        try:
            x = float(self.x.get())
            y = float(self.y.get())
            dx = float(self.dx.get())/2
            dy = float(self.dy.get())/2
        except KeyError:
            return
            
        # update points
        self.pt_tl.set_xdata(x-dx)
        self.pt_bl.set_xdata(x-dx)
        self.pt_tr.set_xdata(x+dx)
        self.pt_br.set_xdata(x+dx)
        
        # update shape
        self.update_tl(x-dx, y+dy, False)
        self.update_tr(x+dx, y+dy, False)
        self.update_bl(x-dx, y-dy, False)
        self.update_br(x+dx, y-dy, False)
        
    # ======================================================================= #
    def update_tr(self, x, y, do_set=True):
        """
            Update top right position based on DraggablePoint
        """
        
        self.pt_tl.set_ydata(y)
        self.pt_br.set_xdata(x)
        
        ddx = x - int(self.pt_tl.get_xdata())
        ddy = y - int(self.pt_br.get_ydata())
        
        dx = round(ddx/2)
        dy = round(ddy/2)
        
        for c in self.patches:
            c.set_xy((x-ddx, y-ddy))
            c.set_width(ddx)
            c.set_height(ddy)
        
        if do_set:
            self.x.set(f'{x-dx:.2f}')
            self.y.set(f'{y-dy:.2f}')
            
            self.dx.set(f'{abs(dx)*2:.2f}')
            self.dy.set(f'{abs(dy)*3:.2f}')
    
    # ======================================================================= #
    def update_tl(self, x, y, do_set=True):
        """
            Update top left position based on DraggablePoint
        """
        self.pt_tr.set_ydata(y)
        self.pt_bl.set_xdata(x)
        
        ddx = int(self.pt_tr.get_xdata()) - x
        ddy = y- int(self.pt_bl.get_ydata())
        
        dx = round(ddx/2)
        dy = round(ddy/2)
        
        for c in self.patches:
            c.set_xy((x, y-ddy))
            c.set_width(ddx)
            c.set_height(ddy)
        
        if do_set:
            self.x.set(f'{x+dx:.2f}')
            self.y.set(f'{y-dy:.2f}')
            
            self.dx.set(f'{abs(dx)*2:.2f}')
            self.dy.set(f'{abs(dy)*2:.2f}')
        
    # ======================================================================= #
    def update_br(self, x, y, do_set=True):
        """
            Update bottom right position based on DraggablePoint
        """
        self.pt_bl.set_ydata(y)
        self.pt_tr.set_xdata(x)
        
        ddx = x - int(self.pt_bl.get_xdata())
        ddy = int(self.pt_tr.get_ydata()) - y
        
        dx = round(ddx/2)
        dy = round(ddy/2)
        
        for c in self.patches:
            c.set_xy((x-ddx, y))
            c.set_width(ddx)
            c.set_height(ddy)
        
        if do_set:
        
            self.x.set(f'{x-dx:.2f}')
            self.y.set(f'{y+dy:.2f}')
            
            self.dx.set(f'{abs(dx)*2:.2f}')
            self.dy.set(f'{abs(dy)*2:.2f}')
            
    # ======================================================================= #
    def update_bl(self, x, y, do_set=True):
        """
            Update bottom left position based on DraggablePoint
        """
        self.pt_br.set_ydata(y)
        self.pt_tl.set_xdata(x)
        
        ddx = int((self.pt_br.get_xdata() - x))
        ddy = int((self.pt_tl.get_ydata() - y))
        
        dx = round(ddx/2)
        dy = round(ddy/2)
        
        for c in self.patches:
            c.set_xy((x, y))
            c.set_width(ddx)
            c.set_height(ddy)
        
        if do_set:
            self.x.set(f'{x+dx:.2f}')
            self.y.set(f'{y+dy:.2f}')
            
            self.dx.set(f'{abs(dx)*2:.2f}')
            self.dy.set(f'{abs(dy)*2:.2f}')
                
class Ellipse(Target):
    """
        Drawing ellipse target shapes on lots of figures
        
        Data fields:
            pt_center, pt_radius1, pt_radius2: DraggablePoints
            patches: mpl.patches for patches
            x, y: center coordinates
            r1, r2: radius
    """
    
    # minimum radius able to set
    rmin = 10

    # ======================================================================= #
    def __init__(self, popup_target, color, result_frame, x, y, r1, r2):
        
        super().__init__(popup_target, color, result_frame)
        
        # save circle position
        self.x = tk.StringVar()
        self.y = tk.StringVar()
        self.r1 = tk.StringVar()
        self.r2 = tk.StringVar()
        self.angle = tk.StringVar()
        
        self.x.set(x)
        self.y.set(y)
        self.r1.set(r1)
        self.r2.set(r2)
        self.angle.set(0)
        
        fields = [self.x, self.y, self.r1, self.r2, self.angle]
        labels = ['x0', 'y0', 'r1', 'r2', 'angle']
        update_fns = [self.update_center_x, self.update_center_y, 
                      self.update_radius1_pt, self.update_radius2_pt,
                      self.update_angle]
        
        # make result lines
        for i in range(len(labels)):
            
            # make fields
            lab = ttk.Label(self.result_frame, text=f'{labels[i]} = ')
            entry = ttk.Entry(self.result_frame, 
                            textvariable=fields[i], 
                            width=10, 
                            justify='right')
            
            entry.bind('<KeyRelease>', update_fns[i])
                            
            # grid
            lab.grid(column=0, row=i, padx=5, pady=5, sticky='e')
            entry.grid(column=1, row=i, padx=5, pady=5)
            
            self.result_entry.append(entry)
        
        # place circle at the center of the window
        self.patches = []
        
        # center
        self.pt_center = DraggablePoint(self, self.update_center, 
                            setx=True, sety=True, color=self.color, marker='x')
        
        # radius
        self.pt_radius1 = DraggablePoint(self, self.update_radius1, 
                            setx=True, sety=True, color=self.color, marker='o')
        
        self.pt_radius2 = DraggablePoint(self, self.update_radius2, 
                            setx=True, sety=True, color=self.color, marker='o')
        
        self.points = [self.pt_center, self.pt_radius1, self.pt_radius2]
        
    # ======================================================================= #
    def draw(self, ax):
        """Add the target to the current axes"""
        
        super().draw(ax)
        
        x = float(self.x.get())
        y = float(self.y.get())
        r1 = float(self.r1.get())
        r2 = float(self.r2.get())
        angle = float(self.angle.get())/180*np.pi
        
        # draw things
        self.patches.append(patches.Ellipse((x, y), 
                                     width=r1*2, 
                                     height=r2*2, 
                                     angle=angle*180/np.pi, 
                                     fill=False, 
                                     facecolor='none', 
                                     lw=1, 
                                     ls='-', 
                                     edgecolor=self.color))
        ax.add_patch(self.patches[-1])
        self.pt_center.add_ax(ax, x, y)
        self.pt_radius1.add_ax(ax,  x+r1*np.cos(angle), 
                                    y+r1*np.sin(angle))
        self.pt_radius2.add_ax(ax,  x+r2*np.sin(angle), 
                                    y+r2*np.cos(angle))

    # ======================================================================= #
    def update_center(self, x, y, do_set=True):
        """
            Update circle position based on DraggablePoint
        """
        
        try:
            r1 = float(self.r1.get())
            r2 = float(self.r2.get())
            angle = float(self.angle.get())/180*np.pi
        except ValueError:
            return
        
        self.pt_radius1.set_xdata(x+r1*np.cos(angle))
        self.pt_radius1.set_ydata(y+r1*np.sin(angle))
        self.pt_radius2.set_xdata(x+r2*np.sin(angle))
        self.pt_radius2.set_ydata(y+r2*np.cos(angle))
        
        for c in self.patches:
            c.set_center((x, y))
        
        if do_set:
            self.x.set(f'{x:.2f}')
            self.y.set(f'{y:.2f}')
    
    # ======================================================================= #
    def update_radius1(self, x, y, do_set=True):
        """
            Update circle radius based on DraggablePoint
        """
        
        x0 = float(self.x.get())
        y0 = float(self.y.get())
        r1 = float(self.r1.get())
        r2 = float(self.r2.get())
        angle = float(self.angle.get())/180*np.pi
        
        # calculate the xy distance
        dx = x-x0
        dy = y-y0

        # get the radius 
        r1 = np.sqrt(dx**2+dy**2)
        
        # prevent too small of a radius
        if r1 < self.rmin and do_set:
            r1 = self.rmin
            self.pt_radius1.set_xdata(x0+r1*np.cos(angle))
            self.pt_radius1.set_ydata(y0+r1*np.sin(angle))
        
        # get the angle 
        try:
            a = np.arctan(dy/dx)
        except RuntimeWarning:
            pass
        else:
            angle = a
            
        # big angles
        if dx < 0:
            angle += np.pi
        
        # set patch
        for c in self.patches:
            c.set_width(r1*2)
            c.set_angle(angle*180/np.pi)
            
        # set r2
        self.pt_radius2.set_xdata(x0+r2*np.cos(angle+np.pi/2))
        self.pt_radius2.set_ydata(y0+r2*np.sin(angle+np.pi/2))
            
        if do_set:
            self.r1.set(f'{r1:.2f}')
            self.angle.set(f'{angle*180/np.pi:.2f}')
    
    # ======================================================================= #
    def update_radius2(self, x, y, do_set=True):
        """
            Update circle radius based on DraggablePoint
        """

        x0 = float(self.x.get())
        y0 = float(self.y.get())
        r1 = float(self.r1.get())
        r2 = float(self.r2.get())
        angle = float(self.angle.get())/180*np.pi
        
        # calculate the xy distance
        dx = x-x0
        dy = y-y0

        # get the radius 
        r2 = np.sqrt(dx**2+dy**2)
        
        # prevent too small of a radius
        if r2 < self.rmin and do_set:
            r2 = self.rmin
            self.pt_radius2.set_xdata(x0+r2*np.cos(angle+np.pi/2))
            self.pt_radius2.set_ydata(y0+r2*np.sin(angle+np.pi/2))
        
        # get the angle 
        try:
            a = np.arctan(dy/dx)+np.pi/2
        except RuntimeWarning:
            pass
        else:
            angle = a
        
         # big angles
        if dx > 0:
            angle -= np.pi
            
        # set patch
        for c in self.patches:
            c.set_height(r2*2)
            c.set_angle(angle*180/np.pi)
            
        # set r1
        self.pt_radius1.set_xdata(x0+r1*np.cos(angle))
        self.pt_radius1.set_ydata(y0+r1*np.sin(angle))       
        
        if do_set:
            self.r2.set(f'{r2:.2f}')
            self.angle.set(f'{angle*180/np.pi:.2f}')

    # ======================================================================= #
    def update_radius1_pt(self, _): 
        """
            Update circle and draggable point based on typed input
        """
        try:
            r1 = float(self.r1.get())
            x = float(self.x.get())
            y = float(self.y.get())
            angle = float(self.angle.get())*np.pi/180
        except ValueError:
            return
            
        # get new positions
        r1_x = abs(x+r1*np.cos(angle))
        r1_y = abs(y+r1*np.sin(angle))
        
        # update position
        self.pt_radius1.set_xdata(r1_x)
        self.pt_radius1.set_ydata(r1_y)
        self.update_radius1(r1_x, r1_y, False)
        
    def update_radius2_pt(self, _):
        """
            Update circle and draggable point based on typed input
        """
        try:
            r2 = float(self.r2.get())
            x = float(self.x.get())
            y = float(self.y.get())
            angle = float(self.angle.get())*np.pi/180
        except ValueError:
            return
            
        # get new positions
        r2_x = abs(x+r2*np.cos(angle+np.pi/2))
        r2_y = abs(y+r2*np.sin(angle+np.pi/2))
        
        # update position
        self.pt_radius2.set_xdata(r2_x)
        self.pt_radius2.set_ydata(r2_y)
        self.update_radius2(r2_x, r2_y, False)
        
    def update_angle(self, _):
        """
            Update circle and draggable point based on typed input
        """
        try:
            r1 = float(self.r1.get())
            r2 = float(self.r2.get())
            x = float(self.x.get())
            y = float(self.y.get())
            angle = float(self.angle.get())*np.pi/180
        except ValueError:
            return
            
        # get new positions
        r1_x = abs(x+r1*np.cos(angle))
        r1_y = abs(y+r1*np.sin(angle))
        r2_x = abs(x+r2*np.cos(angle+np.pi/2))
        r2_y = abs(y+r2*np.sin(angle+np.pi/2))
        
        # update position
        self.pt_radius1.set_xdata(r1_x)
        self.pt_radius1.set_ydata(r1_y)
        self.pt_radius2.set_xdata(r2_x)
        self.pt_radius2.set_ydata(r2_y)
        self.update_radius1(r1_x, r1_y, False)
        self.update_radius2(r2_x, r2_y, False)
    
class DraggablePoint:

    # http://stackoverflow.com/questions/21654008/matplotlib-drag-overlapping-points-interactively
    # https://stackoverflow.com/questions/28001655/draggable-line-with-draggable-points
    
    lock = None #  only one can be animated at a time
    size=8

    # ======================================================================= #
    def __init__(self, parent, updatefn, setx=True, sety=True, color=None, marker='s'):
        """
            parent: parent object
            points: list of point objects, corresponding to the various axes 
                    the target is drawn in 
            updatefn: funtion which updates the line in the corpatchest way
                updatefn(xdata, ydata)
            x, y: initial point position
            setx, sety: if true, allow setting this parameter
            color: point color
        """
        self.parent = parent
        self.points = []
        self.color = color
        self.marker = marker
            
        self.updatefn = updatefn
        self.setx = setx
        self.sety = sety
        self.press = None
        self.background = None
        
        # trackers for connections
        self.cidpress = []
        self.cidrelease = []
        self.cidmotion = []
        
    # ======================================================================= #
    def add_ax(self, ax, x=None, y=None):
        """Add axis to list of axes"""
        
        self.disconnect()
        
        if x is None:
            x = self.get_xdata()
        if y is None:
            y = self.get_ydata()
            
        self.points.append(ax.plot(x, y, zorder=100, color=self.color, alpha=0.5, 
                        marker=self.marker, markersize=self.size)[0])
        self.points[-1].set_pickradius(self.size)
        
        self.connect()
        
    # ======================================================================= #
    def connect(self):
        """connect to all the events we need"""
        
        # trackers for connections
        self.cidpress = []
        self.cidrelease = []
        self.cidmotion = []
        
        for i, pt in enumerate(self.points):
            self.cidpress.append(pt.figure.canvas.mpl_connect('button_press_event', 
                                partial(self.on_press, id=i)))
                                 
            self.cidrelease.append(pt.figure.canvas.mpl_connect('button_release_event', 
                                self.on_release))
                                
            self.cidmotion.append(pt.figure.canvas.mpl_connect('motion_notify_event', 
                                partial(self.on_motion, id=i)))
    
    # ======================================================================= #
    def on_press(self, event, id):
        
        if event.inaxes != self.points[id].axes: return
        if DraggablePoint.lock is not None: return
        contains, attrd = self.points[id].contains(event)
        if not contains: return
        DraggablePoint.lock = self
        
    # ======================================================================= #
    def on_motion(self, event, id):

        if DraggablePoint.lock is not self: return
        if event.inaxes != self.points[id].axes: return
        
        # get data
        x = event.xdata
        y = event.ydata
        
        # move the point
        if self.setx:   self.set_xdata(x)
        if self.sety:   self.set_ydata(y)

        # update the line
        self.updatefn(x, y)        

    # ======================================================================= #
    def on_release(self, event):
        'on release we reset the press data'
        if DraggablePoint.lock is not self: return
        DraggablePoint.lock = None
        
    # ======================================================================= #
    def disconnect(self):
        'disconnect all the stored connection ids'
        
        for i, pt in enumerate(self.points):
            pt.figure.canvas.mpl_disconnect(self.cidpress[i])
            pt.figure.canvas.mpl_disconnect(self.cidrelease[i])
            pt.figure.canvas.mpl_disconnect(self.cidmotion[i])
                
    # ======================================================================= #
    def get_xdata(self):
        """Get x coordinate"""
        return self.points[0].get_xdata()
            
    # ======================================================================= #
    def get_ydata(self):
        """Get y coordinate"""
        return self.points[0].get_ydata()
            
    # ======================================================================= #
    def remove(self, ax):
        """
            Remove drawn points from the axis.
        """
    
        self.disconnect()
        del_list = []
        
        # remove from draggable points
        for i, line in enumerate(ax.lines):
            for pt in self.points:
                if line is pt:
                    del_list.append(i)
                    self.points.remove(line)
                    del line
        
        # remove from mpl
        for d in del_list:
            ax.lines[d].remove()
        
        self.connect()
            
    # ======================================================================= #
    def set_xdata(self, x):
        """Set x coordinate"""
        for pt in self.points:
            pt.set_xdata([x])    
            
    # ======================================================================= #
    def set_ydata(self, y):
        """Set y coordinate"""
        for pt in self.points:
            pt.set_ydata([y])
