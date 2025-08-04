#!/usr/bin/env python3
"""
YouTube Video Downloader
A comprehensive tool for downloading YouTube videos with multiple format options.
Supports both CLI and GUI interfaces.
"""

import os
import sys
import subprocess
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    tk = None
import threading
import json
from pathlib import Path

class YouTubeDownloader:
    def __init__(self):
        self.download_path = str(Path.home() / "Downloads")
        
    def get_video_info(self, url):
        """Get video information using yt-dlp"""
        try:
            cmd = ['yt-dlp', '--dump-json', '--no-download', url]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to get video info: {e.stderr}")
        except json.JSONDecodeError:
            raise Exception("Failed to parse video information")
    
    def download_video(self, url, quality='best', audio_only=False, output_path=None, progress_callback=None):
        """Download video with specified quality"""
        if output_path is None:
            output_path = self.download_path
            
        # Ensure output directory exists
        os.makedirs(output_path, exist_ok=True)
        
        # Build yt-dlp command
        cmd = ['yt-dlp']
        
        if audio_only:
            cmd.extend(['-f', 'bestaudio/best', '--extract-audio', '--audio-format', 'mp3'])
            output_template = os.path.join(output_path, '%(title)s.%(ext)s')
        else:
            if quality == 'best':
                cmd.extend(['-f', 'best'])
            elif quality == 'worst':
                cmd.extend(['-f', 'worst'])
            else:
                cmd.extend(['-f', f'best[height<={quality}]'])
            output_template = os.path.join(output_path, '%(title)s.%(ext)s')
        
        cmd.extend(['-o', output_template])
        cmd.append(url)
        
        try:
            if progress_callback:
                # Run with progress callback
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                         text=True, universal_newlines=True)
                
                for line in process.stdout:
                    progress_callback(line.strip())
                
                process.wait()
                if process.returncode != 0:
                    raise Exception("Download failed")
            else:
                # Simple run
                subprocess.run(cmd, check=True)
                
            return True
        except subprocess.CalledProcessError as e:
            raise Exception(f"Download failed: {e}")
    
    def get_available_formats(self, url):
        """Get available video formats"""
        try:
            cmd = ['yt-dlp', '-F', url]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to get formats: {e.stderr}")

