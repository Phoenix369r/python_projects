import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
import os
import math
import random
from PIL import Image, ImageTk, ImageFilter
import pygame


class PremiumDangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Most Dangerous Writing App - Premium Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        self.root.attributes('-alpha', 0.0)  # Start invisible for fade-in effect

        # Initialize pygame for sound effects
        try:
            pygame.mixer.init()
            self.sound_enabled = True
        except:
            self.sound_enabled = False

        # Timer settings
        self.danger_time = 5.0
        self.last_keystroke = time.time()
        self.timer_running = False
        self.countdown_active = False
        self.update_job = None

        # Visual effects state
        self.red_screen_active = False
        self.blur_effect_active = False
        self.pulse_animation = 0
        self.shake_intensity = 0
        self.glow_intensity = 0
        self.particle_systems = []

        # Animation variables
        self.fade_alpha = 0.0
        self.screen_shake_x = 0
        self.screen_shake_y = 0
        self.danger_pulse = 0
        self.neon_glow = 0

        # UI Elements
        self.canvas = None
        self.red_overlay = None
        self.blur_overlay = None

        # Statistics
        self.words_written = 0
        self.sessions_completed = 0
        self.current_session_start = None

        # Load settings
        self.load_settings()

        # Setup UI
        self.setup_premium_ui()

        # Start animations
        self.start_fade_in()
        self.start_continuous_animations()

        # Start the timer update loop
        self.update_timer()

        # Bind events
        self.setup_events()

    def setup_premium_ui(self):
        # Create main canvas for effects
        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0,
            bg='#0a0a0a'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Main container frame with gradient effect
        self.main_frame = tk.Frame(self.canvas, bg='#0a0a0a')
        self.canvas_window = self.canvas.create_window(0, 0, anchor='nw', window=self.main_frame)

        # Bind canvas resize
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        # Create gradient background
        self.create_gradient_background()

        # Header frame with glassmorphism effect
        header_frame = tk.Frame(self.main_frame, bg='#1a1a2e', relief='flat', bd=0)
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))

        # Title with neon glow effect
        self.title_label = tk.Label(
            header_frame,
            text="⚡ THE MOST DANGEROUS WRITING APP ⚡",
            font=('Orbitron', 24, 'bold'),
            fg='#00ffff',
            bg='#1a1a2e',
            relief='flat'
        )
        self.title_label.pack(pady=20)

        # Timer display with dramatic styling
        timer_container = tk.Frame(header_frame, bg='#1a1a2e')
        timer_container.pack(fill=tk.X, pady=10)

        self.timer_label = tk.Label(
            timer_container,
            text="⚡ READY TO WRITE ⚡",
            font=('Orbitron', 18, 'bold'),
            fg='#00ff41',
            bg='#1a1a2e'
        )
        self.timer_label.pack()

        # Danger bar (visual timer)
        self.danger_bar_frame = tk.Frame(timer_container, bg='#1a1a2e', height=10)
        self.danger_bar_frame.pack(fill=tk.X, pady=(10, 0))

        self.danger_bar = tk.Canvas(
            self.danger_bar_frame,
            height=10,
            bg='#333333',
            highlightthickness=0
        )
        self.danger_bar.pack(fill=tk.X)

        # Status frame
        status_frame = tk.Frame(self.main_frame, bg='#16213e', relief='flat', bd=0)
        status_frame.pack(fill=tk.X, padx=30, pady=10)

        # Word count with glow
        self.word_count_label = tk.Label(
            status_frame,
            text="Words: 0",
            font=('Orbitron', 14, 'bold'),
            fg='#ffd700',
            bg='#16213e'
        )
        self.word_count_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Control buttons with hover effects
        controls_frame = tk.Frame(status_frame, bg='#16213e')
        controls_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        # Full screen button
        self.fullscreen_btn = self.create_neon_button(
            controls_frame, "🔳 FULLSCREEN", self.toggle_fullscreen, '#ff6b35'
        )
        self.fullscreen_btn.pack(side=tk.RIGHT, padx=5)

        # Settings button
        self.settings_btn = self.create_neon_button(
            controls_frame, "⚙️ SETTINGS", self.open_premium_settings, '#9d4edd'
        )
        self.settings_btn.pack(side=tk.RIGHT, padx=5)

        # Save button
        self.save_btn = self.create_neon_button(
            controls_frame, "💾 SAVE", self.save_text_premium, '#06ffa5'
        )
        self.save_btn.pack(side=tk.RIGHT, padx=5)

        # Text area container
        text_container = tk.Frame(self.main_frame, bg='#0a0a0a')
        text_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Text area with cyberpunk styling
        self.text_area = tk.Text(
            text_container,
            font=('Consolas', 16),
            bg='#0d1421',
            fg='#00ff41',
            insertbackground='#00ffff',
            selectbackground='#ff6b35',
            selectforeground='#000000',
            wrap=tk.WORD,
            border=0,
            padx=30,
            pady=30,
            relief='flat'
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Add subtle border glow to text area
        self.text_area.configure(highlightthickness=2, highlightcolor='#00ffff')

        # Welcome message with typewriter effect
        self.show_welcome_message()

    def create_neon_button(self, parent, text, command, color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Orbitron', 10, 'bold'),
            fg=color,
            bg='#1a1a2e',
            activeforeground='#ffffff',
            activebackground=color,
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )

        # Add hover effects
        def on_enter(e):
            btn.configure(bg=color, fg='#000000')

        def on_leave(e):
            btn.configure(bg='#1a1a2e', fg=color)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

        return btn

    def create_gradient_background(self):
        # Create animated gradient background
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        # This would be implemented with PIL for true gradients
        # For now, using canvas rectangles
        colors = ['#0a0a0a', '#1a1a2e', '#16213e', '#0a0a0a']

        for i, color in enumerate(colors):
            y = i * (height // len(colors))
            self.canvas.create_rectangle(0, y, width, y + height // len(colors),
                                         fill=color, outline='')

    def show_welcome_message(self):
        welcome_text = """
╔══════════════════════════════════════════════════════════════╗
║                    ⚡ WELCOME TO THE DANGER ZONE ⚡           ║
╚══════════════════════════════════════════════════════════════╝

🔥 WARNING: This is not your ordinary text editor! 🔥

• Start typing to begin your DANGEROUS writing session
• Stop typing for more than 5 seconds = TOTAL ANNIHILATION
• Your words will vanish into the digital void
• Only the brave survive... Are you ready?

💀 The timer starts the moment you type your first character 💀
⚡ Keep writing or face digital oblivion ⚡

Begin typing to enter the danger zone...
        """

        self.text_area.insert('1.0', welcome_text)
        self.text_area.tag_add('welcome', '1.0', 'end')
        self.text_area.tag_config('welcome', foreground='#00ffff', justify='center')

    def setup_events(self):
        self.text_area.bind('<KeyPress>', self.on_keystroke_premium)
        self.text_area.bind('<Button-1>', self.on_click_premium)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())

    def on_keystroke_premium(self, event):
        # Reset timer
        self.last_keystroke = time.time()

        # Play typing sound
        if self.sound_enabled:
            threading.Thread(target=self.play_typing_sound, daemon=True).start()

        # Clear welcome message with fade effect
        if self.text_area.tag_ranges('welcome'):
            self.fade_out_welcome()

        # Start timer
        if not self.timer_running:
            self.timer_running = True
            self.current_session_start = time.time()

        # Reset danger effects
        self.reset_danger_effects()

        # Update word count
        self.root.after(10, self.update_word_count_premium)

    def fade_out_welcome(self):
        def fade_step(alpha):
            if alpha > 0:
                color = f"#{int(alpha * 255):02x}{int(alpha * 255):02x}ff"
                self.text_area.tag_config('welcome', foreground=color)
                self.root.after(50, lambda: fade_step(alpha - 0.1))
            else:
                self.text_area.delete('1.0', 'end')
                self.text_area.tag_delete('welcome')

        fade_step(1.0)

    def on_click_premium(self, event):
        if self.text_area.tag_ranges('welcome'):
            self.fade_out_welcome()

    def update_timer(self):
        if self.timer_running:
            time_since_last = time.time() - self.last_keystroke
            remaining = self.danger_time - time_since_last

            if remaining <= 0:
                self.trigger_dramatic_deletion()
            else:
                self.update_timer_display(remaining)
                self.update_danger_bar(remaining / self.danger_time)

        # Schedule next update
        self.update_job = self.root.after(50, self.update_timer)  # 50ms for smooth animation

    def update_timer_display(self, remaining):
        if remaining <= 1.0:  # CRITICAL DANGER
            self.timer_label.config(
                text=f"💀 CRITICAL: {remaining:.1f}s 💀",
                fg='#ff0000'
            )
            self.start_screen_shake()
            self.start_danger_pulse()
            if self.sound_enabled:
                threading.Thread(target=self.play_alarm_sound, daemon=True).start()

        elif remaining <= 2.0:  # HIGH DANGER
            self.timer_label.config(
                text=f"⚠️ DANGER: {remaining:.1f}s ⚠️",
                fg='#ff6600'
            )
            self.start_danger_pulse()

        elif remaining <= 3.0:  # WARNING
            self.timer_label.config(
                text=f"⏰ WARNING: {remaining:.1f}s ⏰",
                fg='#ffaa00'
            )

        else:  # SAFE
            self.timer_label.config(
                text=f"✍️ WRITING: {remaining:.1f}s ✍️",
                fg='#00ff41'
            )

    def update_danger_bar(self, percentage):
        self.danger_bar.delete("all")
        width = self.danger_bar.winfo_width()
        height = self.danger_bar.winfo_height()

        if width > 1:  # Make sure widget is properly initialized
            bar_width = width * percentage

            # Color based on danger level
            if percentage < 0.2:  # Critical
                color = '#ff0000'
                glow_color = '#ff6666'
            elif percentage < 0.4:  # High danger
                color = '#ff6600'
                glow_color = '#ffaa66'
            elif percentage < 0.6:  # Warning
                color = '#ffaa00'
                glow_color = '#ffdd66'
            else:  # Safe
                color = '#00ff41'
                glow_color = '#66ff88'

            # Draw glow effect
            for i in range(3):
                glow_width = bar_width + (i * 2)
                self.danger_bar.create_rectangle(
                    0, 0, glow_width, height,
                    fill=glow_color, outline='',
                    stipple='gray25' if i > 0 else ''
                )

            # Draw main bar
            self.danger_bar.create_rectangle(
                0, 0, bar_width, height,
                fill=color, outline=''
            )

    def trigger_dramatic_deletion(self):
        # Stop timer
        self.timer_running = False

        # Start dramatic sequence
        self.start_red_screen_takeover()

    def start_red_screen_takeover(self):
        # Play destruction sound
        if self.sound_enabled:
            threading.Thread(target=self.play_destruction_sound, daemon=True).start()

        # Create red overlay
        self.red_overlay = tk.Toplevel(self.root)
        self.red_overlay.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}")
        self.red_overlay.configure(bg='#ff0000')
        self.red_overlay.attributes('-alpha', 0.0)
        self.red_overlay.attributes('-topmost', True)
        self.red_overlay.overrideredirect(True)

        # Position overlay over main window
        self.red_overlay.geometry(f"+{self.root.winfo_x()}+{self.root.winfo_y()}")

        # Fade in red screen
        self.fade_in_red_screen()

    def fade_in_red_screen(self):
        def fade_step(alpha):
            if alpha < 1.0:
                self.red_overlay.attributes('-alpha', alpha)
                self.root.after(50, lambda: fade_step(alpha + 0.1))
            else:
                # Show destruction message
                self.show_destruction_message()

        fade_step(0.0)

    def show_destruction_message(self):
        # Create dramatic message on red screen
        message_label = tk.Label(
            self.red_overlay,
            text="💀 TOTAL ANNIHILATION 💀\n\nYOUR WORDS HAVE BEEN\nCONSUMED BY THE VOID\n\n⚡ CLICK TO RESURRECT ⚡",
            font=('Orbitron', 32, 'bold'),
            fg='#ffffff',
            bg='#ff0000',
            justify='center'
        )
        message_label.pack(expand=True)

        # Add click handler to restart
        def restart_session(event):
            self.resurrect_from_ashes()

        self.red_overlay.bind('<Button-1>', restart_session)
        message_label.bind('<Button-1>', restart_session)

        # Auto-restart after 3 seconds
        self.root.after(3000, self.resurrect_from_ashes)

    def resurrect_from_ashes(self):
        # Fade out red screen
        def fade_out(alpha):
            if alpha > 0 and self.red_overlay.winfo_exists():
                self.red_overlay.attributes('-alpha', alpha)
                self.root.after(50, lambda: fade_out(alpha - 0.1))
            else:
                if self.red_overlay.winfo_exists():
                    self.red_overlay.destroy()
                self.complete_resurrection()

        if hasattr(self, 'red_overlay') and self.red_overlay.winfo_exists():
            fade_out(1.0)
        else:
            self.complete_resurrection()

    def complete_resurrection(self):
        # Clear text area
        self.text_area.delete('1.0', 'end')

        # Show resurrection message
        resurrection_text = """
╔══════════════════════════════════════════════════════════════╗
║                    🔥 PHOENIX RISING 🔥                     ║
╚══════════════════════════════════════════════════════════════╝

💀 Your words have been consumed by the digital void 💀
⚡ But like a phoenix, you shall rise again ⚡

The timer has been reset.
Your session has ended.
A new challenge awaits...

🔥 Type to begin your resurrection 🔥
        """

        self.text_area.insert('1.0', resurrection_text)
        self.text_area.tag_add('resurrection', '1.0', 'end')
        self.text_area.tag_config('resurrection', foreground='#ff6b35', justify='center')

        # Reset all states
        self.reset_all_effects()
        self.word_count_label.config(text="Words: 0")
        self.timer_label.config(text="⚡ READY TO WRITE ⚡", fg='#00ff41')

    def start_screen_shake(self):
        if self.shake_intensity < 5:
            self.shake_intensity = 5
            self.screen_shake_animation()

    def screen_shake_animation(self):
        if self.shake_intensity > 0:
            # Random shake offset
            shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_y = random.randint(-self.shake_intensity, self.shake_intensity)

            # Move window
            current_x = self.root.winfo_x()
            current_y = self.root.winfo_y()
            self.root.geometry(f"+{current_x + shake_x}+{current_y + shake_y}")

            # Reduce intensity
            self.shake_intensity -= 0.5

            # Continue animation
            self.root.after(50, self.screen_shake_animation)

    def start_danger_pulse(self):
        self.danger_pulse = 1.0
        self.danger_pulse_animation()

    def danger_pulse_animation(self):
        if self.danger_pulse > 0:
            # Pulse effect on timer
            scale = 1.0 + (math.sin(time.time() * 10) * 0.1)
            # This would scale the timer label if tkinter supported it better

            self.danger_pulse -= 0.02
            self.root.after(50, self.danger_pulse_animation)

    def start_fade_in(self):
        def fade_step(alpha):
            if alpha < 1.0:
                self.root.attributes('-alpha', alpha)
                self.root.after(50, lambda: fade_step(alpha + 0.05))

        fade_step(0.0)

    def start_continuous_animations(self):
        # Continuous subtle animations
        def animate():
            # Glow effect on title
            self.neon_glow = (self.neon_glow + 0.1) % (2 * math.pi)
            glow_intensity = (math.sin(self.neon_glow) + 1) / 2

            # Update title glow (simulated with color changes)
            blue_component = int(255 * (0.5 + glow_intensity * 0.5))
            glow_color = f"#{blue_component:02x}ffff"
            self.title_label.config(fg=glow_color)

            # Schedule next frame
            self.root.after(100, animate)

        animate()

    def reset_danger_effects(self):
        self.shake_intensity = 0
        self.danger_pulse = 0

    def reset_all_effects(self):
        self.reset_danger_effects()
        self.red_screen_active = False
        self.blur_effect_active = False

    def play_typing_sound(self):
        # Placeholder for typing sound
        pass

    def play_alarm_sound(self):
        # Placeholder for alarm sound
        pass

    def play_destruction_sound(self):
        # Placeholder for destruction sound
        pass

    def toggle_fullscreen(self, event=None):
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)

    def exit_fullscreen(self):
        self.root.attributes('-fullscreen', False)

    def on_canvas_configure(self, event):
        # Update canvas window size
        self.canvas.itemconfig(self.canvas_window, width=event.width, height=event.height)

    def update_word_count_premium(self):
        text_content = self.text_area.get('1.0', 'end-1c')

        # Don't count special messages
        if (self.text_area.tag_ranges('welcome') or
                self.text_area.tag_ranges('resurrection')):
            words = 0
        else:
            words = len([word for word in text_content.split() if word.strip()])

        self.words_written = words

        # Animate word count with color changes
        if words > 100:
            color = '#ffd700'  # Gold for high word count
        elif words > 50:
            color = '#00ff41'  # Green for good progress
        else:
            color = '#ffaa00'  # Orange for starting out

        self.word_count_label.config(text=f"Words: {words}", fg=color)

    def open_premium_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚡ Premium Settings ⚡")
        settings_window.geometry("400x500")
        settings_window.configure(bg='#1a1a2e')
        settings_window.transient(self.root)
        settings_window.grab_set()

        # Title
        title = tk.Label(
            settings_window,
            text="⚡ DANGER SETTINGS ⚡",
            font=('Orbitron', 16, 'bold'),
            fg='#00ffff',
            bg='#1a1a2e'
        )
        title.pack(pady=20)

        # Timer setting
        timer_frame = tk.Frame(settings_window, bg='#1a1a2e')
        timer_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            timer_frame,
            text="⏰ Danger Time (seconds):",
            font=('Orbitron', 12),
            fg='#ffffff',
            bg='#1a1a2e'
        ).pack(anchor='w')

        timer_var = tk.DoubleVar(value=self.danger_time)
        timer_scale = tk.Scale(
            timer_frame,
            from_=1.0,
            to=30.0,
            resolution=0.5,
            variable=timer_var,
            orient=tk.HORIZONTAL,
            bg='#1a1a2e',
            fg='#00ff41',
            highlightthickness=0,
            troughcolor='#333333',
            activebackground='#00ffff'
        )
        timer_scale.pack(fill=tk.X, pady=5)

        # Effects settings
        effects_frame = tk.Frame(settings_window, bg='#1a1a2e')
        effects_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            effects_frame,
            text="🎨 Visual Effects:",
            font=('Orbitron', 12),
            fg='#ffffff',
            bg='#1a1a2e'
        ).pack(anchor='w')

        # Checkboxes for effects
        self.screen_shake_var = tk.BooleanVar(value=True)
        self.sound_var = tk.BooleanVar(value=self.sound_enabled)

        shake_check = tk.Checkbutton(
            effects_frame,
            text="Screen Shake",
            variable=self.screen_shake_var,
            bg='#1a1a2e',
            fg='#00ff41',
            selectcolor='#333333',
            activebackground='#1a1a2e',
            activeforeground='#00ffff'
        )
        shake_check.pack(anchor='w', pady=2)

        sound_check = tk.Checkbutton(
            effects_frame,
            text="Sound Effects",
            variable=self.sound_var,
            bg='#1a1a2e',
            fg='#00ff41',
            selectcolor='#333333',
            activebackground='#1a1a2e',
            activeforeground='#00ffff'
        )
        sound_check.pack(anchor='w', pady=2)

        # Buttons
        button_frame = tk.Frame(settings_window, bg='#1a1a2e')
        button_frame.pack(fill=tk.X, padx=20, pady=20)

        def save_premium_settings():
            self.danger_time = timer_var.get()
            self.sound_enabled = self.sound_var.get()
            self.save_settings()
            settings_window.destroy()

        save_btn = self.create_neon_button(
            button_frame, "💾 SAVE", save_premium_settings, '#00ff41'
        )
        save_btn.pack(side=tk.RIGHT, padx=5)

        cancel_btn = self.create_neon_button(
            button_frame, "❌ CANCEL", settings_window.destroy, '#ff6b35'
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def save_text_premium(self):
        text_content = self.text_area.get('1.0', 'end-1c')

        # Don't save special messages
        if (self.text_area.tag_ranges('welcome') or
                self.text_area.tag_ranges('resurrection') or
                not text_content.strip()):
            messagebox.showwarning("⚠️ Nothing to Save", "No content to save!")
            return

        # Dramatic warning
        result = messagebox.askyesno(
            "💀 DANGEROUS SAVE 💀",
            "⚠️ WARNING WRITER ⚠️\n\n"
            "Saving will pause your dangerous session!\n"
            "The timer will continue after saving.\n"
            "Your words might still face digital doom!\n\n"
            "💀 Do you dare to save? 💀"
        )

        if result:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="💾 Save Your Dangerous Words"
            )

            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(text_content)
                    messagebox.showinfo("✅ Saved", f"Words saved to digital eternity:\n{filename}")
                except Exception as e:
                    messagebox.showerror("💀 Save Failed", f"The digital void consumed your save:\n{str(e)}")

    def load_settings(self):
        try:
            if os.path.exists('premium_settings.json'):
                with open('premium_settings.json', 'r') as f:
                    settings = json.load(f)
                    self.danger_time = settings.get('danger_time', 5.0)
                    self.sound_enabled = settings.get('sound_enabled', True)
        except Exception:
            pass

    def save_settings(self):
        try:
            settings = {
                'danger_time': self.danger_time,
                'sound_enabled': self.sound_enabled
            }
            with open('premium_settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception:
            pass

    def on_closing(self):
        if self.update_job:
            self.root.after_cancel(self.update_job)
        self.save_settings()

        # Clean up any overlay windows
        if hasattr(self, 'red_overlay') and self.red_overlay.winfo_exists():
            self.red_overlay.destroy()

        self.root.destroy()


def main():
    root = tk.Tk()
    app = PremiumDangerousWritingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()