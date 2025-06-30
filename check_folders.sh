#!/bin/bash

find "$1" -type d | while read dir; do
    [[ ! -d "$dir" ]] && continue
    
    confidence_dir="$dir/confidence"
    depth_dir="$dir/depth"
    
    # Check if both confidence and depth folders exist
    if [[ -d "$confidence_dir" && -d "$depth_dir" ]]; then
        confidence_count=$(find "$confidence_dir" -type f | wc -l)
        depth_count=$(find "$depth_dir" -type f | wc -l)
        
        if [[ $confidence_count -ne $depth_count ]]; then
            echo "Deleting: $dir (confidence: $confidence_count images, depth: $depth_count images)"
            rm -rf "$dir"
        fi
    fi
done