class YouTubeDownloaderGUI:
    def __init__(self):
        self.downloader = YouTubeDownloader()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI interface"""
        self.root = tk.Tk()
        self.root.title("YouTube Video Downloader")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # URL input section
        ttk.Label(main_frame, text="YouTube URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Video info button
        ttk.Button(main_frame, text="Get Video Info", command=self.get_video_info).grid(
            row=0, column=3, padx=(5, 0), pady=(0, 5))
        
        # Quality selection
        ttk.Label(main_frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                   values=["best", "worst", "720", "480", "360"], state="readonly")
        quality_combo.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        # Audio only checkbox
        self.audio_only_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Audio Only (MP3)", variable=self.audio_only_var).grid(
            row=1, column=2, sticky=tk.W, padx=(10, 0), pady=(0, 5))
        
        # Output path selection
        ttk.Label(main_frame, text="Output Path:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.path_var = tk.StringVar(value=self.downloader.download_path)
        path_entry = ttk.Entry(main_frame, textvariable=self.path_var, width=50)
        path_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Button(main_frame, text="Browse", command=self.browse_path).grid(
            row=2, column=2, padx=(5, 0), pady=(0, 5))
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download", command=self.start_download)
        self.download_btn.grid(row=3, column=1, pady=10)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.progress_var).grid(row=4, column=0, columnspan=4, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(5, 10))
        
        # Log output
        ttk.Label(main_frame, text="Log Output:").grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=80)
        self.log_text.grid(row=7, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure row weights for log text expansion
        main_frame.rowconfigure(7, weight=1)
        
        # Clear log button
        ttk.Button(main_frame, text="Clear Log", command=self.clear_log).grid(
            row=8, column=0, sticky=tk.W)
        
    def log_message(self, message):
        """Add message to log output"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear the log output"""
        self.log_text.delete(1.0, tk.END)
        
    def get_video_info(self):
        """Get and display video information"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        self.progress_var.set("Getting video information...")
        self.progress_bar.start()
        
        def get_info_thread():
            try:
                info = self.downloader.get_video_info(url)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', 'Unknown')
                view_count = info.get('view_count', 0)
                
                duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"
                
                info_msg = f"Title: {title}\n"
                info_msg += f"Uploader: {uploader}\n"
                info_msg += f"Duration: {duration_str}\n"
                info_msg += f"Views: {view_count:,}\n"
                
                self.root.after(0, lambda: self.log_message(f"Video Info:\n{info_msg}"))
                self.root.after(0, lambda: messagebox.showinfo("Video Information", info_msg))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
                self.root.after(0, lambda: self.log_message(f"Error getting video info: {e}"))
            finally:
                self.root.after(0, self.progress_bar.stop)
                self.root.after(0, lambda: self.progress_var.set("Ready"))
        
        threading.Thread(target=get_info_thread, daemon=True).start()
        
    def browse_path(self):
        """Browse for output path"""
        path = filedialog.askdirectory(initialdir=self.path_var.get())
        if path:
            self.path_var.set(path)
            self.downloader.download_path = path
            
    def progress_callback(self, line):
        """Handle progress updates"""
        self.root.after(0, lambda: self.log_message(line))
        
    def start_download(self):
        """Start the download process"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        quality = self.quality_var.get()
        audio_only = self.audio_only_var.get()
        output_path = self.path_var.get()
        
        self.download_btn.config(state="disabled")
        self.progress_var.set("Downloading...")
        self.progress_bar.start()
        
        def download_thread():
            try:
                self.root.after(0, lambda: self.log_message(f"Starting download..."))
                self.root.after(0, lambda: self.log_message(f"URL: {url}"))
                self.root.after(0, lambda: self.log_message(f"Quality: {quality}"))
                self.root.after(0, lambda: self.log_message(f"Audio Only: {audio_only}"))
                self.root.after(0, lambda: self.log_message(f"Output Path: {output_path}"))
                
                success = self.downloader.download_video(
                    url, quality, audio_only, output_path, self.progress_callback
                )
                
                if success:
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))
                    self.root.after(0, lambda: self.log_message("Download completed successfully!"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Download failed: {e}"))
                self.root.after(0, lambda: self.log_message(f"Download failed: {e}"))
            finally:
                self.root.after(0, self.progress_bar.stop)
                self.root.after(0, lambda: self.progress_var.set("Ready"))
                self.root.after(0, lambda: self.download_btn.config(state="normal"))
        
        threading.Thread(target=download_thread, daemon=True).start()
        
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

def cli_interface():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="YouTube Video Downloader")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-q", "--quality", default="best", 
                       choices=["best", "worst", "720", "480", "360"],
                       help="Video quality (default: best)")
    parser.add_argument("-a", "--audio-only", action="store_true",
                       help="Download audio only (MP3)")
    parser.add_argument("-o", "--output", help="Output directory path")
    parser.add_argument("-i", "--info", action="store_true",
                       help="Show video information only")
    parser.add_argument("-f", "--formats", action="store_true",
                       help="Show available formats")
    
    args = parser.parse_args()
    
    downloader = YouTubeDownloader()
    
    if args.output:
        downloader.download_path = args.output
    
    try:
        if args.info:
            print("Getting video information...")
            info = downloader.get_video_info(args.url)
            print(f"Title: {info.get('title', 'Unknown')}")
            print(f"Uploader: {info.get('uploader', 'Unknown')}")
            duration = info.get('duration', 0)
            if duration:
                print(f"Duration: {duration // 60}:{duration % 60:02d}")
            print(f"Views: {info.get('view_count', 0):,}")
            
        elif args.formats:
            print("Available formats:")
            formats = downloader.get_available_formats(args.url)
            print(formats)
            
        else:
            print(f"Downloading from: {args.url}")
            print(f"Quality: {args.quality}")
            print(f"Audio only: {args.audio_only}")
            print(f"Output path: {downloader.download_path}")
            
            def progress_callback(line):
                print(line)
            
            success = downloader.download_video(
                args.url, args.quality, args.audio_only, 
                downloader.download_path, progress_callback
            )
            
            if success:
                print("\nDownload completed successfully!")
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # CLI mode
        cli_interface()
    else:
        # GUI mode
        if not TKINTER_AVAILABLE:
            print("GUI not available. tkinter is not installed.")
            print("To install tkinter: sudo apt install python3-tk")
            print("")
            print("Usage for CLI: python3 youtube_downloader.py <URL> [options]")
            print("Run with --help for more options")
            print("")
            print("Example: python3 youtube_downloader.py 'https://youtu.be/dQw4w9WgXcQ' --quality 720")
            return
        
        try:
            app = YouTubeDownloaderGUI()
            app.run()
        except Exception as e:
            print(f"Error starting GUI: {e}")
            print("You can still use the CLI interface.")
            print("Usage: python3 youtube_downloader.py <URL> [options]")

if __name__ == "__main__":
    main()