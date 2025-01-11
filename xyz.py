import streamlit as st
import subprocess
import os
from urllib.parse import urlparse
from io import BytesIO

# Function to extract the domain from the URL
def get_domain(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc
    except Exception as e:
        st.error(f"Error parsing URL: {e}")
        return None

# Function to download video using yt-dlp
def download_video(url):
    try:
        # Create a temporary filename
        output_filename = "downloaded_video.%(ext)s"
        command = ["yt-dlp", "--output", output_filename, url]
        
        # Run the yt-dlp command
        subprocess.run(command, check=True)
        
        # Locate the downloaded file
        for file in os.listdir():
            if file.startswith("downloaded_video."):
                return file
        st.error("Video file not found.")
        return None
    except subprocess.CalledProcessError as e:
        st.error(f"Failed to download video: {e}")
        return None
    except FileNotFoundError:
        st.error("yt-dlp is not installed. Please install it using `pip install yt-dlp`.")
        return None

# Streamlit app
def main():
    st.title("Multi-Platform Video Downloader")
    st.write("Supported platforms: YouTube, Facebook, Instagram, Terabox, MEGA, Telegram")
    
    # URL input
    url = st.text_input("Enter the video URL:")
    
    if st.button("Download"):
        if not url:
            st.error("Please enter a valid URL.")
            return

        domain = get_domain(url)
        if not domain:
            st.error("Invalid URL. Please try again.")
            return

        # Check if the platform is supported
        supported_domains = {
            "youtube.com": "YouTube",
            "youtu.be": "YouTube",
            "facebook.com": "Facebook",
            "instagram.com": "Instagram",
            "terabox.com": "Terabox",
            "mega.nz": "MEGA",
            "t.me": "Telegram",
        }

        platform_detected = None
        for key in supported_domains:
            if key in domain:
                platform_detected = supported_domains[key]
                break

        if platform_detected:
            st.info(f"Platform detected: {platform_detected}")
            st.write("Downloading video...")

            # Download the video
            file_path = download_video(url)

            if file_path:
                # Read the file content
                with open(file_path, "rb") as f:
                    file_data = f.read()
                
                # Provide a download button
                st.download_button(
                    label="Click here to download your video",
                    data=file_data,
                    file_name=file_path,
                    mime="video/mp4",
                )
                
                # Clean up downloaded file
                os.remove(file_path)
        else:
            st.error("Unsupported platform. Supported platforms include:")
            for platform in supported_domains.values():
                st.write(f"- {platform}")

if __name__ == "__main__":
    main()
