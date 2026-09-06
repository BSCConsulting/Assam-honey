import os
import math
import numpy as np
from PIL import Image

def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)

def main():
    base_dir = "/Users/johnyforever/Desktop/Antigravity FIles/public"
    hero_dir = os.path.join(base_dir, "images", "hero")
    output_dir = os.path.join(base_dir, "frames")
    os.makedirs(output_dir, exist_ok=True)

    keyframe_files = [
        "image-1-honeycomb-hero.png",
        "image-2-honey-begin-to-flow.png",
        "image-3-honey-dripping-down.png",
        "image-4-honey-into-jar.png",
        "image-5-honey-swirl.png",
        "image-6-honey-spoon-lift.png",
        "image-7-final-honey-serve.png"
    ]

    target_width = 960
    target_height = 540  # 16:9 ratio matching 960 width

    # Load and preprocess keyframes
    keyframes = []
    for filename in keyframe_files:
        path = os.path.join(hero_dir, filename)
        img = Image.open(path).convert("RGB")
        # Cover-fit resize to target dimensions
        aspect = img.width / img.height
        target_aspect = target_width / target_height
        
        if aspect > target_aspect:
            new_h = target_height
            new_w = int(new_h * aspect)
        else:
            new_w = target_width
            new_h = int(new_w / aspect)
            
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Crop center
        left = (new_w - target_width) // 2
        top = (new_h - target_height) // 2
        img = img.crop((left, top, left + target_width, top + target_height))
        
        keyframes.append(np.array(img, dtype=np.float32) / 255.0)

    num_segments = len(keyframes) - 1
    frames_per_segment = 100  # 6 * 100 = 600 total frames
    frame_counter = 1

    print(f"Generating 600 frames across {num_segments} segments...")

    for seg_idx in range(num_segments):
        img_a = keyframes[seg_idx]
        img_b = keyframes[seg_idx + 1]

        for f in range(frames_per_segment):
            t = f / float(frames_per_segment)
            alpha = smoothstep(t)

            # Non-linear morph blend
            blended = (1.0 - alpha) * img_a + alpha * img_b

            # Add subtle ambient shimmer to emulate slow-motion video lighting
            shimmer = 1.0 + 0.015 * math.sin(frame_counter * 0.1)
            blended = np.clip(blended * shimmer, 0.0, 1.0)

            # Convert back to uint8 image
            frame_uint8 = (blended * 255.0).astype(np.uint8)
            frame_img = Image.fromarray(frame_uint8)

            frame_name = f"frame_{frame_counter:04d}.jpg"
            save_path = os.path.join(output_dir, frame_name)
            frame_img.save(save_path, "JPEG", quality=85)

            frame_counter += 1

    print(f"Successfully generated {frame_counter - 1} frames in {output_dir}!")

if __name__ == "__main__":
    main()
