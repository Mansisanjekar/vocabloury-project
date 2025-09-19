"""
Animation utilities for VocabLoury application
"""

import customtkinter as ctk
import random
from config.settings import ANIMATION_INTERVAL, PARTICLE_COUNT, COLORS, THEME_MODE


class AnimatedBackground(ctk.CTkFrame):
    """Animated background with floating particles"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.particles = []
        self.animation_running = True
        self.create_particles()
        self.animate()
    
    def create_particles(self):
        """Create floating particles"""
        for _ in range(PARTICLE_COUNT):
            particle = {
                'x': random.randint(0, 1200),
                'y': random.randint(0, 800),
                'size': random.randint(2, 6),
                'speed_x': random.uniform(-1, 1),
                'speed_y': random.uniform(-1, 1),
                'opacity': random.uniform(0.3, 0.8)
            }
            self.particles.append(particle)
    
    def animate(self):
        """Animate particles"""
        if not self.animation_running:
            return
            
        # Update particle positions
        for particle in self.particles:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            # Bounce off edges
            if particle['x'] <= 0 or particle['x'] >= 1200:
                particle['speed_x'] *= -1
            if particle['y'] <= 0 or particle['y'] >= 800:
                particle['speed_y'] *= -1
            
            # Keep particles in bounds
            particle['x'] = max(0, min(1200, particle['x']))
            particle['y'] = max(0, min(800, particle['y']))
        
        # Schedule next animation frame
        self.after(ANIMATION_INTERVAL, self.animate)


class AnimatedButton(ctk.CTkButton):
    """Button with hover animations"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.original_fg_color = kwargs.get('fg_color', ["#3B8ED0", "#1F6AA5"])
        self.original_hover_color = kwargs.get('hover_color', ["#36719F", "#144870"])
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        """Animation on mouse enter"""
        self.configure(fg_color=self.original_hover_color)
    
    def on_leave(self, event):
        """Animation on mouse leave"""
        self.configure(fg_color=self.original_fg_color)


def darken_color(color):
    """Darken a hex color for hover effect"""
    color_map = {
        "#1f538d": "#1a4a7a",
        "#0078d4": "#005a9e",
        "#2196F3": "#1976D2",
        "#4CAF50": "#388E3C",
        "#FF9800": "#F57C00",
        "#9C27B0": "#7B1FA2"
    }
    return color_map.get(color, color)
