"""
Animation utilities for VocabLoury application
"""

import customtkinter as ctk
import random
import math
from config.settings import ANIMATION_INTERVAL, PARTICLE_COUNT, COLORS, THEME_MODE


class AnimatedBackground(ctk.CTkFrame):
    """Enhanced animated background with floating particles and gradients"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.particles = []
        self.animation_running = True
        self.time = 0
        self.create_particles()
        self.animate()
    
    def create_particles(self):
        """Create floating particles with enhanced properties"""
        for _ in range(PARTICLE_COUNT):  # More particles
            particle = {
                'x': random.randint(0, 1400),
                'y': random.randint(0, 800),
                'size': random.randint(1, 4),
                'speed_x': random.uniform(-0.5, 0.5),
                'speed_y': random.uniform(-0.5, 0.5),
                'opacity': random.uniform(0.1, 0.4),
                'color': random.choice(['#1f538d', '#3B8ED0', '#ffffff', '#cccccc']),
                'pulse_speed': random.uniform(0.02, 0.05),
                'pulse_phase': random.uniform(0, 2 * math.pi)
            }
            self.particles.append(particle)
    
    def animate(self):
        """Animate particles with enhanced effects"""
        if not self.animation_running:
            return
        
        self.time += 0.02
        
        # Update particle positions
        for particle in self.particles:
            # Add subtle floating motion
            particle['x'] += particle['speed_x'] + math.sin(self.time + particle['pulse_phase']) * 0.2
            particle['y'] += particle['speed_y'] + math.cos(self.time + particle['pulse_phase']) * 0.2
            
            # Pulsing opacity
            particle['opacity'] = 0.2 + 0.2 * math.sin(self.time * particle['pulse_speed'] + particle['pulse_phase'])
            
            # Bounce off edges with smooth transitions
            if particle['x'] <= 0 or particle['x'] >= 1400:
                particle['speed_x'] *= -0.8
            if particle['y'] <= 0 or particle['y'] >= 800:
                particle['speed_y'] *= -0.8
                
            # Keep particles in bounds
            particle['x'] = max(0, min(1400, particle['x']))
            particle['y'] = max(0, min(800, particle['y']))
        
        # Schedule next animation frame
        self.after(ANIMATION_INTERVAL, self.animate)  # Faster animation


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


class TypingAnimation:
    """Typing animation effect for text"""
    
    def __init__(self, widget, text, delay=50):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.current_text = ""
        self.index = 0
        self.is_running = False
    
    def start(self):
        """Start the typing animation"""
        self.is_running = True
        self.current_text = ""
        self.index = 0
        self._type_next_char()
    
    def stop(self):
        """Stop the typing animation"""
        self.is_running = False
    
    def _type_next_char(self):
        """Type the next character"""
        if not self.is_running or self.index >= len(self.text):
            return
        
        self.current_text += self.text[self.index]
        self.widget.configure(text=self.current_text)
        self.index += 1
        
        # Schedule next character
        self.widget.after(self.delay, self._type_next_char)
