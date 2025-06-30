#!/bin/bash

find "$1" -type d | while read dir; do
    [[ ! -d "$dir" ]] && continue
    
    confidence_dir="$dir/confidence"
    depth_dir="$dir/depth"
    
    # Check if both confidence and depth folders exist and rgb.mp4 is present
    if [[ -d "$confidence_dir" && -d "$depth_dir" && -f "$dir/rgb.mp4" ]]; then
        confidence_count=$(find "$confidence_dir" -type f | wc -l)
        depth_count=$(find "$depth_dir" -type f | wc -l)
        
        if [[ $confidence_count -ne $depth_count ]]; then
            echo "Deleting: $dir (confidence: $confidence_count files, depth: $depth_count files)"
            rm -rf "$dir"
        fi
    elif [[ -d "$confidence_dir" || -d "$depth_dir" ]]; then
        echo "Deleting: $dir (missing rgb.mp4 or confidence/depth folder)"
        rm -rf "$dir"
    fi
done
