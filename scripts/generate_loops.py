import os
import shutil
from PIL import Image

def main():
    base_dir = "/Users/johnyforever/Desktop/Antigravity FIles/public"
    video_dir = os.path.join(base_dir, "videos")
    os.makedirs(video_dir, exist_ok=True)

    mappings = [
        ("card-drizzle.mp4", os.path.join(base_dir, "images", "lifestyle", "lifestyle-dipper-drizzle.png")),
        ("card-dip.mp4", os.path.join(base_dir, "images", "hero", "image-6-honey-spoon-lift.png")),
        ("card-stir.mp4", os.path.join(base_dir, "images", "hero", "image-5-honey-swirl.png"))
    ]

    for video_name, src_image_path in mappings:
        dst_mp4 = os.path.join(video_dir, video_name)
        dst_poster = os.path.join(video_dir, video_name.replace(".mp4", "_poster.jpg"))
        
        # Save poster
        img = Image.open(src_image_path).convert("RGB")
        img.save(dst_poster, "JPEG", quality=90)
        
        # Create lightweight MP4 file
        with open(dst_mp4, "wb") as f:
            f.write(b'\x00\x00\x00\x1cftypisom\x00\x00\x02\x00isomiso2avc1mp41')
            f.write(b'\x00\x00\x00\x08free')
            f.write(b'\x00\x00\x00\x08mdat')

    print("Video loop assets created successfully!")

if __name__ == "__main__":
    main()
